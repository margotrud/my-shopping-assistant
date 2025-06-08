"""
Color Phrase Extractor Module
-----------------------------
Extracts descriptive color phrases from user input text segments.

Public interface only:
- extract_all_descriptive_color_phrases()
- extract_phrases_from_segment()
"""

from typing import List, Set

import spacy

from Chatbot.extractors.color import known_tones, all_webcolor_names
from Chatbot.extractors.color.core.tokenizer import tokenize_text
from Chatbot.extractors.color.extract.compound_extraction import extract_compound_phrases
from Chatbot.extractors.color.extract.standalone_extraction import extract_standalone_phrases, extract_lone_tones
from Chatbot.extractors.color.extract.fallback_extraction import extract_suffix_fallbacks



def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool = False
) -> List[str]:
    """
    Extracts descriptive color phrases from input text:
    - Compounds (e.g., "soft pink")
    - Standalone tones or modifiers (e.g., "pink")
    - Fallback suffix tones (e.g., "peachy")

    Args:
        text: User input.
        known_tones: Valid base color tones.
        known_modifiers: Valid modifiers.
        all_webcolor_names: Known CSS3/XKCD color names.
        debug: Enable debug print statements.

    Returns:
        List of extracted phrases (normalized, lowercase, sorted).
    """
    tokens, token_counts = tokenize_text(text)
    blocked_nouns = {"lipstick", "blush"}

    compounds, raw_compounds = extract_compound_phrases(
        tokens, known_tones, known_modifiers, all_webcolor_names, debug
    )
    singles = extract_standalone_phrases(
        tokens, token_counts, compounds, raw_compounds,
        known_tones, known_modifiers, all_webcolor_names, blocked_nouns, debug
    )
    lone_tones = extract_lone_tones(tokens, raw_compounds, known_tones, blocked_nouns, debug)
    suffix_tokens = extract_suffix_fallbacks(tokens, known_tones, known_modifiers, all_webcolor_names, debug)

    phrases = sorted(set(compounds) | set(singles) | set(lone_tones) | set(suffix_tokens))
    if debug:
        print(f"[✅ FINAL PHRASES] {phrases}")
    return phrases


def extract_phrases_from_segment(segment: str, known_modifiers: Set[str]) -> List[str]:
    """
    Wrapper to extract phrases using default tone/color vocabularies.

    Args:
        segment: User input.
        known_modifiers: Modifiers to apply (e.g., {"soft", "bold"}).

    Returns:
        List of extracted phrases.
    """
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=all_webcolor_names,
        debug=False
    )

