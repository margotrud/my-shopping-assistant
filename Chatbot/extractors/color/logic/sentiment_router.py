"""
sentiment_router.py
====================

Sentiment-based aggregation logic for color extraction.

This module provides the bridge between sentiment classification and
color interpretation. It collects all descriptive segments tagged with a
sentiment (e.g., "positive") and builds a color-centric summary from them.

This summary includes:
- All matched color names
- Simplified color phrases
- A representative RGB for visualization
- A fixed threshold for color distance filtering

Main Use Case:
--------------
Used after the user's input is parsed into sentiment-tagged segments.
Each group is then passed to this module to generate interpretable
color outputs tied to user sentiment.

Core Function:
--------------
- `build_color_sentiment_summary()`

Dependencies:
-------------
- `aggregate_color_phrase_results()` from phrase_aggregator.py
- `choose_representative_rgb()` from rgb_distance.py
- `format_tone_modifier_mappings()` for tone/modifier enrichment
"""

from typing import List, Set, Dict, Tuple, Optional, Union
from Chatbot.extractors.color.extraction.phrase_aggregator import aggregate_color_phrase_results
from Chatbot.extractors.color.utils.rgb_distance import choose_representative_rgb
from Chatbot.extractors.color.logic.color_categorizer import format_tone_modifier_mappings

import logging
logger = logging.getLogger(__name__)


def build_color_sentiment_summary(
    sentiment: str,
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]],
    base_rgb_by_sentiment: Dict[str, Optional[Tuple[int, int, int]]]
) -> Dict[str, Union[List[str], Optional[Tuple[int, int, int]], float]]:
    """
    Builds a color interpretation summary for a given sentiment cluster.

    For all user input segments labeled with a particular sentiment (e.g., "positive"),
    this function:
    - Extracts and simplifies color phrases
    - Resolves known color names and RGB values
    - Chooses a representative RGB to represent the cluster

    Args:
        sentiment (str): Sentiment label (e.g., "positive").
        segments (List[str]): All user input segments tagged with that sentiment.
        known_tones (Set[str]): Valid color tone names.
        known_modifiers (Set[str]): Valid modifier tokens.
        rgb_map (Dict[str, RGB]): Color name → RGB lookup table.
        base_rgb_by_sentiment (Dict[str, Optional[RGB]]): Storage dict for the output RGB per sentiment.

    Returns:
        Dict[str, object]:
            - "matched_color_names": Sorted list of matched color terms
            - "base_rgb": A single RGB tuple representing the sentiment (or None)
            - "threshold": Fixed color similarity threshold for downstream filters

    Example:
        >>> build_color_sentiment_summary("positive", ["soft pink", "muted rose"], ...)
        {
            "matched_color_names": ["pink", "rose"],
            "base_rgb": (255,182,193),
            "threshold": 60.0
        }
    """
    all_color_names, simplified_phrases, phrase_rgb_map = aggregate_color_phrase_results(
        segments, known_tones, known_modifiers, rgb_map
    )

    # Optional enrichment: generate tone/modifier maps for logging or caching
    format_tone_modifier_mappings(simplified_phrases, known_tones, known_modifiers)

    rep_rgb = choose_representative_rgb(phrase_rgb_map)
    base_rgb_by_sentiment[sentiment] = rep_rgb

    logger.debug(f"[🎨 SENTIMENT COLOR] '{sentiment}' → RGB: {rep_rgb}")
    logger.debug(f"[📦 COLOR COUNT] '{sentiment}' → Matches: {len(all_color_names)}")

    return {
        "matched_color_names": sorted(all_color_names),
        "base_rgb": rep_rgb,
        "threshold": 60.0,
    }
