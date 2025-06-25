# Chatbot/extractors/color/llm/simplifier.py
"""
simplifier.py
=============

Handles simplification of descriptive color phrases using both rules and LLM.
Also provides suffix fallback logic when direct match fails.
"""

from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def simplify_phrase_if_needed(phrase: str, known_modifiers, known_tones, debug=False) -> str:
    if debug:
        print(f"[🔍 SIMPLIFY] Checking phrase: '{phrase}'")
    if is_valid_tone(phrase, known_tones):
        if debug:
            print(f"[✅ TONE KNOWN] '{phrase}' is a known tone")
        return phrase

    fallback = extract_suffix_fallbacks(phrase, known_modifiers, known_tones, debug)
    if fallback:
        if debug:
            print(f"[✅ FALLBACK MATCH] Using suffix fallback: '{fallback}'")
        return fallback

    if debug:
        print(f"[⚠️ UNSIMPLIFIED] No fallback found, returning raw phrase")
    return phrase

def is_valid_tone(phrase: str, known_tones) -> bool:
    return normalize_token(phrase) in known_tones

def extract_suffix_fallbacks(raw_phrase: str, known_modifiers, known_tones, debug=False):
    lowered = normalize_token(raw_phrase)
    for suffix in ("y", "ish"):
        if lowered.endswith(suffix):
            base = normalize_token(lowered[:-len(suffix)])
            if len(base) < 3 or not base.isalpha():
                if debug:
                    print(f"[⛔ INVALID BASE] '{lowered}' → '{base}' (too short or invalid)")
                continue
            resolved = resolve_modifier_token(base, known_modifiers, known_tones)
            if resolved:
                simplified = f"{resolved} {base}"
                if debug:
                    print(f"[🧪 SUFFIX FALLBACK] '{raw_phrase}' → '{simplified}'")
                return simplified
    return None


def build_prompt(phrase: str) -> str:
    return f"What is the simplified base color or tone implied by: '{phrase}'?"


def simplify_color_description_with_llm(phrase: str, llm_client, cache=None, debug=False) -> str:
    prompt = build_prompt(phrase)
    if debug:
        print(f"[🧠 LLM PROMPT] {prompt}")

    if cache:
        cached = cache.get_simplified(phrase)
        if cached:
            if debug:
                print(f"[🗃️ CACHE HIT] '{phrase}' → '{cached}'")
            return cached

    simplified = llm_client.simplify(prompt)

    if cache:
        cache.store_simplified(phrase, simplified)

    if debug:
        print(f"[🧠 LLM RESPONSE] '{phrase}' → '{simplified}'")
    return simplified
