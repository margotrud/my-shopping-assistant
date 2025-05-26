# Chatbot/extractors/color/rgb_utils.py
"""
RGB Utilities (Color-Specific)
-------------------------------
Provides utilities to:
- Query an LLM for RGB color estimation based on descriptive color names.
- Compute RGB distance and similarity.
- Find known colors similar to a given RGB.
- Fuzzy match simplified color phrases to known XKCD and CSS4 palettes.
"""

import math
import json
import logging
import os
import re
from typing import Optional, Tuple, List, Dict

import requests
import webcolors
from matplotlib.colors import XKCD_COLORS, CSS4_COLORS
from rapidfuzz import process

from Chatbot.extractors.color.simplifier import simplify_color_description_with_llm


logger = logging.getLogger(__name__)

# Precompile RGB extraction regex for performance
RGB_REGEX = re.compile(r'\{\s*"rgb"\s*:\s*\[\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\]\s*\}')


def build_llm_request_payload(color_phrase: str) -> dict:
    """
    Builds the payload dictionary for the LLM RGB query.

    Args:
        color_phrase (str): Descriptive color name.

    Returns:
        dict: JSON payload for the LLM request.
    """
    prompt = (
        f"You're a color matching assistant. Given the color name '{color_phrase}', "
        "estimate its most accurate RGB value based on design and fashion industry standards. "
        "Return only the result in this exact JSON format: {\"rgb\": [R, G, B]} "
        "with integers between 0 and 255. No explanation.\n\n"
        "Use examples like: 'dusty pink' → [213, 138, 148], 'peachy beige' → [243, 207, 183]"
    )
    return {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 20,
    }


def build_llm_headers(api_key: str) -> dict:
    """
    Constructs HTTP headers for LLM API call.

    Args:
        api_key (str): API key for authorization.

    Returns:
        dict: Headers for the request.
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def query_llm_for_rgb(color_phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Queries the LLM to estimate the RGB value for a descriptive color phrase.

    Args:
        color_phrase (str): Descriptive color name.

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple if successfully parsed; None otherwise.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    try:
        headers = build_llm_headers(api_key)
        payload = build_llm_request_payload(color_phrase)
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"LLM request failed: {e}")
        return None

    try:
        raw_output = response.json()["choices"][0]["message"]["content"].strip()
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Invalid JSON response from LLM: {e}")
        return None

    match = RGB_REGEX.search(raw_output)
    if match:
        try:
            r, g, b = map(int, match.groups())
            if all(0 <= val <= 255 for val in (r, g, b)):
                return (r, g, b)
            logger.warning(f"RGB values out of range: {r}, {g}, {b}")
        except Exception as e:
            logger.error(f"Error parsing RGB values: {e}")
    else:
        logger.warning(f"Unexpected LLM output format: {raw_output}")

    return None


def get_rgb_from_descriptive_color_llm_first(input_color: str) -> Optional[Tuple[int, int, int]]:
    """
    Attempts to resolve the RGB value for a descriptive color term by:
    1. Querying the LLM directly.
    2. Simplifying the color phrase and checking exact matches in XKCD and CSS4 palettes.
    3. Fuzzy matching known colors as a fallback.

    Args:
        input_color (str): Descriptive color term.

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple if found, else None.
    """
    try:
        rgb = query_llm_for_rgb(input_color)
        if rgb:
            return rgb
    except Exception as e:
        logger.error(f"LLM RGB query failed for '{input_color}': {e}")

    try:
        simplified_list = simplify_color_description_with_llm(input_color)
    except Exception as e:
        logger.error(f"Failed to simplify color '{input_color}': {e}")
        return None

    if not simplified_list:
        return None

    simplified = simplified_list[0].lower()

    # Exact match in XKCD colors
    for name, hex_code in XKCD_COLORS.items():
        clean_name = name.replace("xkcd:", "").lower()
        if simplified == clean_name:
            try:
                return webcolors.hex_to_rgb(hex_code)
            except ValueError as e:
                logger.warning(f"Invalid hex code '{hex_code}' for XKCD color '{name}': {e}")
            break

    # Exact match in CSS4 colors
    if simplified in CSS4_COLORS:
        try:
            return webcolors.hex_to_rgb(CSS4_COLORS[simplified])
        except ValueError as e:
            logger.warning(f"Invalid hex code '{CSS4_COLORS[simplified]}' for CSS4 color '{simplified}': {e}")

    # Fuzzy match fallback
    try:
        return fuzzy_match_rgb_from_known_colors(simplified)
    except Exception as e:
        logger.error(f"Fuzzy matching failed for '{simplified}': {e}")

    return None


def rgb_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Calculates Euclidean distance between two RGB colors.

    Args:
        rgb1 (Tuple[int, int, int]): First RGB color.
        rgb2 (Tuple[int, int, int]): Second RGB color.

    Returns:
        float: Euclidean distance between rgb1 and rgb2.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


def is_within_rgb_margin(base_rgb: Tuple[int, int, int],
                         test_rgb: Tuple[int, int, int],
                         threshold: float = 60.0) -> bool:
    """
    Checks if two RGB colors are within a specified Euclidean distance threshold.

    Args:
        base_rgb (Tuple[int, int, int]): Reference RGB color.
        test_rgb (Tuple[int, int, int]): RGB color to test.
        threshold (float): Distance threshold to determine similarity.

    Returns:
        bool: True if test_rgb is within threshold of base_rgb, else False.
    """
    return rgb_distance(base_rgb, test_rgb) <= threshold


def find_similar_color_names(base_rgb: Tuple[int, int, int],
                             rgb_map: Dict[str, Tuple[int, int, int]],
                             threshold: float = 60.0) -> List[str]:
    """
    Finds all color names in rgb_map within threshold distance from base_rgb.

    Args:
        base_rgb (Tuple[int, int, int]): Reference RGB color.
        rgb_map (Dict[str, Tuple[int, int, int]]): Mapping of color names to RGB values.
        threshold (float): Distance threshold for similarity.

    Returns:
        List[str]: List of color names within threshold distance.
    """
    return [
        name for name, rgb in rgb_map.items()
        if is_within_rgb_margin(base_rgb, rgb, threshold)
    ]


def fuzzy_match_rgb_from_known_colors(color_phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Fuzzy matches a simplified color phrase to known XKCD or CSS4 colors.

    Args:
        color_phrase (str): Color phrase to match.

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple if match found, else None.
    """
    simplified = color_phrase.lower()

    try:
        xkcd_names = [name.replace("xkcd:", "") for name in XKCD_COLORS]
        best_match_xkcd, score_xkcd = process.extractOne(simplified, xkcd_names)
        if score_xkcd >= 80:
            hex_code = XKCD_COLORS.get(f"xkcd:{best_match_xkcd}")
            if hex_code:
                return webcolors.hex_to_rgb(hex_code)
    except Exception as e:
        logger.error(f"XKCD fuzzy matching failed for '{simplified}': {e}")

    try:
        css_names = list(CSS4_COLORS.keys())
        best_match_css, score_css = process.extractOne(simplified, css_names)
        if score_css >= 80:
            hex_code = CSS4_COLORS.get(best_match_css)
            if hex_code:
                return webcolors.hex_to_rgb(hex_code)
    except Exception as e:
        logger.error(f"CSS4 fuzzy matching failed for '{simplified}': {e}")

    return None
