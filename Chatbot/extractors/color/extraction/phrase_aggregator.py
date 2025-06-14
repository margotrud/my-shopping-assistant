#Chatbot/extractors/color/extraction/phrase_aggregator.py
"""
phrase_aggregator.py
====================

Aggregates structured color parsing results across multiple text segments.

This module acts as the final collector for simplified color phrases, tones,
modifiers, and RGB mappings. It calls low-level color parsing logic on
individual segments, then merges the outputs into unified collections.

Used for:
---------
- Consolidating user input from multiple sentence fragments
- Producing consistent data for downstream recommendation, visualization,
  or LLM prompting
- Bridging raw textual input with color-aware representations

Core Function:
--------------
- `aggregate_color_phrase_results()`:
    Orchestrates phrase-level parsing over multiple segments and aggregates:
    - All matched color names
    - Simplified descriptive phrases
    - RGB value mappings for matched terms

Example Usage:
--------------
>>> segments = ["soft pink shade", "maybe something like muted coral"]
>>> tones, phrases, rgb = aggregate_color_phrase_results(
        segments, known_tones, known_modifiers, rgb_lookup_map
    )

Dependencies:
-------------
- process_segment_colors (called internally)
- known_tones / known_modifiers vocabularies
- RGB color mapping dictionary
"""
from typing import List, Set, Dict, Tuple


def aggregate_color_phrase_results(
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Tuple[Set[str], List[str], Dict[str, Tuple[int, int, int]]]:
    """
    Aggregates simplified color parsing outputs from multiple input segments.

    For each text segment, this function:
    - Extracts matched color names
    - Extracts simplified descriptive phrases
    - Maps each phrase to its RGB triplet (if known)

    Args:
        segments (List[str]): User-generated text segments.
        known_tones (Set[str]): Recognized tone names.
        known_modifiers (Set[str]): Recognized modifiers.
        rgb_map (Dict[str, Tuple[int, int, int]]): Color name → RGB value map.

    Returns:
        Tuple:
            - Set[str]: All matched color names across all segments
            - List[str]: All simplified phrases extracted
            - Dict[str, RGB]: Mapping from phrase → RGB tuple

    Example:
        >>> aggregate_color_phrase_results(["soft pink", "muted coral"], tones, mods, rgb_map)
        ({"pink", "coral"}, ["soft pink", "muted coral"], {"soft pink": (255,182,193)})
    """
    all_names = set()
    simplified = []
    rgb_map_ = {}

    for seg in segments:
        result = process_segment_colors(seg, known_tones, known_modifiers, rgb_map)
        all_names.update(result["matched_names"])
        simplified.extend(result["simplified"])
        rgb_map_.update(result["rgb_map"])

    return all_names, simplified, rgb_map_


def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool = False
) -> List[str]:
    """
    Aggregates all descriptive color phrases from raw user input.

    This function orchestrates the full rule-based color extraction pipeline,
    combining compound detection, standalone modifiers/tones, noun-based tones,
    and suffix-based fallback strategies into a single normalized list of results.

    Extraction Layers:
    ------------------
    - Modifier + tone compounds (e.g., "muted pink")
    - Standalone tones/modifiers (e.g., "pink", "soft")
    - Lone noun-based tones not part of any compound
    - Tokens with tone suffixes (e.g., "peachy", "rosy", "bluish")

    Args:
        text (str): Raw user-provided description (e.g., "I love dusty rose blush").
        known_tones (Set[str]): Full tone vocabulary (CSS3 + XKCD + fallbacks).
        known_modifiers (Set[str]): Valid modifier terms from curated set.
        all_webcolor_names (Set[str]): CSS/XKCD color names (for safety filtering).
        debug (bool): If True, prints verbose debug output for tracing.

    Returns:
        List[str]: Unique, sorted, lowercase list of extracted color phrases.

    Example:
    --------
    >>> extract_all_descriptive_color_phrases("muted rose and peachy tones", known_tones, known_modifiers, all_webcolor_names)
    ['muted rose', 'peachy', 'rose']
    """
    tokens, token_counts = tokenize_text(text)
    blocked_nouns = {"lipstick", "blush"}

    compounds, raw_compounds = extract_compound_phrases(
        tokens, known_tones, known_modifiers, all_webcolor_names, debug
    )
    singles = extract_standalone_phrases(
        tokens, token_counts, compounds, raw_compounds,
        known_tones, known_modifiers, all_webcolor_names, blocked_nouns, debug
    )
    lone_tones = extract_lone_tones(tokens, raw_compounds, known_tones, blocked_nouns, debug)
    suffix_tokens = extract_suffix_fallbacks(tokens, known_tones, known_modifiers, all_webcolor_names, debug)

    phrases = sorted(set(compounds) | set(singles) | set(lone_tones) | set(suffix_tokens))

    if debug:
        print(f"[✅ FINAL PHRASES] {phrases}")

    return phrases

def extract_phrases_from_segment(segment: str, known_modifiers: Set[str]) -> List[str]:
    """
    Extracts descriptive color phrases from a single segment using preloaded vocabularies.

    This is a convenience wrapper around `extract_all_descriptive_color_phrases`
    that injects global tone and webcolor vocabularies. Useful for sentiment processors,
    RGB matchers, or context analyzers where only modifiers vary.

    Args:
        segment (str): Text segment from user input (e.g., "I love soft peach shades").
        known_modifiers (Set[str]): Modifier vocabulary to apply (e.g., {"soft", "bold"}).

    Returns:
        List[str]: List of extracted compound or tone phrases.
    """
    return extract_all_descriptive_color_phrases(
        text=segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=all_webcolor_names,
        debug=False
    )
