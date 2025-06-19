#Chatbot/pipelines/color_extractors.py
"""
Color Extraction Pipeline
--------------------------
This is the main entry point for extracting colors from user input.
It classifies sentiment, processes each segment, resolves colors,
and applies conflict resolution.
"""

import logging
import json
import webcolors
from matplotlib.colors import CSS4_COLORS, XKCD_COLORS
from typing import Set, Dict, Any, Tuple

from Chatbot.extractors.general.old.sentiment import (contains_sentiment_splitter_with_segments,
                                                      classify_segments_by_sentiment_no_neutral)

from Chatbot.extractors.color.old.extract import build_sentiment_output
from Chatbot.extractors.color.extractor import resolve_color_conflicts

from Chatbot.cache.llm_cache import load_cache_from_file

# ──────────────────────────────────────────────────────────
# LOGGER
# ──────────────────────────────────────────────────────────
logger = logging.getLogger("ColorPipeline")
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

load_cache_from_file()

# ──────────────────────────────────────────────────────────
# PIPELINE ENTRY POINT
# ──────────────────────────────────────────────────────────
def extract_color_pipeline(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, Tuple[int, int, int]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Extracts sentiment-aware color information from user input.

    Args:
        text (str): User message (e.g., "I like cherry but not bright red")
        known_tones (Set[str]): Set of base color tones
        known_modifiers (Set[str]): Set of known color modifiers
        rgb_map (Dict[str, Tuple[int, int, int]]): Color → RGB lookup table

    Returns:
        Dict[str, Dict[str, Any]]: {
            "positive": {
                "matched_color_names": [...],
                "base_rgb": (r, g, b) or None,
                "threshold": float
            },
            "negative": {...}
        }
    """
    logger.info(f"[🎤 INPUT TEXT] → {text}")

    rgb_map = rgb_map or {
        name: webcolors.hex_to_rgb(value)
        for name, value in {**CSS4_COLORS, **XKCD_COLORS}.items()
    }

    has_splitter, segments = contains_sentiment_splitter_with_segments(text)
    sentiment_segments = classify_segments_by_sentiment_no_neutral(has_splitter, segments)

    # Ensure both blocks are present
    sentiment_segments.setdefault("positive", [])
    sentiment_segments.setdefault("negative", [])

    base_rgb_by_sentiment = {}

    output = {
        sentiment: build_sentiment_output(
            sentiment=sentiment,
            segments=segments,
            known_tones=known_tones,
            known_modifiers=known_modifiers,
            rgb_map=rgb_map,
            base_rgb_by_sentiment=base_rgb_by_sentiment
        )
        for sentiment, segments in sentiment_segments.items()
    }

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
