#Chatbot/extractors/color/extraction/compound.py

"""
compound.py
===========

Compound Color Phrase Extraction
--------------------------------

This module handles low-level logic for identifying compound color phrases
within a tokenized user input stream. Compound phrases are multi-word or
glued-together combinations of a modifier and a tone, such as:

- "soft pink"
- "mutedrose"
- "deep nude"

The goal is to detect and normalize these structures reliably, even when
tokenization or user formatting is irregular.

Key Capabilities:
-----------------
- Identifies adjacent token pairs (e.g., ADJ + NOUN) as color compounds
- Deconstructs glued tokens like "dustyrose" into separate parts
- Recovers partially split or mis-tokenized color fragments
- Returns structured compound phrases and raw components for post-filtering

Used By:
--------
- `extract_color_phrases()` and `standalone.py` for avoiding duplication
- Phrase aggregation logic during color parsing
- Color sentiment and expression scoring modules

Core Function:
--------------
- `extract_compound_phrases()`: Main entry point combining adjacent, split,
  and glued phrase extraction routines.

Dependencies:
-------------
- Known vocabularies: tones, modifiers, CSS3/XKCD color names
- Helper functions:
    - `extract_from_adjacent()`
    - `extract_from_split()`
    - `extract_from_glued()`

Example:
--------
>>> text = "I'm looking for soft pink or dustyrose"
>>> tokens = nlp(text)
>>> extract_compound_phrases(tokens, known_tones, known_modifiers, webcolors, debug=False)
({"soft pink", "dusty rose"}, ["soft pink", "dusty rose"])
"""
from typing import List, Set, Tuple, Optional

import spacy

from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token, should_suppress_compound
from Chatbot.extractors.color.utils.token_utils import singularize, split_glued_tokens


def extract_compound_phrases(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> Tuple[Set[str], List[str]]:
    """
    Extracts valid compound color phrases from user input tokens.

    This function scans spaCy-parsed tokens to identify multi-word or glued-together
    color phrases composed of known modifiers and tones. It runs three sub-routines:
    - Adjacent token matching (e.g., "soft pink")
    - Glued token splitting (e.g., "dustyrose")
    - Partial compound recovery from token fragments

    Args:
        tokens (List[Token]): Tokenized user input.
        known_tones (Set[str]): Valid tone vocabulary (e.g., "pink", "coral").
        known_modifiers (Set[str]): Known modifier terms (e.g., "muted", "dusty").
        all_webcolor_names (Set[str]): Extended color vocab (CSS3 + XKCD).
        debug (bool): Whether to print debug output for inspection.

    Returns:
        Tuple:
            - compounds (Set[str]): Final compound phrases found (e.g., {"muted rose"}).
            - raw_compounds (List[str]): List of accepted raw compounds, used in filtering.

    Example:
        >>> tokens = nlp("I like soft pink and mutedrose")
        >>> extract_compound_phrases(tokens, tones, modifiers, webcolors, False)
        ({"soft pink", "muted rose"}, ["soft pink", "muted rose"])
    """
    compounds = set()
    raw_compounds = []
    known_color_tokens = known_modifiers | known_tones | all_webcolor_names
    token_texts = [t.text.lower() for t in tokens]

    extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, all_webcolor_names, debug)
    extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)
    extract_from_glued(tokens, compounds, raw_compounds, token_texts, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)

    return compounds, raw_compounds

def extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, all_webcolor_names, debug):
    """
        Extracts compound color phrases by analyzing adjacent token pairs.

        This function scans adjacent tokens in the input, attempting to match a modifier followed
        by a tone (or web color name). It uses suffix fallback and optional fuzzy logic to resolve
        modifiers and tones, then constructs compound phrases like "soft pink" or "muted beige".
        Suppression rules are applied to avoid invalid or redundant combinations.

        Args:
            tokens (List[spacy.tokens.Token]): List of spaCy-parsed tokens from input text.
            compounds (Set[str]): Set to store valid compound phrases.
            raw_compounds (List[str]): List to store raw compound phrases (with duplicates allowed).
            known_modifiers (Set[str]): Set of valid modifier terms.
            known_tones (Set[str]): Set of recognized base tone names.
            all_webcolor_names (Set[str]): Set of valid web color names (CSS/XKCD).
            debug (bool): If True, prints verbose debug output for each step.
        """
    for i in range(len(tokens) - 1):
        raw_mod = tokens[i].text.lower()
        raw_tone = singularize(tokens[i + 1].text.lower())

        mod = resolve_modifier_token(raw_mod, known_modifiers)
        tone = resolve_modifier_token(raw_tone, known_modifiers, known_tones, allow_fuzzy=False, is_tone=True)

        if mod and tone and (tone in known_tones or tone in all_webcolor_names):
            if should_suppress_compound(raw_mod, mod, tone, known_tones):
                if debug:
                    print(f"[⛔ SUPPRESSED] {mod} {tone}")
                continue
            compound = f"{mod} {tone}"
            compounds.add(compound)
            raw_compounds.append(compound)
            if debug:
                print(f"[✅ WHOLE TOKEN COMPOUND DETECTED] → '{compound}'")

