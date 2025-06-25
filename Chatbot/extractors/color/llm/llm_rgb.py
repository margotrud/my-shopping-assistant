# Chatbot/extractors/color/llm/llm_rgb.py

"""
llm_rgb.py
==========

Handles LLM-driven resolution of descriptive color names into RGB tuples.
Attempts multi-step fallback: LLM → simplified match → XKCD/CSS → fuzzy RGB.
"""
import logging
from typing import Optional, Tuple
from webcolors import hex_to_rgb
from matplotlib.colors import XKCD_COLORS, CSS4_COLORS

from Chatbot.extractors.color.llm.llm_api_client import query_llm_for_rgb
from Chatbot.extractors.color.llm.simplifier import simplify_color_description_with_llm
from Chatbot.extractors.color.utils.rgb_distance import fuzzy_match_rgb_from_known_colors, is_within_rgb_margin
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def resolve_rgb_with_llm(
    phrase: str,
    all_webcolor_names: set,
    llm_client,
    cache=None,
    debug=False
) -> Optional[Tuple[int, int, int]]:
    """
    Full RGB resolution entry point: LLM first, then fallback.
    """
    return get_rgb_from_descriptive_color_llm_first(
        input_color=phrase,
        all_webcolor_names=all_webcolor_names,
        llm_client=llm_client,
        cache=cache,
        debug=debug
    )

def get_rgb_from_descriptive_color_llm_first(
    input_color: str,
    all_webcolor_names: set,
    llm_client,
    cache=None,
    debug=False
) -> Optional[Tuple[int, int, int]]:
    """
    Step-by-step resolution:
    1. Direct LLM RGB call
    2. Simplify → match in XKCD / CSS4
    3. Fuzzy match fallback from known set
    """
    if debug:
        print(f"[🎯 RESOLVE RGB] Trying: '{input_color}'")

    rgb = query_llm_for_rgb(input_color, llm_client, cache=cache, debug=debug)
    if rgb:
        return rgb

    simplified = simplify_color_description_with_llm(input_color, llm_client, cache=cache, debug=debug)

    rgb = _try_simplified_match(simplified, all_webcolor_names, debug=debug)
    if rgb:
        return rgb

    rgb = fuzzy_match_rgb_from_known_colors(simplified, all_webcolor_names, debug=debug)
    if rgb:
        return rgb

    if debug:
        print(f"[❌ NO RGB FOUND] '{input_color}' → Failed")
    return None


def _try_simplified_match(name: str, color_names: set, debug=False) -> Optional[Tuple[int, int, int]]:
    """
    Attempts to match a simplified phrase directly to known color names in CSS/XKCD.
    """
    name = normalize_token(name).replace("-", " ")

    if name in XKCD_COLORS:
        hex_code = XKCD_COLORS[name]
        if debug:
            print(f"[🎨 XKCD MATCH] '{name}' → {hex_code}")
        return hex_to_rgb(hex_code)

    if name in CSS4_COLORS:
        hex_code = CSS4_COLORS[name]
        if debug:
            print(f"[🎨 CSS4 MATCH] '{name}' → {hex_code}")
        return hex_to_rgb(hex_code)

    if debug:
        print(f"[🕵️‍♀️ NOT FOUND] '{name}' not in XKCD or CSS4")
    return None


