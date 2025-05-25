import logging
import webcolors
from typing import Dict, List, Set, Any
from matplotlib.colors import CSS4_COLORS, XKCD_COLORS

from Chatbot.extractors.sentiment import (
    contains_sentiment_splitter_with_segments,
    classify_segments_by_sentiment_no_neutral,
)
from Chatbot.extractors.colors import (
    extract_all_descriptive_color_phrases,
    categorize_color_tokens_with_mapping,
    simplify_color_description_with_llm,
    fuzzy_match_modifier,
)
from Chatbot.scripts.RGB import (
    get_rgb_from_descriptive_color_llm_first,
    find_similar_color_names,
)
from Chatbot.scripts.cache import (
    get_cached_rgb, store_rgb_to_cache,
    get_cached_simplified, store_simplified_to_cache,
    load_cache_from_file, save_cache_to_file
)

# ──────────────────────────────────────────────────────────
# LOGGER SETUP
# ──────────────────────────────────────────────────────────
logger = logging.getLogger("ColorPipeline")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

load_cache_from_file()

# ──────────────────────────────────────────────────────────
# I. SENTIMENT CLASSIFICATION
# ──────────────────────────────────────────────────────────
def run_sentiment_classification(text: str) -> Dict[str, List[str]]:
    has_splitter, segments = contains_sentiment_splitter_with_segments(text)
    return classify_segments_by_sentiment_no_neutral(has_splitter, segments)

# ──────────────────────────────────────────────────────────
# II. PHRASE EXTRACTION
# ──────────────────────────────────────────────────────────
def process_segment_phrases(segment: str, known_tones: Set[str], known_modifiers: Set[str]) -> List[str]:
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=set(webcolors.CSS3_NAMES_TO_HEX.keys())

    )


# ──────────────────────────────────────────────────────────
# III. RGB RESOLUTION
# ──────────────────────────────────────────────────────────
def resolve_rgb(phrase: str, sentiment: str, rgb_map: Dict[str, tuple], base_rgb_by_sentiment: Dict[str, tuple]):
    logger.debug(f"[🧪 resolve_rgb()] Checking RGB for '{phrase}'")
    cached = get_cached_rgb(phrase)
    if cached:
        logger.debug(f"[💾 RGB CACHE HIT] '{phrase}' → {cached}")
        rgb = cached
    else:
        logger.debug(f"[🚨 RGB CACHE MISS] '{phrase}' — triggering LLM")
        rgb = get_rgb_from_descriptive_color_llm_first(phrase)
        if rgb:
            logger.debug(f"[🧠 RGB FROM LLM] '{phrase}' → {rgb}")
            store_rgb_to_cache(phrase, rgb)
        else:
            logger.warning(f"[⚠️ RGB LLM FAILED] '{phrase}'")

    if rgb and sentiment not in base_rgb_by_sentiment:
        base_rgb_by_sentiment[sentiment] = rgb
        logger.debug(f"[✅ RGB REGISTERED] for {sentiment}: {rgb}")
    return rgb

def get_similar_colors(rgb, rgb_map):
    return find_similar_color_names(rgb, rgb_map) if rgb else []

# ──────────────────────────────────────────────────────────
# IV. SIMPLIFICATION
# ──────────────────────────────────────────────────────────
def simplify_if_needed(phrase: str) -> List[str]:
    logger.debug(f"[🧪 Simplify Check] → {phrase}")
    cached = get_cached_simplified(phrase)
    if cached:
        logger.debug(f"[💾 SIMPLIFY CACHE HIT] → {phrase} → {cached}")
        return cached
    simplified = simplify_color_description_with_llm(phrase)
    if simplified:
        logger.debug(f"[🧠 SIMPLIFIED VIA LLM] → {phrase} → {simplified}")
        store_simplified_to_cache(phrase, simplified)
    else:
        logger.warning(f"[⚠️ SIMPLIFY FAILED] → {phrase}")
    return simplified

# ──────────────────────────────────────────────────────────
# V. CATEGORIZATION
# ──────────────────────────────────────────────────────────
def clean_and_categorize(phrases: List[str], known_modifiers: Set[str], known_tones: Set[str]) -> Dict[str, List[str]]:
    cleaned = []
    for p in phrases:
        tokens = p.lower().split()
        if len(tokens) == 2:
            mod, tone = tokens
            mod_fixed = fuzzy_match_modifier(mod, known_modifiers) or mod
            cleaned.append(f"{mod_fixed} {tone}")
        else:
            cleaned.append(p)
    return categorize_color_tokens_with_mapping(cleaned, known_tones, known_modifiers)

