# Chatbot/extractors/color/utils/token_utils.py
"""
token_utils.py
==============
Token-level text utilities used throughout the color extraction pipeline.

This module provides low-level, language-agnostic functions that manipulate
and analyze individual tokens — especially useful for cosmetic and fashion-related
text parsing where user inputs often include creative or informal structures.

Key Features:
-------------
- Glued token decomposition: Handles cases like "deepblue" → ["deep", "blue"]
- Designed for integration into higher-level phrase extraction modules
- Lightweight and fully standalone — no dependencies beyond the standard library

Why This Module Exists:
-----------------------
In user-generated input, it's common to encounter color descriptions without
spaces or in non-standard formats (e.g., "lightpeach", "softpink", "rosybrown").
These are not picked up by standard NLP tokenizers. This utility enables
recognizing and extracting valid color components from such inputs.

Example Use Cases:
------------------
Used by:
- compound phrase extractor to parse adjacent or glued modifiers + tones
- fallback extractors to recognize embedded tokens in unknown compounds

Example:
--------
>>> known = {"soft", "pink", "light", "blue", "nude"}
>>> split_glued_tokens("lightblue", known)
['light', 'blue']

>>> split_glued_tokens("softpink", known)
['soft', 'pink']

>>> split_glued_tokens("nude", known)
['nude']

>>> split_glued_tokens("shinyglam", known)
[]
"""


from typing import List, Set

def split_glued_tokens(token: str, known_tokens: Set[str]) -> List[str]:
    """
    Splits a glued token into known sub-tokens using backtracking.

    Args:
        token (str): The glued token (e.g., 'deepblue', 'softpink')
        known_tokens (Set[str]): Set of known color-related tokens

    Returns:
        List[str]: A list of sub-tokens if a valid split is found, else empty list.
    """
    token = token.lower()
    n = len(token)
    results = []

    def backtrack(start: int, path: List[str]):
        if start == n:
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            piece = token[start:end]
            if piece in known_tokens:
                path.append(piece)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])

    if results and len(results[0]) > 1:
        return results[0]
    elif token in known_tokens:
        return [token]
    return []


def singularize(word: str) -> str:
    """
    Heuristically converts simple plural forms to singular
    by stripping trailing 's' (unless ending in 'ss').

    Args:
        word (str): Input word (e.g., 'pinks', 'dresses').

    Returns:
        str: Singular form if applicable, else original.
    """
    if len(word) >= 4 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

