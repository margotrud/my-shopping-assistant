# Chatbot/extractors/color/extractor.py
"""
Color Extraction Pipeline
-------------------------
Main entry point for extracting color preferences from user input text
with sentiment awareness. This module orchestrates:

- Splitting input text into sentiment-tagged segments
- Extracting descriptive color phrases per segment
- Resolving RGB values for phrases via LLM and fuzzy matching
- Simplifying and categorizing extracted colors
- Resolving conflicts between positive and negative color preferences

This module is central to the shopping assistant's ability
to understand user color preferences contextually and accurately.
"""

import logging
import json
from typing import Set, Dict, Tuple, Any, List, Optional

import webcolors

from Chatbot.extractors.color.old.extract import extract_all_descriptive_color_phrases
from Chatbot.extractors.color.old.llm import simplify_color_description_with_llm
from Chatbot.extractors.color.old.extract import categorize_color_tokens_with_mapping
from Chatbot.extractors.color.old.core import (
    get_rgb_from_descriptive_color_llm_first,
    find_similar_color_names
)
from Chatbot.extractors.general.old.sentiment import (
    contains_sentiment_splitter_with_segments,
    classify_segments_by_sentiment_no_neutral
)
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token

logger = logging.getLogger("ColorPipeline")
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def initialize_rgb_map() -> Dict[str, Tuple[int, int, int]]:
    """
    Initialize and return a combined RGB color mapping from CSS4 and XKCD color sets.

    Returns:
        Dict[str, Tuple[int, int, int]]: Mapping of color names to RGB tuples.
    """
    return {
        name: webcolors.hex_to_rgb(value)
        for name, value in {**webcolors.CSS4_COLORS, **webcolors.XKCD_COLORS}.items()
    }


def segment_and_classify_text(text: str) -> Dict[str, List[str]]:
    """
    Splits input text into sentiment-labeled segments and classifies each as positive or negative.

    Args:
        text (str): Raw input string.

    Returns:
        Dict[str, List[str]]: Dictionary with keys 'positive' and 'negative' mapping to lists of text segments.
    """
    has_splitter, segments = contains_sentiment_splitter_with_segments(text)
    sentiment_segments = classify_segments_by_sentiment_no_neutral(has_splitter, segments)
    sentiment_segments.setdefault("positive", [])
    sentiment_segments.setdefault("negative", [])
    return sentiment_segments


