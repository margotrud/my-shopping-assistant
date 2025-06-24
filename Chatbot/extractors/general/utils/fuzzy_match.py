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
from rapidfuzz import fuzz


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
    """
    Computes fuzzy partial match score between two tokens.

    Args:
        a (str): First string.
        b (str): Second string.

    Returns:
        float: Fuzzy match score (0–100).
    """
    return fuzz.partial_ratio(normalize_token(a), normalize_token(b))


def match_expression_aliases(input_text: str, aliases: List[str], threshold: int = 85) -> bool:
    """
    Determines if user input fuzzily matches any known expression alias.

    Args:
        input_text (str): Lowercased user input (e.g., "soft glam").
        aliases (List[str]): Alias tokens for an expression.
        threshold (int): Match threshold (default: 85).

    Returns:
        bool: True if any alias matches, else False.
    """
    for alias in aliases:
        score = fuzz.partial_ratio(alias.lower(), input_text.lower())
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


def is_strong_fuzzy_match(a: str, b: str, threshold: int = 88) -> bool:
    """
    Returns True if a and b are strong fuzzy matches.

    Args:
        a (str): First token.
        b (str): Second token.
        threshold (int): Minimum score required.

    Returns:
        bool: True if fuzzy match is strong.
    """
    return fuzzy_token_match(a, b) >= threshold


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
