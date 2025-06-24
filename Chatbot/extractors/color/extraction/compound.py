#Chatbot/extractors/color/extraction/compound.py

"""
compound.py
===========

Handles compound color phrase extraction logic.

Functions:
- extract_compound_phrases
- extract_from_adjacent
- extract_from_split
- extract_from_glued
- split_tokens_to_parts
- attempt_mod_tone_pair
"""
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens, singularize

def extract_compound_phrases(
    tokens,
    compounds,
    raw_compounds,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    debug=False
):
    extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, debug)
    extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)
    extract_from_glued(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)


def extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, debug=False):
    for i in range(len(tokens) - 1):
        mod = tokens[i].text.lower()
        tone = tokens[i + 1].text.lower()
        if mod in known_modifiers and tone in known_tones:
            phrase = f"{mod} {tone}"
            if phrase not in compounds:
                if debug:
                    print(f"[🧱 COMPOUND] Adjacent pair → '{phrase}'")
                compounds.add(phrase)
                raw_compounds.append(phrase)



def split_tokens_to_parts(text):
    if "-" in text:
        return text.split("-", 1)
    for i in range(2, len(text) - 2):
        left, right = text[:i], text[i:]
        if left.isalpha() and right.isalpha():
            return [left, right]
    return None

def extract_from_glued(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug=False):
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
        mod = resolve_modifier_token(mod_candidate, known_modifiers, known_tones)
        is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names
        original_form = mod_candidate + tone_candidate

        if mod and is_valid and original_form in raw:
            compound = f"{mod} {tone_candidate}"
            if debug:
                print(f"[🧪 GLUED COMPOUND] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)


def extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug=False):
    for token in tokens:
        text = token.text.lower()
        if text in known_color_tokens:
            continue
        if any(text in c.replace(" ", "") for c in compounds):
            continue

        parts = split_tokens_to_parts(text)
        if not parts:
            continue

        mod_candidate, tone_candidate = parts
        mod = resolve_modifier_token(mod_candidate, known_modifiers, known_tones)
        is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names

        if mod and is_valid:
            compound = f"{mod} {tone_candidate}"
            if debug:
                print(f"[🧪 SPLIT COMPOUND] '{text}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)


def attempt_mod_tone_pair(mod_candidate, tone_candidate, known_modifiers, known_tones):
    if mod_candidate in known_modifiers and tone_candidate in known_tones:
        return f"{mod_candidate} {tone_candidate}"
    return None