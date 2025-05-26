# Chatbot/extractors/color/phrase_extractor.py

"""
Color Phrase Extractor Module
-----------------------------
Extracts descriptive color phrases from user input text segments.

Features:
- Identifies compound color phrases like 'soft pink'
- Extracts standalone tones or modifiers like 'pink' or 'soft'
- Handles plural forms and suffix-based fallback (e.g., 'peachy')

Uses spaCy for syntactic parsing and token analysis,
and relies on known vocabularies for tones, modifiers, and web color names.
"""

import spacy
from typing import List, Set, Tuple
from collections import Counter

from Chatbot.extractors.color import known_tones, all_webcolor_names

# Load spaCy English model once at module load
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


def extract_phrases_from_segment(
    segment: str,
    known_modifiers: Set[str]
) -> List[str]:
    """
    Extract descriptive color phrases from a given text segment.

    Args:
        segment (str): User input text segment.
        known_modifiers (Set[str]): Recognized modifiers (e.g., {'soft', 'bold'}).

    Returns:
        List[str]: List of descriptive color phrases found.
    """
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=all_webcolor_names,
        debug=False
    )


def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool = False
) -> List[str]:
    """
    Extracts descriptive color phrases from text including:
    - Compound phrases (modifier + tone/webcolor)
    - Standalone tones and modifiers
    - Suffix-based fallback tokens (e.g., 'peachy', 'reddish')

    Args:
        text (str): Input text.
        known_tones (Set[str]): Valid color tones.
        known_modifiers (Set[str]): Valid color modifiers.
        all_webcolor_names (Set[str]): Known CSS3 color names.
        debug (bool): Enable debug output.

    Returns:
        List[str]: Unique sorted list of extracted color-related phrases.
    """
    doc = nlp(text.lower())
    tokens = list(doc)
    token_texts = [t.text for t in tokens]
    token_counts = Counter(token_texts)
    hardcoded_blocked_nouns = {"lipstick"}  # Example noun to exclude

    compounds, raw_compounds = _extract_compounds(tokens, known_tones, known_modifiers, all_webcolor_names, debug)
    singles = _extract_standalone_tokens(tokens, token_counts, compounds, raw_compounds, known_tones, known_modifiers, hardcoded_blocked_nouns, debug)
    lone_tones = _extract_lone_tones(tokens, raw_compounds, known_tones, hardcoded_blocked_nouns, debug)
    suffix_tokens = _extract_suffix_fallback_tokens(tokens, known_tones, known_modifiers, all_webcolor_names, debug)

    all_phrases = sorted(set(compounds) | set(singles) | set(lone_tones) | set(suffix_tokens))

    if debug:
        print(f"Final extracted phrases: {all_phrases}")

    return all_phrases


def _extract_compounds(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> Tuple[Set[str], List[str]]:
    """
    Identify compound color phrases consisting of a modifier followed by a tone or known webcolor.

    Args:
        tokens: List of spaCy tokens from input text.
        known_tones: Set of valid base tones.
        known_modifiers: Set of valid modifiers.
        all_webcolor_names: Set of all CSS3 color names.
        debug: Enable debug output.

    Returns:
        Tuple of:
            - Set of compound phrases (e.g., {"soft pink"}).
            - List of raw compound phrase strings (duplicates allowed).
    """
    compounds = set()
    raw_compounds = []

    for i in range(len(tokens) - 1):
        t1, t2 = tokens[i], tokens[i + 1]
        t1_text = t1.text.lower()
        t2_text = singularize(t2.text.lower())

        if t1_text in known_modifiers and (t2_text in known_tones or t2_text in all_webcolor_names):
            compound = f"{t1.text} {t2.text}"
            compounds.add(compound)
            raw_compounds.append(compound)
            if debug:
                print(f"Compound detected: {compound}")

    return compounds, raw_compounds


def _extract_standalone_tokens(
    tokens: List[spacy.tokens.Token],
    token_counts: Counter,
    compounds: Set[str],
    raw_compounds: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extract standalone tokens which are valid tones or modifiers
    not fully absorbed by compound phrases.

    Args:
        tokens: List of spaCy tokens.
        token_counts: Counter of all token texts.
        compounds: Set of detected compound phrases.
        raw_compounds: List of raw compound phrases.
        known_tones: Valid base tones.
        known_modifiers: Valid modifiers.
        hardcoded_blocked_nouns: Nouns to exclude.
        debug: Enable debug output.

    Returns:
        List of standalone tone/modifier tokens.
    """
    singles = []
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())

    for t in tokens:
        text = t.text.lower()
        norm = singularize(text)
        if (text in known_modifiers or norm in known_tones) and norm not in hardcoded_blocked_nouns:
            if token_counts[text] > compound_token_counts[text]:
                singles.append(text)
                if debug:
                    print(f"Standalone token added: {text}")

    return singles


def _extract_lone_tones(
    tokens: List[spacy.tokens.Token],
    raw_compounds: List[str],
    known_tones: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extract standalone tone tokens which appear as nouns,
    and are not part of any compound phrase.

    Args:
        tokens: List of spaCy tokens.
        raw_compounds: List of raw compound phrases.
        known_tones: Valid base tones.
        hardcoded_blocked_nouns: Nouns to exclude.
        debug: Enable debug output.

    Returns:
        List of lone tone tokens.
    """
    lone_tones = []
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())

    for t in tokens:
        norm = singularize(t.text.lower())
        if norm in known_tones and t.pos_ == "NOUN" and norm not in compound_token_counts and norm not in hardcoded_blocked_nouns:
            lone_tones.append(norm)
            if debug:
                print(f"Lone tone added: {norm}")

    return lone_tones


def _extract_suffix_fallback_tokens(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> List[str]:
    """
    Extract tokens based on suffix fallbacks, e.g., adjectives
    ending with 'ish' or 'y' that are tones or webcolors, excluding modifiers.

    Args:
        tokens: List of spaCy tokens.
        known_tones: Valid base tones.
        known_modifiers: Valid modifiers.
        all_webcolor_names: Known CSS3 color names.
        debug: Enable debug output.

    Returns:
        List of suffix-fallback tokens.
    """
    suffix_tokens = []

    for t in tokens:
        norm = singularize(t.text.lower())
        if (
            t.pos_ == "ADJ"
            and norm.endswith(("ish", "y"))
            and norm not in known_modifiers
            and (norm in known_tones or norm in all_webcolor_names)
        ):
            suffix_tokens.append(norm)
            if debug:
                print(f"Suffix fallback token added: {norm}")

    return suffix_tokens
