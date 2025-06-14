#Chatbot/extractors/color/extracts/compound_extraction.py
"""
Compound Phrase Extraction
--------------------------
Handles detection of compound color phrases (e.g., "soft pink").

Strategies:
- Adjacent token pairs (soft + pink)
- Split glued tokens (e.g., deepblue → deep blue)
- Fallback combinations with suffix and fuzzy logic
"""

from typing import List, Tuple, Set
import spacy
from Chatbot.extractors.color.old.core import singularize
from Chatbot.extractors.general.old.helpers import split_glued_tokens
from Chatbot.extractors.color.old.core import resolve_modifier_with_suffix_fallback, should_suppress_compound

def extract_compound_phrases(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> Tuple[Set[str], List[str]]:
    """
    Extract compound phrases from adjacent tokens, glued tokens, and split candidates.

    Args:
        tokens: spaCy tokens.
        known_tones: Valid tone tokens.
        known_modifiers: Valid modifier tokens.
        all_webcolor_names: Recognized CSS3/XKCD colors.
        debug: Print debug output.

    Returns:
        Tuple of:
            - Set of compound phrases (e.g., {'soft pink'})
            - List of raw compounds for usage tracking
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

        mod = resolve_modifier_with_suffix_fallback(raw_mod, known_modifiers)
        tone = resolve_modifier_with_suffix_fallback(raw_tone, known_modifiers, known_tones, allow_fuzzy=False, is_tone=True)

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


def extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug):
    """
        Extracts compound color phrases by attempting to split glued tokens into valid modifier-tone pairs.

        This function handles cases where user input includes compound tokens without spaces
        (e.g., "deepblue", "brightred"). It splits each adjacent token into known color components
        and checks for valid (modifier + tone) combinations. Suppression rules are applied to
        avoid invalid combinations, and valid compounds are recorded.

        Args:
            tokens (List[spacy.tokens.Token]): List of parsed tokens from input text.
            compounds (Set[str]): Set to store deduplicated compound phrases.
            raw_compounds (List[str]): List to store all compound phrases (including duplicates).
            known_color_tokens (Set[str]): Combined set of valid tone and modifier tokens for splitting.
            known_modifiers (Set[str]): Set of recognized color modifier terms.
            known_tones (Set[str]): Set of valid base color tone names.
            all_webcolor_names (Set[str]): Set of recognized web color names (CSS/XKCD).
            debug (bool): If True, prints debug output for each match attempt and result.
        """
    for i in range(len(tokens) - 1):
        t1 = tokens[i].text.lower()
        t2 = singularize(tokens[i + 1].text.lower())

        parts1 = split_glued_tokens(t1, known_color_tokens)
        parts2 = split_glued_tokens(t2, known_color_tokens)

        for mod_candidate in parts1:
            mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers)
            for tone_candidate in parts2:
                if tone_candidate in known_tones or tone_candidate in all_webcolor_names:
                    if should_suppress_compound(mod_candidate, mod, tone_candidate, known_tones):
                        if debug:
                            print(f"[⛔ SUPPRESSED FALLBACK] {mod} {tone_candidate}")
                        continue
                    compound = f"{mod} {tone_candidate}"
                    compounds.add(compound)
                    raw_compounds.append(compound)
                    if debug:
                        print(f"[✅ COMPOUND DETECTED] → '{compound}'")


def extract_from_glued(tokens, compounds, raw_compounds, token_texts, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug):
    """
       Extracts compound color phrases from single tokens that may contain glued modifier-tone combinations.

       This function handles edge cases where users enter glued words without spaces (e.g., "softpink", "boldred").
       It attempts to split such tokens into a modifier and tone using known color vocabularies,
       verifies their validity, and adds them to the compound set if they haven’t been detected already.

       Args:
           tokens (List[spacy.tokens.Token]): List of parsed tokens from the input text.
           compounds (Set[str]): Set collecting deduplicated compound phrases.
           raw_compounds (List[str]): List collecting all raw compound phrases (with possible duplicates).
           token_texts (List[str]): Original list of token text values for verification.
           known_color_tokens (Set[str]): Combined set of known tones and modifiers used for splitting.
           known_modifiers (Set[str]): Set of valid color modifier terms.
           known_tones (Set[str]): Set of valid base tone names.
           all_webcolor_names (Set[str]): Set of known web color names (CSS/XKCD).
           debug (bool): If True, prints verbose debug output for tracing match logic and rejections.
       """
    for token in tokens:
        raw = singularize(token.text.lower())
        if any(raw in c.replace(" ", "") for c in compounds):
            if debug:
                print(f"[⛔ SKIPPED GLUED TOKEN] '{raw}' already detected")
            continue

        parts = split_glued_tokens(raw, known_color_tokens)
        if debug:
            print(f"[🔬 SPLIT GLUED TOKEN] '{raw}' → {parts}")
        if len(parts) != 2:
            continue

        mod_candidate, tone_candidate = parts
        mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers, known_tones)
        is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names
        original_form = mod_candidate + tone_candidate

        if mod and is_valid and original_form in token_texts:
            compound = f"{mod} {tone_candidate}"
            compounds.add(compound)
            raw_compounds.append(compound)
            if debug:
                print(f"[✅ GLUED COMPOUND] '{raw}' → '{compound}'")
        elif debug:
            print(f"[⛔ REJECTED GLUED COMPOUND] '{raw}' not valid")

