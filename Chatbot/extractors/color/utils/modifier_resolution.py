#Chatbot/extractors/color/utils/modifier_resolution.py

"""
modifier_resolution.py
=======================
Handles resolution and fuzzy matching of color modifiers.

This module provides utilities for:
- Resolving noisy or derived user inputs to known modifiers
- Fuzzy string matching for flexible input handling
- Suffix stripping for tokens like 'peachy' or 'greenish'

Used in compound phrase extraction, standalone parsing,
and suffix-based fallbacks across the color pipeline.

Examples:
---------
>>> resolve_modifier_token("barely", known_modifiers)
"barely-there"

>>> resolve_modifier_token("softy", known_modifiers)
"soft"

>>> fuzzy_match_modifier("barely", "barely-there")
True
"""

from typing import Optional, Set, Union
from rapidfuzz import fuzz


def _is_known_tone(raw: str, known_tones: Optional[Set[str]]) -> bool:
    return known_tones is not None and raw in known_tones

def _match_direct_modifier(raw: str, known_modifiers: Set[str]) -> Optional[str]:
    if raw in known_modifiers:
        print(f"[✅ DIRECT MATCH] '{raw}' found in modifiers")
        return raw
    return None

def _match_suffix_fallback(raw: str, known_modifiers: Set[str], known_tones: Optional[Set[str]], allow_fuzzy: bool, is_tone: bool) -> Optional[str]:
    for suffix in ["y", "ish"]:
        if raw.endswith(suffix):
            base = raw[:-len(suffix)]
            cleaned_base = base.rstrip("-").strip()
            if len(cleaned_base) < 3 or not cleaned_base.isalpha():
                print(f"[⛔ INVALID BASE] '{raw}' → '{base}' (too short or non-alpha)")
                continue

            if cleaned_base in known_modifiers:
                print(f"[🔁 SUFFIX '{suffix}'] '{raw}' → '{cleaned_base}' in modifiers")
                return cleaned_base

            if is_tone and known_tones and cleaned_base in known_tones:
                print(f"[🔁 SUFFIX '{suffix}'] '{raw}' → '{cleaned_base}' in tones")
                return cleaned_base

            if allow_fuzzy and not is_tone:
                if known_tones and cleaned_base in known_tones:
                    print(f"[⛔ BLOCKED FUZZY BASE] '{cleaned_base}' is a tone — skip")
                    continue
                match = fuzzy_match_modifier(cleaned_base, known_modifiers)
                if match:
                    print(f"[✨ FUZZY ON BASE] '{cleaned_base}' → '{match}'")
                    return match
    return None

def _fuzzy_match_modifier_safe(raw: str, known_modifiers: Set[str], known_tones: Optional[Set[str]]) -> Optional[str]:
    if _is_known_tone(raw, known_tones):
        print(f"[⛔ SKIP FUZZY] '{raw}' is in known tones — skip fuzzy match")
        return None
    match = fuzzy_match_modifier(raw, known_modifiers)
    if match:
        print(f"[✨ FUZZY MODIFIER MATCH] '{raw}' → '{match}'")
        return match
    return None

def _fuzzy_match_tone(raw: str, known_tones: Optional[Set[str]]) -> Optional[str]:
    if known_tones:
        match = fuzzy_match_modifier(raw, known_tones, threshold=60)
        if match:
            print(f"[✨ FUZZY TONE MATCH] '{raw}' → '{match}'")
            return match
    return None

def resolve_modifier_token(
    word: str,
    known_modifiers: Set[str],
    known_tones: Optional[Set[str]] = None,
    allow_fuzzy: bool = True,
    is_tone: bool = False
) -> Optional[str]:
    raw = word.lower()
    print(f"[🔍 RESOLVE] Trying to resolve: '{raw}'")

    # ─── STRICT TONE MODE ──────────────────────
    if is_tone and not allow_fuzzy:
        if _is_known_tone(raw, known_tones):
            print(f"[🎯 STRICT TONE MATCH] '{raw}' accepted as tone")
            return raw
        print(f"[❌ STRICT TONE REJECTED] '{raw}' is not a valid tone")
        return None

    # ─── BLOCK TONE USED AS MODIFIER ───────────
    if not is_tone and _is_known_tone(raw, known_tones):
        print(f"[⛔ ABORT] '{raw}' is a tone, not a modifier")
        return None

    # ─── DIRECT MATCH ──────────────────────────
    direct = _match_direct_modifier(raw, known_modifiers)
    if direct:
        return direct

    # ─── SUFFIX FALLBACK ───────────────────────
    suffix_match = _match_suffix_fallback(raw, known_modifiers, known_tones, allow_fuzzy, is_tone)
    if suffix_match:
        return suffix_match

    # ─── FUZZY MODIFIER (GUARDED) ───────────────
    if allow_fuzzy and not is_tone:
        fuzzy_mod = _fuzzy_match_modifier_safe(raw, known_modifiers, known_tones)
        if fuzzy_mod:
            return fuzzy_mod

    # ─── FUZZY TONE (ONLY IF TONE MODE) ────────
    if is_tone and allow_fuzzy:
        fuzzy_tone = _fuzzy_match_tone(raw, known_tones)
        if fuzzy_tone:
            return fuzzy_tone

    # ─── FINAL FALLBACK ────────────────────────
    print(f"[❌ UNRESOLVED] '{raw}' could not be matched")
    return None


def fuzzy_match_modifier(token: str, target: Union[str, Set[str]], threshold: int = 75):
    """
    Checks if two tokens match fuzzily (string-to-string or string-to-set).

    Args:
        token (str): Input token to test.
        target (Union[str, Set[str]]): Single known modifier or set of them.
        threshold (int): Minimum similarity score.

    Returns:
        Union[bool, Optional[str]]:
            - If target is a string → returns bool
            - If target is a set → returns best matching string or None
    """
    token = token.lower()

    if isinstance(target, str):
        score = fuzz.ratio(token, target.lower())
        print(f"[🧪 FUZZY COMPARE] '{token}' vs '{target.lower()}' → score={score} (threshold={threshold})")
        return score >= threshold

    best_score = 0
    best_match = None
    for mod in target:
        score = fuzz.ratio(token, mod.lower())
        print(f"[🧪 FUZZY SET CHECK] '{token}' vs '{mod.lower()}' → score={score}")
        if score >= threshold and score > best_score:
            best_score = score
            best_match = mod

    if best_match:
        print(f"[✅ BEST MATCH FOUND] '{token}' → '{best_match}' with score={best_score}")
    else:
        print(f"[❌ NO MATCH] '{token}' → No match ≥ {threshold}")
    return best_match
def _is_y_suffix_from_tone(word: str, known_tones: Optional[Set[str]]) -> bool:
    """
    Checks if a modifier candidate like 'rosy' ends in 'y' and
    its base is a known tone (e.g., 'rose').

    Used to prevent reusing tone-derived words as modifiers.

    Args:
        word (str): The word to evaluate (e.g., 'rosy').
        known_tones (Optional[Set[str]]): Set of valid tone words.

    Returns:
        bool: True if the word is a 'y'-suffix form of a known tone.
    """
    if known_tones and word.endswith("y"):
        base = word[:-1]
        return base in known_tones
    return False


def should_suppress_compound(
    raw_modifier: str,
    resolved_modifier: Optional[str],
    resolved_tone: Optional[str],
    known_tones: Set[str]
) -> bool:
    return (
        raw_modifier.endswith("y") and
        resolved_modifier in known_tones and
        resolved_tone is None
    )
