#Chatbot/extractors/color/utils/modifier_resolution.py

"""
modifier_resolution.py
=======================

Handles all logic related to resolving modifier tokens in descriptive color phrases.
Supports direct matching, suffix fallback, and fuzzy logic.
"""
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.general.utils.fuzzy_match import fuzzy_token_match

def is_known_tone(word: str) -> bool:
    return word.lower() in known_tones
def match_direct_modifier(word: str, known_modifiers: set) -> str | None:
    raw = word.lower()
    return raw if raw in known_modifiers else None


def match_suffix_fallback(word: str, known_modifiers: set) -> str | None:
    lowered = word.lower()
    for suffix in ("y", "ish"):
        if lowered.endswith(suffix):
            base = lowered[:-len(suffix)].rstrip("-").strip()
            if len(base) >= 3 and base.isalpha() and base in known_modifiers:
                return base
    return None


def fuzzy_match_modifier_safe(word: str, known_modifiers: set, threshold: int = 83) -> str | None:
    raw = word.lower()
    best = _fuzzy_match_modifier(raw, known_modifiers)
    if best and best[1] >= threshold:
        return best[0]
    return None


def _fuzzy_match_modifier(raw: str, known_modifiers: set) -> tuple[str, float] | None:
    best_score = 0
    best_match = None
    for candidate in known_modifiers:
        score = fuzzy_token_match(raw, candidate)
        if score > best_score:
            best_score = score
            best_match = candidate
    return (best_match, best_score) if best_match else None


def resolve_modifier_token(word: str, known_modifiers: set, known_tones: set, allow_fuzzy=True, is_tone=False, debug=False) -> str | None:
    raw = word.lower()
    if not is_tone and raw in known_tones:
        if debug:
            print(f"[⛔ BLOCKED] '{raw}' is a tone, not a modifier")
        return None

    direct = match_direct_modifier(raw, known_modifiers)
    if direct:
        if debug:
            print(f"[✅ DIRECT MATCH] '{raw}' → '{direct}'")
        return direct

    suffix = match_suffix_fallback(raw, known_modifiers)
    if suffix:
        if debug:
            print(f"[🌀 SUFFIX MATCH] '{raw}' → '{suffix}'")
        return suffix

    if allow_fuzzy:
        fuzzy = fuzzy_match_modifier_safe(raw, known_modifiers)
        if fuzzy:
            if debug:
                print(f"[🤏 FUZZY MATCH] '{raw}' → '{fuzzy}'")
            return fuzzy

    if debug:
        print(f"[❌ UNRESOLVED] '{raw}' not matched")
    return None


def is_y_suffix_from_tone(word: str, known_tones: set) -> bool:
    raw = word.lower()
    return raw.endswith("y") and raw[:-1] in known_tones


def should_suppress_compound(mod: str, tone: str) -> bool:
    return mod == tone or tone.startswith(mod) or mod.startswith(tone)