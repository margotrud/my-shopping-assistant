# Chatbot/extractors/color/utils/token_utils.py

"""
token_utils.py
==============

Token-level normalization and recovery utilities.

Used By:
--------
- Compound extraction
- Glued token recovery
- Plural normalization of cosmetic nouns
"""

from typing import Set, List, Tuple


def split_glued_tokens(
    token: str,
    known_tokens: Set[str]
) -> List[str]:
    """
    Attempts to split a glued token (e.g. 'dustyrose') into two known color-related parts.

    Logic:
    - Iterates through all possible 2-part splits of the token.
    - Returns the first valid [modifier, tone] pair where both parts are in known_tokens.

    Args:
        token (str): Input fused token (e.g. 'deepnude').
        known_tokens (Set[str]): Vocabulary of valid tones and modifiers.

    Returns:
        List[str]: Two-part list if valid split found, else empty list.
    """
    token = token.lower()
    for i in range(3, len(token) - 2):
        part1, part2 = token[:i], token[i:]
        if part1 in known_tokens and part2 in known_tokens:
            return [part1, part2]
    return []


def singularize(word: str) -> str:
    """
    Converts plural cosmetic nouns to singular form using simple heuristics.

    - 'lipsticks' → 'lipstick'
    - 'glosses' → 'gloss'
    - 'blushes' → 'blush'

    Args:
        word (str): Input word, possibly plural.

    Returns:
        str: Singularized version if transformation applies, else unchanged.
    """
    word = word.lower()
    if word.endswith("es") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word
