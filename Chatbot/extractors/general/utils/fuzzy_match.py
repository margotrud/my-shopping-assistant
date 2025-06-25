# Chatbot/extractors/general/utils/fuzzy_match.py

"""
fuzzy_match.py
==============

Generic fuzzy token matcher with blocklist, prefix, and multi-word logic.

Designed for reuse across multiple domains (e.g., colors, brands, products).
Wraps common secure fuzzy matching behaviors into a single configurable function.

Features:
---------
- Exact match
- Safe prefix match (single-word only)
- Multi-word trigger matching
- Fuzzy string ratio fallback
- Optional semantic blocklist filtering
"""

from typing import List, Set
import re
from fuzzywuzzy import fuzz
from Chatbot.extractors.color.shared.constants import SEMANTIC_CONFLICTS
from Chatbot.extractors.color.utils.token_utils import singularize, normalize_token


def fuzzy_token_match(a: str, b: str) -> float:
    a = normalize_token(a)
    b = normalize_token(b)

    if a == b:
        return 100

    if frozenset({a, b}) in SEMANTIC_CONFLICTS:
        return 60  # hard semantic block

    partial = fuzz.partial_ratio(a, b)
    ratio = fuzz.ratio(a, b)
    bonus = 10 if a[:3] == b[:3] or a[:2] == b[:2] else 0

    return min(100, round((partial + ratio) / 2 + bonus))
def match_expression_aliases(input_text: str, aliases: list, threshold: int = 80) -> bool:
    """
    Determines if user input fuzzily matches any known expression alias.
    Uses both partial and token sort ratio for robust matching.

    Args:
        input_text (str): User input (not necessarily lowercase).
        aliases (List[str]): List of known aliases for an expression.
        threshold (int): Minimum fuzzy score to count as match.

    Returns:
        bool: True if any alias matches input fuzzily, else False.
    """
    input_text = normalize_token(input_text)

    for alias in aliases:
        alias = normalize_token(alias)

        score = max(
            fuzz.partial_ratio(alias, input_text),
            fuzz.token_sort_ratio(alias, input_text)
        )

        if score >= threshold:
            return True

    return False
def should_accept_multiword_alias(alias: str, input_text: str, threshold: int = 85) -> bool:
    """
    Evaluates whether a multi-word alias should be accepted as a match based on fuzzy similarity.

    Args:
        alias (str): The multi-word alias (e.g., "work appropriate").
        input_text (str): Lowercased user input text (e.g., "something more work appropriate").
        threshold (int): Minimum fuzzy ratio required for match.

    Returns:
        bool: True if match is confident, else False.
    """
    score = fuzz.partial_ratio(normalize_token(alias), normalize_token(input_text))
    return score >= threshold


def is_exact_match(a: str, b: str) -> bool:
    """
    Checks for normalized equality.

    Args:
        a (str): First token.
        b (str): Second token.

    Returns:
        bool: True if equal after normalization.
    """
    return normalize_token(a) == normalize_token(b)


def is_strong_fuzzy_match(a: str, b: str, threshold: int = 85) -> bool:
    a_norm = normalize_token(a)
    b_norm = normalize_token(b)

    if frozenset({a_norm, b_norm}) in SEMANTIC_CONFLICTS:
        return False

    if is_negation_conflict(a_norm, b_norm):
        return False

    return fuzzy_token_match(a_norm, b_norm) >= threshold
def is_embedded_alias_conflict(longer: str, shorter: str) -> bool:
    """
    Detects conflict where one alias is embedded in another (e.g., 'glamorous' vs 'glam').

    Args:
        longer (str): Full phrase matched.
        shorter (str): Alias token.

    Returns:
        bool: True if alias is strictly embedded and not equal.
    """
    return shorter in longer and shorter != longer


def is_modifier_compound_conflict(expression: str, modifier_tokens: Set[str]) -> bool:
    """
    Flags if an expression token conflicts with a known modifier,
    e.g., 'natural' being interpreted both as an expression and a modifier.

    Args:
        expression (str): Candidate expression token.
        modifier_tokens (Set[str]): Set of known modifiers.

    Returns:
        bool: True if conflict exists.
    """
    return expression in modifier_tokens


def remove_subsumed_matches(matches: List[str]) -> List[str]:
    """
    Removes redundant short matches that are:
    - Prefixes of longer tokens (e.g., 'glam' vs 'glamorous')
    - Full-word components inside longer multi-word expressions (e.g., 'glam' in 'soft glam')

    Args:
        matches (List[str]): List of matched phrases.

    Returns:
        List[str]: Filtered list with minimal semantic redundancy.
    """
    filtered = []
    matches = sorted(matches, key=len, reverse=True)

    for candidate in matches:
        is_subsumed = False
        for existing in filtered:
            if candidate == existing:
                continue

            # Case 1: strict prefix in a single-word token (e.g., glam → glamorous)
            if " " not in existing and existing.startswith(candidate):
                is_subsumed = True
                break

            # Case 2: full-word contained in a multi-word expression (e.g., glam in soft glam)
            if re.search(rf'\b{re.escape(candidate)}\b', existing):
                is_subsumed = True
                break

        if not is_subsumed:
            filtered.append(candidate)

    return filtered
def is_negation_conflict(a: str, b: str) -> bool:
    a = normalize_token(a)
    b = normalize_token(b)

    return (
        (a.startswith("no ") and a[3:] == b) or
        (b.startswith("no ") and b[3:] == a)
    )