def split_tokens_to_parts(t1: str, t2: str, known_color_tokens: Set[str], debug: bool):
    parts1 = split_glued_tokens(t1, known_color_tokens)
    parts2 = split_glued_tokens(singularize(t2), known_color_tokens)
    if debug:
        print(f"[🧪 SPLIT CHECK] '{t1}' → {parts1}")
        print(f"[🧪 SPLIT CHECK] '{t2}' → {parts2}")
    return parts1, parts2


def resolve_valid_modifier(mod_candidate: str, known_modifiers, known_tones, debug: bool) -> Optional[str]:
    if mod_candidate in known_tones:
        if debug:
            print(f"[⛔ SKIP MODIFIER] '{mod_candidate}' is actually a tone")
        return None

    mod = resolve_modifier_token(
        mod_candidate,
        known_modifiers,
        known_tones=known_tones,
        is_tone=False,
        allow_fuzzy=True
    )

    if not mod and debug:
        print(f"⛔ Invalid modifier from '{mod_candidate}'")
    return mod

def attempt_mod_tone_pair(
    mod_candidate: str,
    mod: str,
    tone_candidate: str,
    compounds: Set[str],
    raw_compounds: List[str],
    known_modifiers: Set[str],
    known_tones: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
):
    if debug:
        print(f"[🔍 TONE CHECK] tone_candidate='{tone_candidate}'")

    tone = resolve_modifier_token(
        tone_candidate,
        known_modifiers,
        known_tones=known_tones,
        allow_fuzzy=False,
        is_tone=True
    )

    if not tone:
        if debug:
            print(f"⛔ Rejected: '{tone_candidate}' is not a strict tone")
        return

    if tone.endswith("y") or tone.endswith("ish"):
        if debug:
            print(f"⛔ Rejected: tone='{tone}' looks suffixy")
        return

    if should_suppress_compound(mod_candidate, mod, tone, known_tones):
        if debug:
            print(f"[⛔ SUPPRESSED] {mod} {tone}")
        return

    compound = f"{mod} {tone}"
    compounds.add(compound)
    raw_compounds.append(compound)
    if debug:
        print(f"[✅ COMPOUND DETECTED] → '{compound}'")


def extract_from_split(
    tokens,
    compounds,
    raw_compounds,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    debug
):
    for i in range(len(tokens) - 1):
        t1 = tokens[i].text.lower()
        t2 = tokens[i + 1].text.lower()
        if debug:
            print(f"[🧪 DEBUG] Trying to split '{t1}' → {split_glued_tokens(t1, known_color_tokens)}")

        parts1, parts2 = split_tokens_to_parts(t1, t2, known_color_tokens, debug)

        if len(parts1) == 2:
            internal_mod_candidate, internal_tone_candidate = parts1

            mod = resolve_valid_modifier(internal_mod_candidate, known_modifiers, known_tones, debug)
            if mod:
                attempt_mod_tone_pair(
                    internal_mod_candidate,
                    mod,
                    internal_tone_candidate,
                    compounds,
                    raw_compounds,
                    known_modifiers,
                    known_tones,
                    all_webcolor_names,
                    debug
                )

        for mod_candidate in parts1:
            mod = resolve_valid_modifier(mod_candidate, known_modifiers, known_tones, debug)
            if not mod:
                continue

            for tone_candidate in parts2:
                attempt_mod_tone_pair(
                    mod_candidate,
                    mod,
                    tone_candidate,
                    compounds,
                    raw_compounds,
                    known_modifiers,
                    known_tones,
                    all_webcolor_names,
                    debug
                )
