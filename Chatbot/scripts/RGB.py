import webcolors
from thefuzz import process
from matplotlib.colors import XKCD_COLORS, CSS4_COLORS

from Chatbot.extractors.colors import simplify_color_description_with_llm  # existing simplifier
from typing import Tuple, List
import math

import os
import json
import re
import requests
from typing import Optional, Tuple

def query_llm_for_rgb(color_phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Uses LLM via OpenRouter to estimate the RGB value of a descriptive color phrase.
    Handles noisy output using regex-based JSON extraction.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env")

    prompt = (
        f"You're a color matching assistant. Given the color name '{color_phrase}', "
        f"estimate its most accurate RGB value based on design and fashion industry standards. "
        f"Return only the result in this exact JSON format: {{\"rgb\": [R, G, B]}} "
        f"with integers between 0 and 255. No explanation.\n\n"
        f"Use the following reference examples to calibrate your answers:\n"
        f"- {{\"rgb\": [213, 138, 148]}} for 'dusty pink' → muted mauve pink\n"
        f"- {{\"rgb\": [243, 207, 183]}} for 'peachy beige' → warm skin-tone peach\n"
        f"- {{\"rgb\": [136, 8, 8]}} for 'deep cherry red' → dark dramatic red\n"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 20,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"[LLM ERROR] Status: {response.status_code} | Message: {response.text}")
        return None

    raw_output = response.json()["choices"][0]["message"]["content"].strip()

    # 🔍 Use regex to extract only the valid JSON block (e.g., {"rgb": [R, G, B]})
    # Extract valid JSON block using regex (tolerant of slight formatting issues)
    match = re.search(r'\{\s*"rgb"\s*:\s*\[\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*]', raw_output)
    if match:
        try:
            r, g, b = map(int, match.groups())
            rgb = (r, g, b)
            if all(0 <= val <= 255 for val in rgb):
                print(f"[🎯 LLM RGB MATCH] → {rgb}")
                return rgb
        except Exception as e:
            print(f"[⚠️ LLM PARSE FAILED] Extracted groups: {match.groups()}\nError: {e}")
    else:
        print(f"[⚠️ LLM PARSE FAILED] Raw:  {raw_output}\nNo valid JSON found.")

    return None


def get_rgb_from_descriptive_color_llm_first(input_color: str) -> Optional[Tuple[int, int, int]]:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"[🎨 INPUT COLOR] → '{input_color}'")

    # Step 1 → Try LLM RGB prediction directly
    rgb_llm = query_llm_for_rgb(input_color)
    if rgb_llm:
        return rgb_llm

    # Step 2 → Fallback to simplification + fuzzy matching
    simplified_list = simplify_color_description_with_llm(input_color)
    if not simplified_list:
        print("[❌ LLM Simplification] → No valid simplified result")
        return None

    simplified = simplified_list[0]
    print(f"[✅ LLM SIMPLIFIED] → '{simplified}'")

    # 3. Try exact match in xkcd
    for name, hex_code in XKCD_COLORS.items():
        if simplified == name.replace("xkcd:", ""):
            rgb = webcolors.hex_to_rgb(hex_code)
            print(f"[🎯 XKCD EXACT MATCH] → '{name}' = {rgb}")
            return rgb

    # 4. Exact match in CSS4
    if simplified in CSS4_COLORS:
        rgb = webcolors.hex_to_rgb(CSS4_COLORS[simplified])
        print(f"[🎯 CSS4 EXACT MATCH] → '{simplified}' = {rgb}")
        return rgb

    # 5. Fuzzy match: XKCD
    xkcd_names = [name.replace("xkcd:", "") for name in XKCD_COLORS]
    best_match_xkcd, score_xkcd = process.extractOne(simplified, xkcd_names)
    if score_xkcd >= 80:
        hex_code = XKCD_COLORS[f"xkcd:{best_match_xkcd}"]
        rgb = webcolors.hex_to_rgb(hex_code)
        print(f"[🔍 FUZZY MATCH - XKCD] → '{best_match_xkcd}' (score={score_xkcd}) = {rgb}")
        return rgb

    # 6. Fuzzy match: CSS4
    css_names = list(CSS4_COLORS.keys())
    best_match_css, score_css = process.extractOne(simplified, css_names)
    if score_css >= 80:
        rgb = webcolors.hex_to_rgb(CSS4_COLORS[best_match_css])
        print(f"[🔍 FUZZY MATCH - CSS4] → '{best_match_css}' (score={score_css}) = {rgb}")
        return rgb

    print("[❌ NO MATCH FOUND]")
    return None


def rgb_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Computes the Euclidean distance between two RGB colors.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


def is_within_rgb_margin(base_rgb: Tuple[int, int, int], test_rgb: Tuple[int, int, int],
                         threshold: float = 60.0) -> bool:
    """
    Returns True if the test_rgb is within the color margin of base_rgb.

    Args:
        base_rgb: The reference RGB (e.g. (255, 0, 0))
        test_rgb: The RGB to compare
        threshold: Maximum distance allowed

    Returns:
        bool: Whether test_rgb is close enough to base_rgb
    """
    return rgb_distance(base_rgb, test_rgb) <= threshold


def find_similar_color_names(base_rgb: Tuple[int, int, int],
                             rgb_map: dict,
                             threshold: float = 60.0) -> List[str]:
    """
    Returns a list of color names from rgb_map that are within a certain distance from the base_rgb.

    Args:
        base_rgb: Reference RGB tuple (e.g. (255, 0, 0))
        rgb_map: Dictionary {color_name: (r, g, b)}
        threshold: Max distance

    Returns:
        List[str]: Matching color names
    """
    return [
        name for name, rgb in rgb_map.items()
        if is_within_rgb_margin(base_rgb, rgb, threshold)
    ]
