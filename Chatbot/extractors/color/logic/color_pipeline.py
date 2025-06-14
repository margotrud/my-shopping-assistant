"""
color_pipeline.py
==================

Color Phrase Interpretation Pipeline
------------------------------------

This module orchestrates multi-step processing for descriptive color inputs.
It serves as the main coordination layer that links LLM resolution, RGB mapping,
phrase simplification, and similarity-based color name detection.

Key Responsibilities:
---------------------
- Convert abstract color phrases (e.g., "muted rosy nude") into usable RGB values
- Find similar or standardized color names based on RGB proximity
- Simplify verbose or non-standard phrases for fallback attempts
- Output structured representations usable by recommender engines or UI

Used By:
--------
- Segment-level processing modules (e.g., `aggregate_color_phrase_results`)
- Sentiment-aware pipelines (e.g., `build_color_sentiment_summary`)
- LLM prompting logic and visual previews

Included Functions:
-------------------
- `process_color_phrase`: Handles RGB lookup + fallback for a single phrase
- (Planned) functions for batch phrase resolution, color set scoring, and distance ranking

Dependencies:
-------------
- LLM resolution layer (`llm_rgb`)
- Phrase simplifier (`llm_simplifier`)
- Color name matching via RGB distance (`color_name_matcher`)
- RGB maps from `shared/vocab.py`

Example:
--------
>>> process_color_phrase("dusty rose", known_tones, rgb_lookup)
(
    {"rose", "pink"},
    ["dusty rose", "dusty", "rose"],
    {"dusty rose": (188, 143, 143)}
)
"""


from typing import Tuple, Set, List, Dict
from Chatbot.extractors.color.llm.llm_rgb import get_rgb_from_descriptive_color_llm_first
from Chatbot.extractors.color.logic.color_name_matcher import find_similar_color_names
from Chatbot.extractors.color.llm.llm_simplifier import simplify_phrase_if_needed

import spacy
nlp = spacy.load("en_core_web_sm")

