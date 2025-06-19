# Chatbot/extractors/color/llm/llm_rgb.py

"""
llm_rgb.py
==========

LLM-powered RGB resolution module.

This module defines logic to convert descriptive color phrases into RGB
values using a large language model (LLM). It is useful when the phrase is
non-standard, abstract, or not directly mappable to a known CSS/XKCD name.

Example phrases:
- "rosy nude"
- "muted champagne"
- "soft autumn blush"

Key Functions:
--------------
- `get_rgb_from_descriptive_color_llm_first()`: Core LLM query logic (mockable)
- `resolve_rgb_with_llm()`: Public API for RGB resolution using LLM

Planned Extensions:
-------------------
- Multi-step fallback (e.g., tone-level averaging, webcolor backup)
- LLM caching for performance
- Ranking of multiple candidate RGBs

Dependencies:
-------------
- LLM cache or API logic
- Standard RGB tuple representation
"""

from Chatbot.cache.color_llm_cache import ColorLLMCache
cache = ColorLLMCache.get_instance()
from typing import Optional, Set, Tuple

def resolve_rgb_with_llm(
    phrase: str,
    known_tones: Set[str]  # currently unused, placeholder for future disambiguation
) -> Optional[Tuple[int, int, int]]:
    """
    Resolves the RGB value for a color phrase using the LLM-backed interpretation engine.

    This function sends the phrase to a descriptive LLM endpoint and returns
    the resolved RGB tuple if successful.

    Args:
        phrase (str): The user-facing descriptive phrase (e.g., "muted dusty rose").
        known_tones (Set[str]): Available base tones (reserved for future fallback logic).

    Returns:
            Optional[Tuple[int, int, int]]: RGB triplet if resolved, else None.

    Example:
        >>> resolve_rgb_with_llm("rosy nude", known_tones)
        (225, 190, 200)
    """
    return get_rgb_from_descriptive_color_llm_first(phrase)

logger = logging.getLogger(__name__)


def get_rgb_from_descriptive_color_llm_first(input_color: str) -> Optional[Tuple[int, int, int]]:
    """
    Attempts to resolve a descriptive color phrase into an RGB tuple using a hybrid strategy:
    1. LLM query via OpenRouter
    2. Simplification and matching in CSS4 or XKCD color dictionaries
    3. Fuzzy fallback to closest RGB

    Args:
        input_color (str): Descriptive color name (e.g., 'dusty coral').

    Returns:
        Optional[Tuple[int, int, int]]: RGB triplet if found, else None.
    """
    rgb_cached = cache.get_rgb(input_color)
    if rgb_cached:
        return rgb_cached

    try:
        rgb = query_llm_for_rgb(input_color)
        if rgb:
            cache.store_rgb(input_color, rgb)  # ✅ You forgot this line!
            return rgb
    except Exception as e:
        logger.error(f"[LLM FAILURE] '{input_color}' → {e}")

    try:
        simplified_list = simplify_color_description_with_llm(input_color)
    except Exception as e:
        logger.error(f"[SIMPLIFICATION ERROR] '{input_color}' → {e}")
        return None

    if not simplified_list:
        return None

    simplified = simplified_list[0].lower()

    # Exact match in XKCD
    for name, hex_code in XKCD_COLORS.items():
        clean_name = name.replace("xkcd:", "").lower()
        if simplified == clean_name:
            try:
                return webcolors.hex_to_rgb(hex_code)
            except ValueError as e:
                logger.warning(f"[HEX PARSE ERROR] {hex_code} → {e}")
            break

    # Exact match in CSS4
    if simplified in CSS4_COLORS:
        try:
            return webcolors.hex_to_rgb(CSS4_COLORS[simplified])
        except ValueError as e:
            logger.warning(f"[CSS4 HEX ERROR] {simplified} → {e}")

    # Fallback: fuzzy match to closest RGB
    try:
        return fuzzy_match_rgb_from_known_colors(simplified)
    except Exception as e:
        logger.error(f"[FUZZY MATCH ERROR] '{simplified}' → {e}")

    return None

def rgb_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Computes the Euclidean distance between two RGB color tuples.

    Args:
        rgb1 (Tuple[int, int, int]): First RGB value.
        rgb2 (Tuple[int, int, int]): Second RGB value.

    Returns:
        float: Distance in RGB space.
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


def is_within_rgb_margin(
    base_rgb: Tuple[int, int, int],
    test_rgb: Tuple[int, int, int],
    threshold: float = 60.0
) -> bool:
    """
    Checks whether two RGB tuples are close enough in color space.

    Args:
        base_rgb (Tuple[int, int, int]): Reference color.
        test_rgb (Tuple[int, int, int]): Test color to compare.
        threshold (float): Maximum allowed distance.

    Returns:
        bool: True if the test color is within the margin.
    """
    return rgb_distance(base_rgb, test_rgb) <= threshold


