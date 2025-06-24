# Chatbot/extractors/general/utils/tokenize.py

"""
tokenize.py
===========

Token counting utility for lowercase, space-separated input.

Used By:
--------
- Expression relevance analysis
- Contextual phrase disambiguation
"""

from typing import Dict


def get_tokens_and_counts(text: str) -> Dict[str, int]:
    """
    Tokenizes input text and returns lowercase token frequency.

    Splits on whitespace only (no punctuation removal or NLP).
    Converts all tokens to lowercase before counting.

    Args:
        text (str): Raw user input or phrase (e.g., "Soft pink and peachy tones")

    Returns:
        Dict[str, int]: Token → frequency mapping.
    """
    tokens = text.lower().split()
    counts = {}

    for token in tokens:
        counts[token] = counts.get(token, 0) + 1

    return counts
