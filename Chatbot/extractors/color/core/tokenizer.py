"""
Tokenizer Utilities
-------------------
Provides text normalization and tokenization for color phrase analysis.

Functions:
- singularize(): Handles plural normalization.
- tokenize_text(): Tokenizes input using spaCy and returns token objects + counts.
"""

import spacy
from collections import Counter
from typing import List, Tuple

nlp = spacy.load("en_core_web_sm")


def singularize(word: str) -> str:
    """
    Convert plural words ending in 's' (but not 'ss') to singular.

    Args:
        word (str): Input word.

    Returns:
        str: Singular form if plural, else original word.
    """
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenize_text(text: str) -> Tuple[List[spacy.tokens.Token], Counter]:
    """
    Tokenizes and lowers input text, returning token objects and word counts.

    Args:
        text (str): Raw user input.

    Returns:
        Tuple of:
            - tokens (List[Token]): spaCy token objects.
            - token_counts (Counter): Frequency counts for each token.
    """
    doc = nlp(text.lower())
    tokens = list(doc)
    token_texts = [t.text for t in tokens]
    return tokens, Counter(token_texts)
