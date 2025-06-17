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


def resolve_modifier_token(
    word: str,
    known_modifiers: Set[str],
    known_tones: Optional[Set[str]] = None,
    allow_fuzzy: bool = True,
    is_tone: bool = False
) -> Optional[str]:
    raw = word.lower()
    print(f"[🔍 RESOLVE] Trying to resolve: '{raw}'")

    # 1. Direct match
    if raw in known_modifiers:
        print(f"[✅ DIRECT MATCH] '{raw}' found in modifiers")
        return raw

    # 2. Suffix-stripped base (and fuzzy match on base)
    for suffix in ["y", "ish"]:
        if raw.endswith(suffix):
            base = raw[:-len(suffix)]
            if base in known_modifiers:
                print(f"[🔁 SUFFIX '{suffix}'] '{raw}' → '{base}' in modifiers")
                return base
            if is_tone and known_tones and base in known_tones:
                print(f"[🔁 SUFFIX '{suffix}'] '{raw}' → '{base}' in tones")
                return base
            if allow_fuzzy:
                match = fuzzy_match_modifier(base, known_modifiers)
                if match:
                    print(f"[✨ FUZZY ON BASE] '{base}' → '{match}'")
                    return match
                if is_tone and known_tones:
                    match = fuzzy_match_modifier(base, known_tones)
                    if match:
                        print(f"[✨ FUZZY ON BASE TONE] '{base}' → '{match}'")
                        return match

    # 3. Fuzzy match on full word
    if allow_fuzzy:
        match = fuzzy_match_modifier(raw, known_modifiers)
        if match:
            print(f"[✨ FUZZY MODIFIER MATCH] '{raw}' → '{match}'")
            return match
        if is_tone and known_tones:
            match = fuzzy_match_modifier(raw, known_tones)
            if match:
                print(f"[✨ FUZZY TONE MATCH] '{raw}' → '{match}'")
                return match

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