def extract_color_pipeline(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Optional[Dict[str, Tuple[int, int, int]]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Extracts and analyzes color-related information from user input text.

    Args:
        text (str): Raw user input string.
        known_tones (Set[str]): Recognized base color tones.
        known_modifiers (Set[str]): Recognized color modifiers.
        rgb_map (Optional[Dict[str, Tuple[int, int, int]]]): Predefined color-to-RGB mapping.

    Returns:
        Dict[str, Dict[str, Any]]: Output keyed by 'positive' and 'negative' sentiment labels,
                                   each mapping to extraction results.
    """
    logger.info(f"[🎤 INPUT TEXT] → {text}")

    rgb_map = rgb_map or initialize_rgb_map()
    sentiment_segments = segment_and_classify_text(text)

    output = {}
    for sentiment in ["positive", "negative"]:
        output[sentiment] = build_sentiment_output(
            sentiment=sentiment,
            segments=sentiment_segments[sentiment],
            known_tones=known_tones,
            known_modifiers=known_modifiers,
            rgb_map=rgb_map
        )

    resolved = resolve_color_conflicts(
        positive=output["positive"]["matched_color_names"],
        negative=output["negative"]["matched_color_names"],
        known_tones=known_tones
    )

    output["positive"]["matched_color_names"] = resolved["positive"]
    output["negative"]["matched_color_names"] = resolved["negative"]

    if not resolved["positive"]:
        output["positive"]["base_rgb"] = None

    logger.debug("[✅ FINAL OUTPUT STRUCTURE]")
    logger.debug(json.dumps(output, indent=2))

    return output


def extract_phrases_from_segment_safe(
    segment: str,
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> List[str]:
    """
    Safely extracts descriptive color phrases from a segment, logging failures.

    Args:
        segment (str): Text segment to extract from.
        known_tones (Set[str]): Known base tones.
        known_modifiers (Set[str]): Known modifiers.

    Returns:
        List[str]: Extracted color phrases or empty list on error.
    """
    try:
        return extract_all_descriptive_color_phrases(
            segment,
            known_tones=known_tones,
            known_modifiers=known_modifiers,
            all_webcolor_names=set(webcolors.CSS3_NAMES_TO_HEX.keys())
        )
    except Exception as e:
        logger.warning(f"[⚠️ SEGMENT FAIL] '{segment}' → {e}")
        return []


def resolve_phrase_rgb_safe(phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Resolves RGB for a phrase using LLM, with error logging.

    Args:
        phrase (str): Color phrase.

    Returns:
        Optional[Tuple[int, int, int]]: RGB tuple or None.
    """
    try:
        return get_rgb_from_descriptive_color_llm_first(phrase)
    except Exception as e:
        logger.warning(f"[⚠️ RGB ERROR] '{phrase}' → {e}")
        return None


def process_phrase(
    phrase: str,
    rgb_map: Dict[str, Tuple[int, int, int]],
    known_modifiers: Set[str],
    known_tones: Set[str]
) -> Tuple[Set[str], List[str], Optional[Tuple[int, int, int]]]:
    """
    Processes a single color phrase: resolves RGB, finds similar colors, and simplifies it.

    Args:
        phrase (str): Color phrase.
        rgb_map (Dict[str, Tuple[int, int, int]]): Color to RGB mapping.
        known_modifiers (Set[str]): Known modifiers.
        known_tones (Set[str]): Known tones.

    Returns:
        Tuple containing:
            - matched color names (Set[str])
            - simplified phrases (List[str])
            - RGB tuple or None
    """
    matched_names = set()
    simplified_phrases = []

    rgb = resolve_phrase_rgb_safe(phrase)
    if rgb:
        matches = find_similar_color_names(rgb, rgb_map)
        if matches:
            matched_names.update(matches)
        else:
            matched_names.add(phrase)

        simplified = simplify_color_description_with_llm(phrase)
        if simplified:
            simplified_phrases.extend(simplified)
        else:
            simplified_phrases.append(phrase)

        return matched_names, simplified_phrases, rgb

    return set(), [], None


def build_sentiment_output(
    sentiment: str,
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]]
) -> Dict[str, Any]:
    """
    Processes all text segments for a single sentiment category.

    Extracts color phrases, resolves RGB values, simplifies phrases, and aggregates matches.

    Args:
        sentiment (str): Sentiment label ("positive" or "negative").
        segments (List[str]): Text segments labeled with the sentiment.
        known_tones (Set[str]): Recognized base color tones.
        known_modifiers (Set[str]): Recognized color modifiers.
        rgb_map (Dict[str, Tuple[int, int, int]]): Color name to RGB mapping.

    Returns:
        Dict[str, Any]: Contains:
            - "matched_color_names" (List[str]): Sorted list of matched color names.
            - "base_rgb" (Optional[Tuple[int, int, int]]): Representative RGB tuple or None.
            - "threshold" (float): Threshold for color similarity (fixed at 60.0).
    """
    all_color_names = set()
    simplified_phrases = []
    phrase_rgb_map = {}

    for segment in segments:
        phrases = extract_phrases_from_segment_safe(segment, known_tones, known_modifiers)
        seen_phrases = set(phrases)

        for phrase in phrases:
            matched_names, simplified, rgb = process_phrase(phrase, rgb_map, known_modifiers, known_tones)
            all_color_names.update(matched_names)
            simplified_phrases.extend(simplified)
            if rgb:
                phrase_rgb_map[phrase] = rgb

        # TODO: Implement fallback tokens if needed

    rep_rgb = next(iter(phrase_rgb_map.values()), None)

    # Categorize simplified phrases for downstream processing
    _ = categorize_color_tokens_with_mapping(simplified_phrases, known_modifiers, known_tones)

    return {
        "matched_color_names": sorted(all_color_names),
        "base_rgb": rep_rgb,
        "threshold": 60.0
    }


def resolve_color_conflicts(
    positive: List[str],
    negative: List[str],
    known_tones: Set[str]
) -> Dict[str, List[str]]:
    """
    Resolves conflicts between positive and negative color lists based on tone overlap.

    A color from the positive list is moved to the negative list if it shares any base tone
    with a color in the negative list, ensuring mutually exclusive tone groups.

    Args:
        positive (List[str]): Positive matched color names.
        negative (List[str]): Negative matched color names.
        known_tones (Set[str]): Recognized base tones.

    Returns:
        Dict[str, List[str]]: Cleaned positive and negative color lists with conflicts resolved.
    """

    def extract_tones(color_name: str) -> Set[str]:
        return {normalize_token(t) for t in color_name.split()} & known_tones

    positive_set = set(positive)
    negative_set = set(negative)
    conflict_colors = positive_set.intersection(negative_set)

    for neg_color in negative_set:
        neg_tones = extract_tones(neg_color)
        for pos_color in positive_set:
            pos_tones = extract_tones(pos_color)
            if neg_tones & pos_tones:
                conflict_colors.add(pos_color)

    cleaned_positive = sorted(positive_set - conflict_colors)
    cleaned_negative = sorted(negative_set | conflict_colors)

    return {
        "positive": cleaned_positive,
        "negative": cleaned_negative,
    }
