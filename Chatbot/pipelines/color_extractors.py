import logging
from Chatbot.extractors.sentiment import (
    contains_sentiment_splitter_with_segments,
    classify_segments_by_sentiment_no_neutral,
)

from Chatbot.extractors.colors import (
    extract_all_descriptive_color_phrases,
    categorize_color_tokens_with_mapping,
    simplify_color_description_with_llm, fuzzy_match_modifier
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
from matplotlib.colors import CSS4_COLORS, XKCD_COLORS
from typing import Dict, List, Set
import webcolors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ColorPipeline")

# Load cache once at module load
load_cache_from_file()


def extract_color_pipeline(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    rgb_map: Dict[str, tuple] = None
) -> Dict[str, Dict[str, List[str]]]:
    """
    Full pipeline to extract, simplify, categorize, and RGB-match color descriptions from user input.

    Returns:
        {
            "positive": {
                "tones": [...],
                "matched_color_names": [...]
            },
            "negative": {
                "tones": [...],
                "matched_color_names": [...]
            }
        }
    """

    logger.info(f"[🎤 USER INPUT] → {text}")

    try:
        has_splitter, segments = contains_sentiment_splitter_with_segments(text)
        logger.info(f"[🔍 SPLIT DETECTED] → {has_splitter}, segments = {segments}")
        classified = classify_segments_by_sentiment_no_neutral(has_splitter, segments)
        logger.info(f"[🧠 SENTIMENT CLASSIFIED] → {classified}")
    except Exception as e:
        logger.error(f"[❌ ERROR] during sentiment detection: {e}")
        return {"positive": {}, "negative": {}}

    output = {"positive": {}, "negative": {}}
    rgb_map = rgb_map or {
        name: webcolors.hex_to_rgb(value)
        for name, value in {**CSS4_COLORS, **XKCD_COLORS}.items()
    }

    for sentiment in ["positive", "negative"]:
        print(f"[⚙️ PROCESSING SENTIMENT] {sentiment}")
        all_phrases = []
        simplified_phrases = []
        all_color_names = set()

        logger.info(f"[🧩 PROCESSING SEGMENTS] → {sentiment.upper()}")

        for seg in classified[sentiment]:
            try:
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"[📥 RAW SEGMENT TEXT] → {repr(seg)}")
                phrases = extract_all_descriptive_color_phrases(
                    text=seg,
                    known_tones=known_tones,
                    known_modifiers=known_modifiers,
                    debug=True
                )

                print(f"[🧪 PHRASES EXTRACTED] {phrases}")  # 🔍 INSERT THIS
                all_phrases.extend(phrases)
            except Exception as e:
                logger.warning(f"[⚠️ SKIP SEGMENT] '{seg}' → {e}")

        for phrase in all_phrases:
            logger.info(f"[🧪 RAW PHRASE] → '{phrase}'")
            print(f"[🧪 RAW PHRASE] → '{phrase}'")

            if phrase.lower() not in known_modifiers and phrase.lower() not in known_tones:
                logger.info(f"[⛔ SKIPPED LLM] '{phrase}' not in known modifiers or tones → skipping LLM call")
                print(f"[⛔ SKIPPED LLM] '{phrase}' not in known modifiers or tones → skipping LLM call")
                continue

            logger.info(f"[DEBUG] ➤ Processing phrase: '{phrase}'")
            logger.info(f"[DEBUG] ➤ Is in RGB MAP? {'✅' if phrase in rgb_map else '❌'}")

            try:
                # ✅ If it's a known color, use it directly and skip LLM/simplify
                if phrase in rgb_map:
                    rgb = rgb_map[phrase]
                    logger.info(f"[✅ RGB DIRECT MATCH] '{phrase}' found in rgb_map → {rgb}")
                    matches = find_similar_color_names(rgb, rgb_map)
                    logger.info(f"[🔍 RGB MATCH] for '{phrase}' → {matches}")
                    all_color_names.update(matches)

                    # ✅ Treat as tone directly if in known_tones
                    if phrase in known_tones:
                        logger.info(f"[🧠 DIRECT TONE ADD] '{phrase}' is a known tone")
                        simplified_phrases.append(phrase)
                    else:
                        logger.info(f"[ℹ️ NO TONE CLASSIFICATION] '{phrase}' not in known tones")

                    continue  # ✅ No need to run LLM

                # Step 1: RGB cache lookup
                cached_rgb = get_cached_rgb(phrase)
                if cached_rgb:
                    rgb = cached_rgb
                    logger.info(f"[🧠 RGB CACHE HIT] → {phrase} → {rgb}")
                else:
                    rgb = get_rgb_from_descriptive_color_llm_first(phrase)
                    if rgb:
                        store_rgb_to_cache(phrase, rgb)
                        logger.info(f"[💾 RGB CACHE STORE] → {phrase} → {rgb}")

                # Step 2: Match similar names
                if rgb:
                    matches = find_similar_color_names(rgb, rgb_map)
                    logger.info(f"[🔍 RGB MATCH] for '{phrase}' → {matches}")
                    all_color_names.update(matches)
                else:
                    logger.warning(f"[⚠️ NO RGB MATCH] for phrase '{phrase}'")

                # Step 3: Simplification (only for unknown phrases)
                cached_simplified = get_cached_simplified(phrase)
                if cached_simplified:
                    simplified = cached_simplified
                    logger.info(f"[🧠 SIMPLIFY CACHE HIT] → {phrase} → {simplified}")
                else:
                    simplified = simplify_color_description_with_llm(phrase)
                    print(f"[🧠 LLM RESULT] → {simplified}")
                    logger.info(f"[🧠 LLM RESULT] → {simplified}")

                    if simplified:
                        store_simplified_to_cache(phrase, simplified)
                        logger.info(f"[💾 SIMPLIFY CACHE STORE] → {phrase} → {simplified}")

                simplified_phrases.extend(simplified)
                print(f"[🎯 SIMPLIFIED PHRASES ADDED] {simplified}")

            except Exception as e:
                logger.error(f"[❌ ERROR] during RGB/simplify for '{phrase}' → {e}")

                # ✅ Always try to simplify, even if RGB lookup fails
                cached_simplified = get_cached_simplified(phrase)
                if cached_simplified:
                    simplified = cached_simplified
                    logger.info(f"[🧠 SIMPLIFY CACHE HIT] → {phrase} → {simplified}")
                else:
                    simplified = simplify_color_description_with_llm(phrase)
                    if simplified:
                        store_simplified_to_cache(phrase, simplified)
                        logger.info(f"[💾 SIMPLIFY CACHE STORE] → {phrase} → {simplified}")

                simplified_phrases.extend(simplified)
                print(f"[🎯 SIMPLIFIED PHRASES ADDED] {simplified}")



            except Exception as e:
                logger.error(f"[❌ ERROR] during RGB/simplify for '{phrase}' → {e}")

        try:
            print(f"[📦 FINAL COLOR NAMES] {all_color_names}")
            print(f"[📦 FINAL SIMPLIFIED PHRASES] {simplified_phrases}")  # 🔍 INSERT THIS

            # 🧽 Fuzzy correct modifiers inside simplified phrases
            corrected_phrases = []
            for phrase in simplified_phrases:
                tokens = phrase.lower().split()
                if len(tokens) == 2:
                    mod, tone = tokens
                    mod_fixed = fuzzy_match_modifier(mod, known_modifiers) or mod
                    corrected_phrases.append(f"{mod_fixed} {tone}")
                    if mod != mod_fixed:
                        print(f"[🧠 FUZZY FIX] {mod} → {mod_fixed}")
                else:
                    corrected_phrases.append(phrase)
            simplified_phrases = corrected_phrases

            cat = categorize_color_tokens_with_mapping(
                simplified_phrases, known_tones, known_modifiers
            )
            tones = cat.get("tones", [])
            modifiers = cat.get("modifiers", [])

            print(f"[🎯 FINAL COLOR CATEGORIZATION]")
            print(f"    → TONES:     {tones}")
            print(f"    → MODIFIERS: {modifiers}")
            print(f"    → PHRASES:   {simplified_phrases}")



        except Exception as e:
            logger.error(f"[❌ ERROR] during categorization → {e}")
            tones = []

        output[sentiment] = {
            "tones": tones,
            "matched_color_names": sorted(all_color_names)
        }

    # Save cache after every call (can be throttled if needed)
    save_cache_to_file()

    return output