def process_color_phrase(
    phrase: str,
    known_tones: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Tuple[Set[str], List[str], Dict[str, Tuple[int, int, int]]]:
    """
    Resolves a color phrase into color name matches, simplified forms, and RGB values.

    This function:
    - Resolves the input phrase via LLM to an RGB tuple
    - Matches that RGB to known color names via similarity
    - Attempts simplification and re-resolution if needed

    Args:
        phrase (str): Descriptive input (e.g., "rosy nude").
        known_tones (Set[str]): Known tone vocabulary (used for tagging).
        rgb_map (Dict[str, RGB]): Mapping from known color names to RGB tuples.

    Returns:
        Tuple:
            - matched_names (Set[str]): Similar known color names (e.g., {"pink", "coral"})
            - simplified_phrases (List[str]): Phrase variants or simplified forms
            - phrase_rgb_map (Dict[str, RGB]): Mapping of resolved phrases to RGB

    Example:
        >>> process_color_phrase("rosy nude", known_tones, rgb_map)
        ({"nude", "peach"}, ["rosy nude", "rosy", "nude"], {"rosy nude": (222,180,190)})
    """
    matched_names = set()
    simplified_phrases = []
    phrase_rgb_map = {}

    # ─── Step 1: Resolve main phrase
    rgb = get_rgb_from_descriptive_color_llm_first(phrase)

    if rgb:
        phrase_rgb_map[phrase] = rgb
        matches = find_similar_color_names(rgb, rgb_map) or [phrase]
        matched_names.update(matches)

        simplified = simplify_phrase_if_needed(phrase)
        simplified_phrases.extend(simplified)

        if phrase in known_tones and phrase not in simplified_phrases:
            simplified_phrases.append(phrase)

    else:
        # ─── Step 2: Fallback to simplifications
        simplified = simplify_phrase_if_needed(phrase)
        simplified_phrases.extend(simplified)

        for simplified_phrase in simplified:
            fallback_rgb = get_rgb_from_descriptive_color_llm_first(simplified_phrase)
            if fallback_rgb:
                phrase_rgb_map[simplified_phrase] = fallback_rgb
                matches = find_similar_color_names(fallback_rgb, rgb_map)
                matched_names.update(matches)
                break  # stop at first success

    return matched_names, simplified_phrases, phrase_rgb_map


def process_segment_colors(
    segment: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Dict[str, object]:
    """
    Orchestrates full color extraction for a single text segment.

    This function identifies descriptive color phrases within the input,
    resolves their RGB values, finds similar known color names, and
    simplifies the phrases where possible.

    Also performs a secondary fallback resolution step using tone-only logic
    for cases where compound phrases are not matched.

    Args:
        segment (str): Raw user text (e.g., "I love soft dusty pinks").
        known_tones (Set[str]): Recognized base tone vocabulary.
        known_modifiers (Set[str]): List of approved modifiers.
        rgb_map (Dict[str, RGB]): Mapping from standard color names to RGB values.

    Returns:
        Dict[str, object]: A dictionary containing:
            - "matched_names" (Set[str]): All matched known color names.
            - "simplified" (List[str]): Simplified color phrases.
            - "rgb_map" (Dict[str, RGB]): Phrase → RGB mapping for downstream use.

    Example:
        >>> process_segment_colors("I love dusty rose and muted nude", ...)
        {
            "matched_names": {"rose", "nude"},
            "simplified": ["dusty rose", "muted nude"],
            "rgb_map": {
                "dusty rose": (188, 143, 143),
                "muted nude": (224, 182, 170)
            }
        }
    """

    matched_names = set()
    simplified_phrases = []
    phrase_rgb_map = {}

    # Extract descriptive color phrases from the segment
    phrases = extract_phrases_from_segment(segment, known_modifiers)
    seen_phrases = set(phrases)

    for phrase in phrases:
        names, simplified, rgb_map_ = process_color_phrase(phrase, known_tones, rgb_map)
        matched_names.update(names)
        simplified_phrases.extend(simplified)
        phrase_rgb_map.update(rgb_map_)

    # Resolve fallback tokens that were not captured by phrase extraction
    fallback_matches = resolve_fallback_tokens(segment, seen_phrases, known_tones, rgb_map)
    matched_names.update(fallback_matches)

    return {
        "matched_names": matched_names,
        "simplified": simplified_phrases,
        "rgb_map": phrase_rgb_map
    }

def resolve_fallback_tokens(
    segment: str,
    seen_phrases: Set[str],
    known_tones: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> List[str]:
    """
    Resolves color tokens not previously captured by phrase extraction.

    This function analyzes a text segment token by token to identify additional
    color-relevant words that might not have been grouped into phrases. It then
    attempts to resolve each one to an RGB value using an LLM, and finds similar
    known color names using RGB distance matching.

    Args:
        segment (str): Full user input sentence (e.g., "maybe something coral").
        seen_phrases (Set[str]): Phrases already processed (e.g., {"muted peach"}).
        known_tones (Set[str]): Known tone names (not used directly, but available).
        rgb_map (Dict[str, Tuple[int, int, int]]): Mapping from standard color names to RGB.

    Returns:
        List[str]: List of matched known color names based on uncovered tokens.

    Example:
        >>> resolve_fallback_tokens("maybe something coral", {"soft peach"}, known_tones, rgb_map)
        ["coral"]
    """
    matches = []
    doc = nlp(segment.lower())

    for token in doc:
        candidate = token.text.lower()

        if (
            candidate not in seen_phrases
            and token.pos_ in {"NOUN", "ADJ"}
            and token.is_alpha
            and len(candidate) <= 20
        ):
            rgb = get_rgb_from_descriptive_color_llm_first(candidate)
            if rgb:
                similar_colors = find_similar_color_names(rgb, rgb_map)
                matches.extend(similar_colors)

    return matches


def extract_from_glued(
    tokens,
    compounds,
    raw_compounds,
    token_texts,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    debug
):
    """
    Extracts compound color phrases from single glued tokens (e.g., "mutedrose").

    This function identifies cases where users enter modifier-tone combinations
    without spaces — a common occurrence in informal or fast-typed inputs.
    It attempts to split each token into valid color components using the
    `split_glued_tokens()` utility, then verifies both modifier and tone validity
    using known vocabularies.

    Duplicates are suppressed by checking:
    - If the normalized glued token was already extracted as a compound
    - If the original glued form was present in token texts (sanity check)

    Args:
        tokens (List[Token]): spaCy-parsed input tokens.
        compounds (Set[str]): Set for collecting final unique compound phrases.
        raw_compounds (List[str]): List to record all detected raw compound forms.
        token_texts (List[str]): List of original token text strings from input.
        known_color_tokens (Set[str]): Union of all known tones and modifiers.
        known_modifiers (Set[str]): Known modifier vocabulary.
        known_tones (Set[str]): Known tone vocabulary.
        all_webcolor_names (Set[str]): Web color names (CSS/XKCD).
        debug (bool): If True, enables detailed logging.

    Example:
        >>> token = "dustyrose"
        >>> split → ["dusty", "rose"]
        >>> resolve → "dusty rose"
    """
    for token in tokens:
        raw = singularize(token.text.lower())

        # Avoid reprocessing if the glued form was already extracted
        if any(raw in c.replace(" ", "") for c in compounds):
            if debug:
                print(f"[⛔ SKIPPED GLUED TOKEN] '{raw}' already detected")
            continue

        parts = split_glued_tokens(raw, known_color_tokens)
        if debug:
            print(f"[🔬 SPLIT GLUED TOKEN] '{raw}' → {parts}")
        if len(parts) != 2:
            continue

        mod_candidate, tone_candidate = parts
        mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers, known_tones)
        is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names
        original_form = mod_candidate + tone_candidate

        if mod and is_valid and original_form in token_texts:
            compound = f"{mod} {tone_candidate}"
            compounds.add(compound)
            raw_compounds.append(compound)
            if debug:
                print(f"[✅ GLUED COMPOUND] '{raw}' → '{compound}'")
        elif debug:
            print(f"[⛔ REJECTED GLUED COMPOUND] '{raw}' not valid")
