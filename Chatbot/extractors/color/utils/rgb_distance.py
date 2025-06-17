#Chatbot/extractors/color/utils/rgb_distance.py
"""
rgb_distance.py
===============

Low-level RGB utilities for handling color distance, similarity,
and representative selection.

This module provides mathematical and heuristic tools for working with
RGB tuples extracted from user-facing color descriptions. It serves
as a utility backbone for tasks like:

- Color similarity scoring
- Color distance minimization
- Selecting representative RGB values from phrase-level mappings

Why This Matters:
-----------------
User inputs often produce multiple valid color candidates (e.g., "muted rose",
"soft pink"), each with an associated RGB. Selecting a single representative
color is necessary for:

- Visual swatch display
- Single-color product matching
- Prompt injection into LLM responses

Core Functions:
---------------
- `choose_representative_rgb()`:
    Returns the first available RGB tuple from a mapping (simple fallback logic).

Planned Extensions:
-------------------
This module may later include:
- Euclidean RGB distance calculation
- Weighted RGB averaging
- Clustering of RGB values by perceptual similarity

Example Usage:
--------------
>>> rgb_map = {"soft pink": (255,182,193), "muted coral": (240,128,128)}
>>> choose_representative_rgb(rgb_map)
(255,182,193)

Dependencies:
-------------
- Standard library only
"""

import math
from rapidfuzz import process
from typing import Dict, Tuple, Optional, List

import webcolors
from matplotlib.colors import XKCD_COLORS, CSS4_COLORS

import logging

logger = logging.getLogger(__name__)

def choose_representative_rgb(
    rgb_mapping: Dict[str, Tuple[int, int, int]]
) -> Optional[Tuple[int, int, int]]:
    """
    Selects a single representative RGB value from a mapping of phrases → RGB.

    This function returns the first RGB tuple found in the mapping.
    It does not apply ranking, scoring, or prioritization logic —
    it simply returns the first available value.

    Useful for:
    - Displaying a single swatch in a summary
    - Feeding into LLM prompts when only one color is needed

    Args:
        rgb_mapping (Dict[str, Tuple[int, int, int]]): Phrase → RGB value map.

    Returns:
        Optional[Tuple[int, int, int]]: A single RGB value, or None if input is empty.

    Example:
        >>> choose_representative_rgb({"soft pink": (255,182,193), "nude": (205,133,63)})
        (255,182,193)
    """
    return next(iter(rgb_mapping.values()), None)

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




def find_similar_color_names(
    base_rgb: Tuple[int, int, int],
    rgb_map: Dict[str, Tuple[int, int, int]],
    threshold: float = 60.0
) -> List[str]:
    """
    Finds color names in the RGB map that are within a given distance from the base RGB.

    Used to retrieve similar or approximate color names for a resolved tone,
    based on Euclidean proximity in RGB space.

    Args:
        base_rgb (Tuple[int, int, int]): Reference RGB color.
        rgb_map (Dict[str, Tuple[int, int, int]]): Mapping of color name → RGB.
        threshold (float): Distance threshold (default: 60.0).

    Returns:
        List[str]: List of color names within threshold distance.
    """
    return [
        name for name, rgb in rgb_map.items()
        if is_within_rgb_margin(base_rgb, rgb, threshold)
    ]


def fuzzy_match_rgb_from_known_colors(color_phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Resolves a color phrase to an RGB triplet using exact and fuzzy matching.
    Prioritizes CSS4 color names over XKCD when both are valid matches.

    Args:
        color_phrase (str): Cleaned color term (e.g., 'dusty rose').

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple if match found, else None.
    """
    simplified = color_phrase.lower().replace(" ", "")

    # ---------- Exact Match ----------
    if simplified in CSS4_COLORS:
        return webcolors.hex_to_rgb(CSS4_COLORS[simplified])
    if f"xkcd:{simplified}" in XKCD_COLORS:
        return webcolors.hex_to_rgb(XKCD_COLORS[f"xkcd:{simplified}"])

    # ---------- Fuzzy Match: CSS4 First ----------
    try:
        css_names = list(CSS4_COLORS.keys())
        best_match_css, score_css = process.extractOne(simplified, css_names)
        if score_css >= 80:
            hex_code = CSS4_COLORS.get(best_match_css)
            if hex_code:
                return webcolors.hex_to_rgb(hex_code)
    except Exception as e:
        logger.error(f"[FUZZY MATCH] CSS4 error for '{simplified}': {e}")

    # ---------- Fuzzy Match: XKCD Fallback ----------
    try:
        xkcd_names = [name.replace("xkcd:", "") for name in XKCD_COLORS]
        best_match_xkcd, score_xkcd = process.extractOne(simplified, xkcd_names)
        if score_xkcd >= 80:
            hex_code = XKCD_COLORS.get(f"xkcd:{best_match_xkcd}")
            if hex_code:
                return webcolors.hex_to_rgb(hex_code)
    except Exception as e:
        logger.error(f"[FUZZY MATCH] XKCD error for '{simplified}': {e}")

    return None