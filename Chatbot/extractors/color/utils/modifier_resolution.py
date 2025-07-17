#Chatbot/extractors/color/utils/modifier_resolution.py

"""
modifier_resolution.py
=======================

Handles all logic related to resolving modifier tokens in descriptive color phrases.
Supports direct matching, suffix fallback, and fuzzy logic.
"""
from typing import Set

from fuzzywuzzy import fuzz

from Chatbot.extractors.color.shared.constants import SEMANTIC_CONFLICTS
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.token_utils import normalize_token
from Chatbot.extractors.color.logic.compound_rule import is_blocked_modifier_tone_pair

def is_known_tone(word: str) -> bool:
    return normalize_token(word) in known_tones
from Chatbot.extractors.color.utils.token_utils import normalize_token, singularize

def match_direct_modifier(token: str, known_modifiers: set, debug: bool = False) -> str | None:
    """
    Resolves a token to a known modifier using direct match, suffix stripping,
    override map, and compound splitting.

    Handles:
    - Plural forms
    - Derived adjectives (e.g., -y, -ish, -ness)
    - Irregular forms (via override map)
    - Hyphenated or space-separated compounds (e.g., 'soft-focus')
    """

    raw = token
    token = token.strip().lower().replace("-", " ").strip()

    if token in known_modifiers:
        return token

    # Manual overrides for irregular transformations
    OVERRIDE_MAP = {
        "matting": "matte",
        "rosier": "rose"
    }
    if token in OVERRIDE_MAP:
        if debug:
            print(f"[OVERRIDE] '{raw}' → '{OVERRIDE_MAP[token]}'")
        return OVERRIDE_MAP[token]

    # Suffix stripping logic
    SUFFIXES = (
        "iness", "ness", "ishly", "ly", "ish", "y",
        "ier", "er", "est", "ing", "edly", "en"
    )
    for suffix in SUFFIXES:
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            base = token[: -len(suffix)]
            if base in known_modifiers:
                if debug:
                    print(f"[SUFFIX MATCH] '{raw}' → '{base}' (via -{suffix})")
                return base

    # Special case: 'rosy' → 'rose'
    if token.endswith("y") and (token[:-1] + "e") in known_modifiers:
        fallback = token[:-1] + "e"
        if debug:
            print(f"[Y→E FALLBACK] '{raw}' → '{fallback}'")
        return fallback

    # Singularize
    singular = singularize(token)
    if singular in known_modifiers:
        if debug:
            print(f"[SINGULAR MATCH] '{raw}' → '{singular}'")
        return singular

    # Compound fallback: pick any part if present
    if " " in token:
        for part in token.split():
            if part in known_modifiers:
                if debug:
                    print(f"[COMPOUND MATCH] '{raw}' → '{part}'")
                return part

    if debug:
        print(f"[NO MATCH] '{raw}' → no match in known_modifiers")
    return None

def match_suffix_fallback(token: str, known_modifiers: set) -> str | None:
    """
    Attempts to strip known cosmetic suffixes and return a valid modifier root.
    Handles noise like 'softishy', 'rosy-', 'soft y', 'shady' (via override).
    """
    raw = token
    token = token.lower().strip().replace("-", "").replace(" ", "")

    if token in known_modifiers:
        return token

    # Manual overrides
    OVERRIDE_MAP = {
        "matting": "matte",
        "rosier": "rose",
        "rosy": "rose",
        "rosy-": "rose",
        "shady": "shade",
        "soft y": "soft"
    }
    if raw.strip().lower() in OVERRIDE_MAP:
        return OVERRIDE_MAP[raw.strip().lower()]

    # Recursive suffix stripper
    SUFFIXES = ("ish", "y", "er", "ly", "en", "ness", "ing", "est", "ier")
    seen = set()

    while token and token not in seen:
        seen.add(token)
        for suffix in SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                token = token[: -len(suffix)]
                if token in known_modifiers:
                    return token
                # y→e fallback for mid-stages too
                if token.endswith("y") and token[:-1] + "e" in known_modifiers:
                    return token[:-1] + "e"
                break
        else:
            break

    # Final soft y→e fallback
    if raw.endswith("y") and (raw[:-1] + "e") in known_modifiers:
        return raw[:-1] + "e"

    return None



def fuzzy_match_modifier_safe(raw_token: str, known_modifiers: set, threshold: int = 70) -> str:
    """
    Attempts to fuzzy match a raw token to a known modifier.
    Returns the best match if score is above the threshold.
    Returns None if no match passes the threshold.
    """
    raw_token = raw_token.lower().strip()
    best_match = None
    best_score = 0

    for candidate in known_modifiers:
        candidate_norm = candidate.lower().strip()
        score = fuzz.ratio(raw_token, candidate_norm)

        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        return best_match

    print(f"[DEBUG] Best match for '{raw_token}': '{best_match}' with score {best_score}")

    return None