# ──────────────────────────────────────────────────────────
# VI. SENTIMENT HANDLER
# ──────────────────────────────────────────────────────────
def build_sentiment_output(
    sentiment: str,
    segments: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, tuple],
    base_rgb_by_sentiment: Dict[str, tuple]
) -> Dict[str, object]:
    logger.debug(f"[🧪 SENTIMENT BLOCK] → {sentiment.upper()}")
    all_color_names = set()
    simplified_phrases = []

    for seg in segments:
        logger.debug(f"[🧾 SEGMENT] → {seg}")
        try:
            phrases = process_segment_phrases(seg, known_tones, known_modifiers)
            logger.debug(f"[🎯 EXTRACTED PHRASES] {phrases}")
        except Exception as e:
            logger.warning(f"[⚠️ SEGMENT FAIL] '{seg}' → {e}")
            continue

        for phrase in phrases:
            logger.debug(f"[⚙️ PHRASE] → {phrase}")
            try:
                rgb = resolve_rgb(phrase, sentiment, rgb_map, base_rgb_by_sentiment)
                logger.debug(f"[🎨 RGB RESOLVED] → {rgb}")
                matches = get_similar_colors(rgb, rgb_map)
                logger.debug(f"[🎯 COLOR MATCHES] {matches}")
                all_color_names.update(matches)

                if not rgb:
                    simplified = simplify_if_needed(phrase)
                    simplified_phrases.extend(simplified)
                elif phrase in known_tones:
                    simplified_phrases.append(phrase)

            except Exception as e:
                logger.error(f"[❌ PHRASE ERROR] '{phrase}' → {e}")

    logger.debug(f"[🧹 SIMPLIFIED PHRASES] → {simplified_phrases}")
    categories = clean_and_categorize(simplified_phrases, known_modifiers, known_tones)

    result = {
        "matched_color_names": sorted(all_color_names),
        "base_rgb": base_rgb_by_sentiment.get(sentiment),
        "threshold": 60.0,
    }

    logger.debug(f"[📦 FINAL SENTIMENT OUTPUT] → {sentiment.upper()}")
    logger.debug(result)
    return result

# ──────────────────────────────────────────────────────────
# VII. PIPELINE ENTRY POINT
# ──────────────────────────────────────────────────────────
def extract_color_pipeline(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, tuple] = None
) -> dict[str, dict[Any, Any]] | dict[str, dict[str, object]]:
    logger.info(f"[🎤 INPUT TEXT] → {text}")
    rgb_map = rgb_map or {
        name: webcolors.hex_to_rgb(value)
        for name, value in {**CSS4_COLORS, **XKCD_COLORS}.items()
    }

    try:
        sentiment_segments = run_sentiment_classification(text)
        logger.debug(f"[🧠 SENTIMENT CLASSIFICATION] → {sentiment_segments}")
    except Exception as e:
        logger.error(f"[❌ SENTIMENT ERROR] → {e}")
        return {"positive": {}, "negative": {}}

    base_rgb_by_sentiment = {}

    output = {
        sentiment: build_sentiment_output(
            sentiment,
            sentiment_segments[sentiment],
            known_tones,
            known_modifiers,
            rgb_map,
            base_rgb_by_sentiment
        )
        for sentiment in ["positive", "negative"]
    }

    import json
    logger.debug("[✅ FINAL OUTPUT STRUCTURE]")
    logger.debug(json.dumps(output, indent=2))

    # Remove any matched_color_names in negative from the positive set
    pos_set = set(output["positive"]["matched_color_names"])
    neg_set = set(output["negative"]["matched_color_names"])

    # True exclusion: if a color is explicitly part of negative → remove it from positive
    cleaned_pos = sorted(list(pos_set - neg_set))
    output["positive"]["matched_color_names"] = cleaned_pos
    # If nothing remains in positive, clear its base_rgb too
    if not cleaned_pos:
        output["positive"]["base_rgb"] = None

    return output
