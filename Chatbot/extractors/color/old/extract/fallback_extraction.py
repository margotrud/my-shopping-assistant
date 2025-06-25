#Chatbot/extractors/color/extract/fallback_extraction.py
"""
Fallback Extraction: Suffix Tokens
----------------------------------
Extracts tones from adjectives ending with suffixes like 'y' or 'ish',
when not captured in compound or standalone logic.

Example: 'peachy', 'reddish'
"""

from typing import List, Set
import spacy
from Chatbot.extractors.color.old.core import singularize
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def extract_suffix_fallbacks(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts fallback tone tokens based on suffixes (e.g., 'peachy').

    Args:
        tokens: spaCy tokenized input.
        known_tones: Set of valid base tones.
        known_modifiers: Modifier vocabulary (to avoid misclassification).
        all_webcolor_names: Known CSS/XKCD color names.
        debug: Enable debug output.

    Returns:
        List of valid suffix-based tone tokens.
    """
    results = []

    for t in tokens:
        norm = normalize_token(t.text)

        if (
            t.pos_ == "ADJ"
            and norm.endswith(("y", "ish"))
            and norm not in known_modifiers
            and (norm in known_tones or norm in all_webcolor_names)
        ):
            results.append(norm)
            if debug:
                print(f"[✅ SUFFIX FALLBACK ADDED] → '{norm}'")

    return results
