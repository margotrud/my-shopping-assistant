# Chatbot/extractors/color/utils/rgb_distance.py

"""
rgb_distance.py
===============

Functions for RGB color comparison, similarity lookup,
and fallback name matching based on perceptual closeness.

Used By:
--------
- LLM color resolution
- Sentiment RGB clustering
- Fallback phrase simplification
"""

from typing import Tuple, Dict, Optional, List
from Chatbot.extractors.color.shared.vocab import all_webcolor_names


def rgb_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Computes Euclidean distance between two RGB colors.

    Args:
        rgb1 (Tuple[int, int, int]): First color.
        rgb2 (Tuple[int, int, int]): Second color.

    Returns:
        float: Euclidean distance in RGB space.
    """
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)) ** 0.5


def is_within_rgb_margin(
    rgb1: Tuple[int, int, int],
    rgb2: Tuple[int, int, int],
    margin: float = 60.0
) -> bool:
    """
    Determines if two RGB values are close within a given margin.

    Args:
        rgb1, rgb2: RGB colors to compare.
        margin (float): Maximum allowable distance.

    Returns:
        bool: True if within margin.
    """
    return rgb_distance(rgb1, rgb2) <= margin


def choose_representative_rgb(
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Optional[Tuple[int, int, int]]:
    """
    Picks the most central RGB color from a group using centroid minimization.

    Args:
        rgb_map (Dict[str, Tuple]): Mapping of color phrases to RGB values.

    Returns:
        RGB tuple that minimizes total distance to all others, or None if empty.
    """
    if not rgb_map:
        return None

    candidates = list(rgb_map.values())
    min_total = float("inf")
    best_rgb = None

    for candidate in candidates:
        total = sum(rgb_distance(candidate, other) for other in candidates)
        if total < min_total:
            min_total = total
            best_rgb = candidate

    return best_rgb


def find_similar_color_names(
    base_rgb: Tuple[int, int, int],
    known_rgb_map: Dict[str, Tuple[int, int, int]],
    threshold: float = 60.0
) -> List[str]:
    """
    Finds color names from a known map that are perceptually similar to a target RGB.

    Args:
        base_rgb: Target RGB color.
        known_rgb_map: Mapping from name → RGB tuple.
        threshold: Max allowable distance.

    Returns:
        List[str]: Sorted matching color names within margin.
    """
    return sorted([
        name for name, rgb in known_rgb_map.items()
        if is_within_rgb_margin(rgb, base_rgb, margin=threshold)
    ])


def fuzzy_match_rgb_from_known_colors(
    phrase: str,
    known_rgb_map: Dict[str, Tuple[int, int, int]]
) -> Optional[str]:
    """
    Attempts to match a phrase to the closest known named RGB color.

    Args:
        phrase (str): Simplified color phrase (e.g., 'peachy nude').
        known_rgb_map (Dict[str, Tuple]): Reference RGB names.

    Returns:
        str or None: Closest color name within margin, if found.
    """
    import difflib

    candidates = difflib.get_close_matches(phrase, all_webcolor_names, n=1, cutoff=0.75)
    if candidates:
        return candidates[0]
    return None
