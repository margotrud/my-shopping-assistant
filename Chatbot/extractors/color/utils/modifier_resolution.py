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

from typing import Optional, Set
from rapidfuzz import fuzz


def resolve_modifier_token(
    word: str,
    known_modifiers: Set[str],
    known_tones: Optional[Set[str]] = None,
    allow_fuzzy: bool = True,
    is_tone: bool = False
) -> Optional[str]:
    """
    Resolves a modifier token to a known modifier using direct match,
    suffix stripping, or optional fuzzy matching.

    Args:
        word (str): Input token (e.g., 'barely', 'softy')
        known_modifiers (Set[str]): Set of valid modifiers.
        known_tones (Optional[Set[str]]): Optional tones for suffix fallback disambiguation.
        allow_fuzzy (bool): Whether to use fuzzy fallback.
        is_tone (bool): If True, allows tone disambiguation via known_tones.

    Returns:
        Optional[str]: Best matched modifier or None if unresolved.
    """
    raw = word.lower()

    # 1. Direct match
    if raw in known_modifiers:
        return raw

    # 2. Suffix fallback
    if raw.endswith("y"):
        base = raw[:-1]
        if base in known_modifiers or (is_tone and known_tones and base in known_tones):
            return base
    if raw.endswith("ish"):
        base = raw[:-3]
        if base in known_modifiers or (is_tone and known_tones and base in known_tones):
            return base

    # 3. Fuzzy fallback
    if allow_fuzzy:
        for mod in known_modifiers:
            if fuzzy_match_modifier(raw, mod):
                return mod

    return None


def fuzzy_match_modifier(token: str, target: str, threshold: int = 85) -> bool:
    """
    Checks if two tokens match fuzzily using edit distance.

    Args:
        token (str): Input token.
        target (str): Target known modifier.
        threshold (int): Minimum similarity score (default: 85)

    Returns:
        bool: True if match passes threshold.
    """
    return fuzz.ratio(token.lower(), target.lower()) >= threshold

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
