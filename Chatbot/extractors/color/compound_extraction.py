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
from Chatbot.extractors.color.tokenizer import singularize
from Chatbot.extractors.general.helpers import split_glued_tokens
from Chatbot.extractors.color.modifier_resolution import resolve_modifier_with_suffix_fallback, should_suppress_compound

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
