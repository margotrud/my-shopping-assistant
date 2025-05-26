# Chatbot/pipelines/color_extractors.py
import spacy
nlp = spacy.load("en_core_web_sm")

import logging
import webcolors
from typing import Dict, List, Set, Any
from matplotlib.colors import CSS4_COLORS, XKCD_COLORS
import json

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
def run_sentiment_classification(text: str) -> dict[str, list[str]]:
    has_splitter, segments = contains_sentiment_splitter_with_segments(text)

    classification = {
        "positive": [],
        "negative": []
    }

    try:
        raw_result = classify_segments_by_sentiment_no_neutral(has_splitter, segments)
        # In case the classifier returned None
        if raw_result is None:
            print(f"[❌ CLASSIFIER FAILED TO RETURN RESULT] → {text}")
            return classification
    except Exception as e:
        print(f"[❌ SENTIMENT ERROR] → {e}")
        return classification  # fail-safe fallback

    # Normalize 'neutral' into 'positive' if needed
    if "neutral" in raw_result:
        print(f"[⚠️ NEUTRAL → POSITIVE FALLBACK] → {raw_result}")
        raw_result["positive"] = raw_result.pop("neutral")

    # Safeguard return keys
    classification["positive"] = raw_result.get("positive", [])
    classification["negative"] = raw_result.get("negative", [])

    return classification


# ──────────────────────────────────────────────────────────
# II. PHRASE EXTRACTION
# ──────────────────────────────────────────────────────────
def process_segment_phrases(segment: str, known_tones: Set[str], known_modifiers: Set[str]) -> List[str]:
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=set(webcolors.CSS3_NAMES_TO_HEX.keys()),
        debug=True

    )


