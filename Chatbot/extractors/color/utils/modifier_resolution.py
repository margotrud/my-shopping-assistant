#Chatbot/extractors/color/utils/modifier_resolution.py

"""
modifier_resolution.py
=======================

Handles all logic related to resolving modifier tokens in descriptive color phrases.
Supports direct matching, suffix fallback, and fuzzy logic.
"""
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.general.utils.fuzzy_match import fuzzy_token_match
from Chatbot.extractors.color.utils.token_utils import normalize_token
from Chatbot.extractors.color.logic.compound_rule import is_blocked_modifier_tone_pair

def is_known_tone(word: str) -> bool:
    return normalize_token(word) in known_tones
def match_direct_modifier(word: str, known_modifiers: set) -> str | None:
    raw = normalize_token(word)
    return raw if raw in known_modifiers else None


def match_suffix_fallback(word: str, known_modifiers: set) -> str | None:
    lowered = normalize_token(word)
    for suffix in ("y", "ish"):
        if lowered.endswith(suffix):
            base = lowered[:-len(suffix)].rstrip("-").strip()
            if len(base) >= 3 and base.isalpha():
                if base in known_modifiers:
                    return base
                # New rule: if base + 'e' is known, return that
                if base + "e" in known_modifiers:
                    return base + "e"
    return None



def fuzzy_match_modifier_safe(word: str, known_modifiers: set, threshold: int = 81) -> str | None:
    raw = normalize_token(word)
    best = _fuzzy_match_modifier(raw, known_modifiers)
    if best and best[1] >= threshold:
        return best[0]
    return None


def _fuzzy_match_modifier(raw: str, known_modifiers: set, threshold: float = 80, debug: bool = True) -> tuple[str, float] | None:
    best_score = 0
    best_match = None
    for candidate in known_modifiers:
        score = fuzzy_token_match(raw, candidate)
        if candidate == raw:
            # 👑 PRIORITIZE exact match
            best_match = candidate
            best_score = 100
            break
        elif ( score > best_score or
                (score == best_score and best_match is not None and len(candidate) < len(best_match))
            ):

            best_score = score
            best_match = candidate

    if best_match and best_score >= threshold:
        if debug:
            print(f"[DEBUG] Best match: '{best_match}' with score {best_score}")
        return best_match, best_score

    if debug:
        print("[DEBUG] No suitable match found (below threshold)")
    return None


def resolve_modifier_token(
    word: str,
    known_modifiers: set,
    known_tones: set,
    allow_fuzzy: bool = True,
    is_tone: bool = False,
    debug: bool = False
) -> str | None:
    raw = normalize_token(word)

    def debug_print(msg):
        if debug:
            print(msg)

    # 1. Direct exact match
    direct = match_direct_modifier(raw, known_modifiers)
    if direct:
        debug_print(f"[✅ DIRECT MATCH] '{raw}' → '{direct}'")
        return direct

    # 2. Suffix fallback
    suffix_match = match_suffix_fallback(raw, known_modifiers)
    if suffix_match:
        debug_print(f"[🌀 SUFFIX MATCH] '{raw}' → '{suffix_match}'")
        return suffix_match

    # 3. Try removing "ish"/"y" suffix and fuzzy match the base
    for suffix in ("y", "ish"):
        if raw.endswith(suffix):
            base = raw[:-len(suffix)].rstrip("-").strip()
            if len(base) >= 3:
                if base in known_tones:
                    if is_blocked_modifier_tone_pair(base, raw):
                        debug_print(f"[⛔ BLOCKED PAIR] '{base} {raw}' → blocked by rule")
                        return None
                    debug_print(f"[🌀 BASE IS TONE] '{raw}' → '{base}'")
                    return base
                base_fuzzy = fuzzy_match_modifier_safe(base, known_modifiers)
                if base_fuzzy:
                    debug_print(f"[🧪 FUZZY BASE] '{raw}' → '{base_fuzzy}' (via base '{base}')")
                    return base_fuzzy

    # 4. Fuzzy match fallback BEFORE blocking
    if allow_fuzzy:
        fuzzy = fuzzy_match_modifier_safe(raw, known_modifiers | known_tones)
        if fuzzy:
            debug_print(f"[🤏 FUZZY MATCH] '{raw}' → '{fuzzy}'")
            return fuzzy

    # 5. Block tones being used as modifiers
    if not is_tone and raw in known_tones:
        debug_print(f"[⛔ BLOCKED] '{raw}' is a tone, not a modifier")
        return None

    debug_print(f"[❌ UNRESOLVED] '{raw}' not matched")
    return None
def is_y_suffix_from_tone(word: str, known_tones: set) -> bool:
    raw = normalize_token(word)
    return raw.endswith("y") and raw[:-1] in known_tones


def should_suppress_compound(mod: str, tone: str) -> bool:
    return mod == tone or tone.startswith(mod) or mod.startswith(tone)