def _fuzzy_match_modifier(raw: str, known_modifiers: set, threshold: float = 75, debug: bool = True) -> tuple[str, float] | None:
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

import spacy
nlp = spacy.load("en_core_web_sm")
def lemmatize_token(token: str) -> str:
    doc = nlp(token)
    return doc[0].lemma_ if doc else token
def resolve_modifier_token(
    raw_token: str,
    known_modifiers: set,
    known_tones: set = None,
    allow_fuzzy: bool = True,
    is_tone: bool = False,
    debug: bool = False
) -> str | None:
    """
    Resolves a token to a known modifier using:
    1. Direct match
    2. Lemmatization (e.g., 'blurred' → 'blur')
    3. Suffix fallback (e.g., 'softish' → 'soft')
    4. Optional fuzzy match (e.g., 'sofft' → 'soft')

    Args:
        raw_token (str): The raw input token.
        known_modifiers (set): Set of accepted modifiers.
        known_tones (set, optional): Set of tones (used for tone blocking).
        allow_fuzzy (bool): Whether to allow fuzzy fallback if strict methods fail.
        is_tone (bool): Whether this token is intended to resolve as a tone.
        debug (bool): If True, print resolution trace.

    Returns:
        str | None: The resolved modifier, or None if no match found.
    """

    token = raw_token.strip().lower()
    # ─── Shortcut: Accept if it's a valid tone
    if known_tones and token in known_tones:
        if debug:
            print(f"[🎯 KNOWN TONE SHORTCUT] '{raw_token}' is a valid tone → returning as-is")
        return token

    # Step 1: Direct match
    direct = match_direct_modifier(token, known_modifiers, debug)
    if direct:
        if debug:
            print(f"[✅ DIRECT MATCH] '{raw_token}' → '{direct}'")
        return direct

    # Step 2: Lemmatization fallback
    lemma = lemmatize_token(token)
    if lemma in known_modifiers:
        if debug:
            print(f"[✅ LEMMA MATCH] '{raw_token}' → '{lemma}'")
        return lemma

    # Step 3: Suffix fallback
    suffix = match_suffix_fallback(token, known_modifiers)
    if suffix:
        if debug:
            print(f"[✅ SUFFIX MATCH] '{raw_token}' → '{suffix}'")
        return suffix

    # Step 4: Fuzzy fallback
    if allow_fuzzy:
        fuzzy = fuzzy_match_modifier_safe(token, known_modifiers)
        if isinstance(fuzzy, tuple) and len(fuzzy) == 2:
            match, score = fuzzy

            # 🔍 Filtering to block unsafe semantic returns
            if match in {"blur", "classic", "luminous", "radiant", "off-white"}:
                if debug:
                    print(f"[⚠️ BLOCKED FUZZY] '{raw_token}' → '{match}' (score={score})")
                return None

            if len(match) > len(token) + 3 and score < 80:
                if debug:
                    print(f"[⚠️ SKIPPED: too long fuzzy match] '{raw_token}' → '{match}' (score={score})")
                return None

            if debug:
                print(f"[🔍 FUZZY MATCH] '{raw_token}' → '{match}' (score={score})")
            return match

        elif isinstance(fuzzy, str):
            # fallback behavior if fuzzy_match_modifier_safe returns str (e.g. "bright")
            if debug:
                print(f"[🔍 FUZZY MATCH (no score)] '{raw_token}' → '{fuzzy}'")
            return fuzzy

    if debug:
        print(f"[❌ NO MATCH] '{raw_token}' → None")
    return None

def is_y_suffix_from_tone(word: str, known_tones: set) -> bool:
    raw = normalize_token(word)
    return raw.endswith("y") and raw[:-1] in known_tones


def should_suppress_compound(mod: str, tone: str) -> bool:
    return mod == tone or tone.startswith(mod) or mod.startswith(tone)

def is_modifier_compound_conflict(expression: str, modifier_tokens: Set[str]) -> bool:
    """
    Determines whether the expression token overlaps with the modifier space.
    Uses internal resolution logic.
    """
    resolved = resolve_modifier_token(expression, modifier_tokens, known_tones=None, allow_fuzzy=True, is_tone=False)
    return resolved in modifier_tokens

def fuzzy_token_match(a: str, b: str) -> float:
    a = normalize_token(a)
    b = normalize_token(b)

    if a == b:
        return 100

    if frozenset({a, b}) in SEMANTIC_CONFLICTS:
        return 50

    partial = fuzz.partial_ratio(a, b)
    ratio = fuzz.ratio(a, b)
    bonus = 10 if a[:3] == b[:3] or a[:2] == b[:2] else 0

    return min(100, round((partial + ratio) / 2 + bonus))