# ──────────────────────────────────────────────────────────
# III. RGB RESOLUTION
# ──────────────────────────────────────────────────────────


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
    phrase_rgb_map = {}

    logger.debug(f"[🧪 RAW SEGMENTS for sentiment={sentiment}] → {segments}")

    for seg in segments:
        logger.debug(f"[🧾 SEGMENT] → {seg}")
        try:
            phrases = process_segment_phrases(seg, known_tones, known_modifiers)
            logger.debug(f"[🟨 EXTRACTED PHRASES for SEGMENT] '{seg}' → {phrases}")
        except Exception as e:
            logger.warning(f"[⚠️ SEGMENT FAIL] '{seg}' → {e}")
            continue

        seen_phrases = set(phrases)

        for phrase in phrases:
            logger.debug(f"[🔍 PHRASE FROM EXTRACTOR] → {phrase}")
            logger.debug(f"[📌 DEBUG PHRASE PASSTHROUGH] → '{phrase}' (segment: '{seg}')")

            rgb = None
            try:
                cached = get_cached_rgb(phrase)
                if cached:
                    rgb = cached
                    logger.debug(f"[💾 CACHED RGB USED] {phrase} → {rgb}")
                else:
                    logger.debug(f"[🚀 LLM RGB CALL] for → '{phrase}'")
                    rgb = get_rgb_from_descriptive_color_llm_first(phrase)
                    if rgb:
                        logger.debug(f"[🎯 LLM RGB RESULT] {phrase} → {rgb}")
                        store_rgb_to_cache(phrase, rgb)
                    else:
                        # ✅ NEW: Try suffix-based fallback
                        if (phrase.endswith("y") or phrase.endswith("ish")) and len(phrase) > 3:
                            logger.debug(f"[🟠 SUFFIX FALLBACK TRIGGERED] → {phrase}")
                            for suffix in ["y", "ish"]:
                                if phrase.endswith(suffix):
                                    base = phrase[:-len(suffix)]
                                    logger.debug(f"[🟠 TRYING BASE] '{phrase}' → '{base}'")
                                    if base in known_tones:
                                        logger.debug(f"[🟠 BASE IS KNOWN TONE] '{base}' is a valid tone")
                                        try:
                                            rgb = get_rgb_from_descriptive_color_llm_first(base)
                                            if rgb:
                                                store_rgb_to_cache(phrase, rgb)
                                                logger.debug(f"[🎯 SUFFIX RGB RESOLVED] {phrase} → {rgb} (via '{base}')")
                                                break
                                            else:
                                                logger.warning(
                                                    f"[⚠️ SUFFIX RGB RESOLUTION FAILED] '{base}' returned no RGB")
                                        except Exception as sub_e:
                                            logger.warning(f"[⚠️ SUFFIX RGB FAIL] '{base}' → {sub_e}")
                                    else:
                                        logger.debug(f"[🔁 BASE NOT IN TONES] '{base}' is not in known tones")

                        if not rgb:
                            logger.warning(f"[⚠️ RGB NOT RESOLVED] {phrase} → Skipped from matched_color_names")
            except Exception as e:
                logger.warning(f"[⚠️ MAIN RGB ERROR] '{phrase}' → {e}")
                rgb = None

            if rgb:
                logger.debug(f"[🎨 RGB FINALIZED] Phrase: {phrase} → {rgb}")
                phrase_rgb_map[phrase] = rgb

                try:
                    matches = get_similar_colors(rgb, rgb_map)
                    logger.debug(f"[🎯 MATCHES FOR {phrase}] RGB: {rgb} → {matches}")
                    if matches:
                        all_color_names.update(matches)
                    else:
                        logger.debug(f"[🔁 FORCED ADD] RGB resolved but no matches found — manually adding '{phrase}'")
                        all_color_names.add(phrase)
                except StopIteration:
                    logger.warning(f"[🧨 MOCK EXHAUSTED] find_similar_color_names mock ran out — force-adding '{phrase}'")
                    all_color_names.add(phrase)

                simplified = simplify_if_needed(phrase)
                if not simplified:
                    logger.debug(f"[🪂 FALLBACK TO ORIGINAL] → {phrase}")
                    simplified = [phrase]

                simplified_phrases.extend(simplified)

                if phrase in known_tones and phrase not in simplified_phrases:
                    simplified_phrases.append(phrase)
            else:
                logger.warning(f"[⚠️ RGB NOT RESOLVED] Phrase: {phrase} → Skipped from matched_color_names")

        # Fallback RGB for missed color-like tokens (NOUN or ADJ)
        doc = nlp(seg.lower())
        for token in doc:
            candidate = token.text.lower()

            if (
                    candidate not in seen_phrases
                    and token.pos_ in {"NOUN", "ADJ"}
                    and token.is_alpha
                    and len(candidate) <= 20
            ):

                # Only proceed if known vocab or LLM confirms it's a color
                if candidate in known_modifiers or candidate in known_tones:
                    logger.debug(f"[🧠 FALLBACK ALLOWED] '{candidate}' in known vocab")
                else:
                    # Only proceed if known vocab or LLM confirms it's a color
                    if candidate in known_modifiers or candidate in known_tones:
                        logger.debug(f"[🧠 FALLBACK ALLOWED] '{candidate}' in known vocab")
                    else:
                        # 🚫 Block container/category nouns like 'tones', 'shades', 'colors'
                        if token.lemma_ in {"tone", "tones", "shade", "shades", "color",
                                            "colors"} and token.pos_ == "NOUN":
                            logger.debug(f"[🚫 BLOCKED GENERIC NOUN] '{candidate}' → Skipped as container noun")
                            continue

                        simplified = simplify_if_needed(candidate)
                        if not simplified:
                            logger.debug(f"[⚠️ LLM SIMPLIFICATION FAILED] '{candidate}'")

                            # ✅ Fallback: suffix-based color heuristic
                            if candidate.endswith(("y", "ish")):
                                for suffix in ["y", "ish"]:
                                    if candidate.endswith(suffix):
                                        base = candidate[:-len(suffix)]
                                        if base in known_tones:
                                            logger.debug(f"[🧠 SUFFIX COLOR FALLBACK] '{candidate}' → base='{base}'")
                                            candidate = base  # override candidate with valid tone base
                                            break
                                else:
                                    logger.debug(f"[🚫 SUFFIX STRIPPED BASE NOT A VALID TONE] '{candidate}' → Skipping")
                                    continue
                            else:
                                logger.debug(f"[🚫 SKIPPED NON-COLOR TOKEN] '{candidate}' → Not a suffix-based color")
                                continue

                logger.debug(f"[🆕 FALLBACK RGB CHECK] → {candidate}")

                try:
                    fallback_rgb = get_rgb_from_descriptive_color_llm_first(candidate)
                    if fallback_rgb:
                        store_rgb_to_cache(candidate, fallback_rgb)
                        logger.debug(f"[🎯 FALLBACK RGB RESULT] {candidate} → {fallback_rgb}")

                        phrase_rgb_map[candidate] = fallback_rgb  # ✅ <=== insert here

                        matches = get_similar_colors(fallback_rgb, rgb_map)
                        if matches:
                            logger.debug(f"[✅ ADDED VIA FALLBACK] {candidate} → {matches}")
                            all_color_names.update(matches)
                        else:
                            logger.debug(f"[⚠️ NO NEARBY COLORS] → {candidate} (will skip)")

                except Exception as e:
                    logger.warning(f"[❌ FALLBACK FAILED for {candidate}] → {e}")

    logger.debug(f"[🧹 SIMPLIFIED PHRASES] → {simplified_phrases}")
    categories = clean_and_categorize(simplified_phrases, known_modifiers, known_tones)

    rep_rgb = next(iter(phrase_rgb_map.values()), None)

    result = {
        "matched_color_names": sorted(all_color_names),
        "base_rgb": rep_rgb,
        "threshold": 60.0,
    }

    logger.debug(f"[📦 FINAL SENTIMENT OUTPUT] → {sentiment.upper()}")
    logger.debug(json.dumps(result, indent=2))
    return result


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

    sentiment_segments = {}

    try:
        sentiment_segments = run_sentiment_classification(text)
        logger.debug(f"[🧠 SENTIMENT CLASSIFICATION] → {sentiment_segments}")

    except Exception as e:
        logger.error(f"[❌ SENTIMENT ERROR] → {e}")

    # ✅ FIX: Always treat 'neutral' as 'positive' BEFORE using sentiment_segments
    if "neutral" in sentiment_segments:
        logger.debug(f"[🔁 REASSIGNED NEUTRAL] Now → {sentiment_segments}")
        sentiment_segments["positive"] = sentiment_segments.pop("neutral")

    # 🛡️ Ensure both keys exist before downstream processing
    for key in ["positive", "negative"]:
        if key not in sentiment_segments:
            sentiment_segments[key] = []

    base_rgb_by_sentiment = {}

    output = {}
    for sentiment in ["positive", "negative"]:
        if sentiment in sentiment_segments:
            output[sentiment] = build_sentiment_output(
                sentiment,
                sentiment_segments[sentiment],
                known_tones,
                known_modifiers,
                rgb_map,
                base_rgb_by_sentiment
            )
        else:
            output[sentiment] = {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            }

    import json
    logger.debug("[✅ FINAL OUTPUT STRUCTURE]")
    logger.debug(json.dumps(output, indent=2))

    # ───────────────────────────────────────────────────────────────
    # VIII. CONFLICT RESOLUTION — move overlaps from positive to negative
    # ───────────────────────────────────────────────────────────────
    pos_set = set(output["positive"]["matched_color_names"])
    neg_set = set(output["negative"]["matched_color_names"])

    # Detect strict conflicts
    conflict_colors = pos_set.intersection(neg_set)

    # Also detect partial overlaps like 'red' vs 'bright red'
    for neg_item in neg_set:
        neg_tokens = set(neg_item.lower().split())
        for pos_item in list(pos_set):
            pos_tokens = set(pos_item.lower().split())
            if neg_tokens.issubset(pos_tokens) or pos_tokens.issubset(neg_tokens):
                conflict_colors.add(pos_item)

    cleaned_pos = sorted(list(pos_set - conflict_colors))
    cleaned_neg = sorted(list(neg_set.union(conflict_colors)))

    output["positive"]["matched_color_names"] = cleaned_pos
    output["negative"]["matched_color_names"] = cleaned_neg

    if not cleaned_pos:
        output["positive"]["base_rgb"] = None

    logger.debug("[📊 CLEANED POSITIVE MATCHES] → %s", cleaned_pos)

    return output
