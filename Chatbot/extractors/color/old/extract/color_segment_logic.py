# Chatbot/extractors/color/extract/color_segment_logic.py

"""
Color Segment Logic
--------------------
Module responsible for processing user input text segments associated with
a specific sentiment category (e.g., "positive", "negative") by:

- Extracting descriptive color phrases from each text segment
- Resolving RGB color values for each phrase, including fallbacks
- Simplifying complex or ambiguous phrases using LLM
- Matching fallback tokens not directly extracted as phrases

This module returns structured results with matched color names,
their representative RGB values, and relevant mappings for further processing.
"""

import spacy
import logging
from typing import List, Set, Dict, Tuple, Optional, Union

from Chatbot.extractors.color.old.extract import extract_phrases_from_segment
from Chatbot.extractors.color.simplifier import simplify_phrase_if_needed
from Chatbot.extractors.color.old.extract import clean_and_categorize
from Chatbot.extractors.color.old.core import get_rgb_from_descriptive_color_llm_first
from Chatbot.extractors.color.old.core import find_similar_color_names
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token

logger = logging.getLogger("ColorPipeline")
nlp = spacy.load("en_core_web_sm")


def aggregate_results(
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Tuple[Set[str], List[str], Dict[str, Tuple[int, int, int]]]:
    """
    Processes each segment to collect matched color names, simplified phrases, and RGB mappings.

    Args:
        segments: List of text segments to process.
        known_tones: Set of known tones.
        known_modifiers: Set of known modifiers.
        rgb_map: Mapping from color names to RGB tuples.

    Returns:
        A tuple of:
            - set of matched color names,
            - list of simplified phrases,
            - dict mapping phrases to RGB tuples.
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


def choose_representative_rgb(
    rgb_mapping: Dict[str, Tuple[int, int, int]]
) -> Optional[Tuple[int, int, int]]:
    """
    Selects a representative RGB from the phrase-to-RGB map.

    Args:
        rgb_mapping: Dictionary mapping phrases to RGB tuples.

    Returns:
        The first RGB tuple found or None if empty.
    """
    return next(iter(rgb_mapping.values()), None)


def build_sentiment_output(
    sentiment: str,
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]],
    base_rgb_by_sentiment: Dict[str, Optional[Tuple[int, int, int]]]
) -> Dict[str, Union[List[str], Optional[Tuple[int, int, int]], float]]:
    """
    Processes all text segments associated with a given sentiment.

    For each segment, extracts color phrases, resolves their RGB values
    (with fallback strategies), simplifies phrases, and aggregates results.

    Args:
        sentiment (str): Sentiment category label ("positive" or "negative").
        segments (List[str]): List of text segments to process.
        known_tones (Set[str]): Known base color tones vocabulary.
        known_modifiers (Set[str]): Known color modifiers vocabulary.
        rgb_map (Dict[str, Tuple[int, int, int]]): Lookup mapping from color names to RGB tuples.
        base_rgb_by_sentiment (Dict[str, Optional[Tuple[int, int, int]]]): Mutable dict to store representative RGB per sentiment.

    Returns:
        Dict[str, object]: Dictionary containing:
            - "matched_color_names" (List[str]): Sorted unique color names matched.
            - "base_rgb" (Optional[Tuple[int, int, int]]): Representative RGB value or None.
            - "threshold" (float): Fixed threshold for color similarity (e.g., 60.0).
    """
    all_color_names, simplified_phrases, phrase_rgb_map = aggregate_results(
        segments, known_tones, known_modifiers, rgb_map
    )

    # Categorize the simplified phrases into tones/modifiers for later logic (side-effect)
    clean_and_categorize(simplified_phrases, known_modifiers, known_tones)

    rep_rgb = choose_representative_rgb(phrase_rgb_map)
    base_rgb_by_sentiment[sentiment] = rep_rgb

    logger.debug(f"[DEBUG] Sentiment '{sentiment}' representative RGB: {rep_rgb}")
    logger.debug(f"[DEBUG] Sentiment '{sentiment}' matched names count: {len(all_color_names)}")

    return {
        "matched_color_names": sorted(all_color_names),
        "base_rgb": rep_rgb,
        "threshold": 60.0,
    }


def resolve_phrase_rgb_with_fallback(
    phrase: str,
    known_tones: Set[str]
) -> Optional[Tuple[int, int, int]]:
    """
    Resolves the RGB value for a phrase using the LLM-based simplification and fallback.

    Args:
        phrase (str): The color phrase to resolve.
        known_tones (Set[str]): Set of valid tones for context (not used here).

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple if resolved, else None.
    """
    return get_rgb_from_descriptive_color_llm_first(phrase)


def process_color_phrase(
    phrase: str,
    known_tones: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Tuple[Set[str], List[str], Dict[str, Tuple[int, int, int]]]:
    """
    Processes a single color phrase to find matching color names, simplified forms,
    and phrase-to-RGB mappings.

    Args:
        phrase (str): The color phrase.
        known_tones (Set[str]): Known tones vocabulary.
        rgb_map (Dict[str, Tuple[int, int, int]]): Mapping of color names to RGB.

    Returns:
        Tuple containing:
            - matched_names (Set[str]): Similar matched color names.
            - simplified_phrases (List[str]): Simplified forms.
            - phrase_rgb_map (Dict[str, Tuple[int, int, int]]): Phrase to RGB mapping.
    """
    matched_names = set()
    simplified_phrases = []
    phrase_rgb_map = {}

    # Primary RGB resolution
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
        # Fallback: try to simplify first, then re-resolve
        simplified = simplify_phrase_if_needed(phrase)
        simplified_phrases.extend(simplified)

        for simplified_phrase in simplified:
            fallback_rgb = get_rgb_from_descriptive_color_llm_first(simplified_phrase)
            if fallback_rgb:
                phrase_rgb_map[simplified_phrase] = fallback_rgb
                matches = find_similar_color_names(fallback_rgb, rgb_map)
                matched_names.update(matches)
                break  # stop after first success

    return matched_names, simplified_phrases, phrase_rgb_map


def process_segment_colors(
    segment: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Dict[str, object]:
    """
    Processes a single text segment to identify color-related tokens,
    resolve RGB values, simplify phrases, and find fallback matches.

    Args:
        segment (str): Text segment to analyze.
        known_tones (Set[str]): Known base color tones.
        known_modifiers (Set[str]): Known color modifiers.
        rgb_map (Dict[str, Tuple[int, int, int]]): Color name to RGB mapping.

    Returns:
        Dict[str, object]: Contains:
            - "matched_names" (Set[str]): Unique matched color names.
            - "simplified" (List[str]): Simplified color phrases.
            - "rgb_map" (Dict[str, Tuple[int, int, int]]): Phrase to RGB mappings.
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
    Identifies additional color tokens within the segment not extracted initially,
    resolves their RGB values, and returns matching color names.

    Args:
        segment (str): Text segment to analyze.
        seen_phrases (Set[str]): Phrases already processed.
        known_tones (Set[str]): Known base color tones.
        rgb_map (Dict[str, Tuple[int, int, int]]): Color name to RGB mapping.

    Returns:
        List[str]: List of matched color names from fallback tokens.
    """
    matches = []
    doc = nlp(segment.lower())

    for token in doc:
        candidate = normalize_token(token.text)

        if (
            candidate not in seen_phrases and
            token.pos_ in {"NOUN", "ADJ"} and
            token.is_alpha and
            len(candidate) <= 20
        ):
            rgb = get_rgb_from_descriptive_color_llm_first(candidate)
            if rgb:
                similar_colors = find_similar_color_names(rgb, rgb_map)
                matches.extend(similar_colors)

    return matches

