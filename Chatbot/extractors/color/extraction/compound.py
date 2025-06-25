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
from typing import Set, List

from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token, should_suppress_compound, match_suffix_fallback
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens, singularize
from Chatbot.extractors.color.utils.token_utils import normalize_token


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
        mod = normalize_token(tokens[i].text)
        tone = normalize_token(tokens[i + 1].text)
        if mod in known_modifiers and tone in known_tones:
            phrase = f"{mod} {tone}"
            if phrase not in compounds:
                if debug:
                    print(f"[🧱 COMPOUND] Adjacent pair → '{phrase}'")
                compounds.add(phrase)
                raw_compounds.append(phrase)




def split_tokens_to_parts(text, known_color_tokens):
    print(f"\n[🔍 SPLIT START] Input: '{text}'")

    if "-" in text:
        parts = text.split("-", 1)
        if all(p in known_color_tokens for p in parts):
            return parts

    for i in reversed(range(2, len(text) - 2)):
        left, right = text[:i], text[i:]

        resolved_left = match_suffix_fallback(left, known_color_tokens) or left
        resolved_right = match_suffix_fallback(right, known_color_tokens) or right

        print(f"[🔍 TRY] '{left}' + '{right}' → resolved: '{resolved_left}', '{resolved_right}'")

        if resolved_left in known_color_tokens and resolved_right in known_color_tokens:
            return [left, right]

    return None



def extract_from_glued(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug=False):
    for token in tokens:
        raw = normalize_token(token.text)
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
        text = normalize_token(token.text)
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


def attempt_mod_tone_pair(
    mod_candidate: str,
    tone_candidate: str,
    compounds: set,
    raw_compounds: list,
    known_modifiers: set,
    known_tones: set,
    all_webcolor_names: set,
    debug: bool
):
    if debug:
        print(f"[🔍 MOD CHECK] mod_candidate='{mod_candidate}'")
        print(f"[🔍 TONE CHECK] tone_candidate='{tone_candidate}'")

    mod = resolve_modifier_token(
        mod_candidate,
        known_modifiers,
        known_tones=known_tones,
        allow_fuzzy=False,
        is_tone=False
    )

    if not mod:
        if debug:
            print(f"⛔ Rejected: modifier '{mod_candidate}' is not valid")
        return

    tone = resolve_modifier_token(
        tone_candidate,
        known_modifiers,
        known_tones=known_tones,
        allow_fuzzy=False,
        is_tone=True
    )

    if not tone:
        if tone_candidate in known_tones or tone_candidate in all_webcolor_names:
            tone = tone_candidate
            if debug:
                print(f"[⚠️ FALLBACK] accepted tone='{tone}' via direct match")
        else:
            if debug:
                print(f"⛔ Rejected: '{tone_candidate}' is not a strict tone")
            return

    if (tone.endswith("y") or tone.endswith("ish")) and tone not in known_tones and tone not in all_webcolor_names:
        if debug:
            print(f"⛔ Rejected: tone='{tone}' looks suffixy and is not a real tone")
        return

    if should_suppress_compound(mod, tone):
        if debug:
            print(f"[⛔ SUPPRESSED] {mod} {tone}")
        return

    compound = f"{mod} {tone}"
    compounds.add(compound)
    raw_compounds.append(compound)
    if debug:
        print(f"[✅ COMPOUND DETECTED] → '{compound}'")

