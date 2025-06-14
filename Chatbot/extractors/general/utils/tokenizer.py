#Chatbot/extractors/general/utils/tokenizer.py
"""
tokenizer.py
============
Shared spaCy-based text tokenizer and counter utility.

This module provides a central point to tokenize raw user input and extract
both rich token objects and simple word frequency counts. It ensures consistent
lowercasing and prepares data for downstream color phrase parsing, expression
matching, and fuzzy resolution.

Features:
---------
- Consistent lowercase preprocessing
- spaCy token parsing with POS information
- Token frequency counter for scoring and disambiguation

Example:
--------
>>> get_tokens_and_counts("I love soft pink blush, but not bright pink")
tokens → [soft (ADJ), pink (ADJ), blush (NOUN), ...]
counts → {"soft": 1, "pink": 2, "blush": 1, ...}
"""

import spacy
from collections import Counter
from typing import List, Tuple
from spacy.tokens import Token

# Load once globally to avoid re-initialization
_nlp = spacy.load("en_core_web_sm")

def get_tokens_and_counts(text: str) -> Tuple[List[Token], Counter]:
    """
    Tokenizes and lowercases input text, returning both spaCy tokens
    and a frequency Counter of token texts.

    Args:
        text (str): Raw user input.

    Returns:
        Tuple:
            - tokens (List[Token]): spaCy token objects with linguistic features.
            - token_counts (Counter): Frequencies of lowercased token texts.
    """
    doc = _nlp(text.lower())
    tokens = list(doc)
    token_texts = [t.text for t in tokens]
    return tokens, Counter(token_texts)
