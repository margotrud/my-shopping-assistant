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
from fuzzywuzzy import fuzz
from Chatbot.extractors.color.shared.constants import SEMANTIC_CONFLICTS



def normalize_token(token: str) -> str:
    """
    Standardizes token for comparison: lowercase and strip whitespace.

    Args:
        token (str): Input string.

    Returns:
        str: Normalized token.
    """
    return token.lower().strip()


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
    input_text = input_text.lower()

    for alias in aliases:
        alias = alias.lower()

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
    score = fuzz.partial_ratio(alias.lower(), input_text.lower())
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
    a_norm = a.lower().strip()
    b_norm = b.lower().strip()

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
    Removes overlapping short matches when longer ones exist.

    E.g., from ['glamorous', 'glam'], keep only 'glamorous'.

    Args:
        matches (List[str]): List of matched tokens.

    Returns:
        List[str]: Filtered list with minimal redundancy.
    """
    filtered = []
    matches = sorted(matches, key=len, reverse=True)
    for m in matches:
        if not any(m in other and m != other for other in filtered):
            filtered.append(m)
    return filtered


def is_negation_conflict(a: str, b: str) -> bool:
    a = a.strip().lower()
    b = b.strip().lower()

    return (
        (a.startswith("no ") and a[3:] == b) or
        (b.startswith("no ") and b[3:] == a)
    )
