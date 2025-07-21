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

from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed
from Chatbot.extractors.color.logic.compound_rule import is_blocked_modifier_tone_pair
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token, should_suppress_compound, match_suffix_fallback
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens, singularize
from Chatbot.extractors.color.utils.token_utils import normalize_token

import spacy
nlp = spacy.load("en_core_web_sm")
from spacy.tokens import Token as SpacyToken


def extract_compound_phrases(
    tokens,
    compounds,
    raw_compounds,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    raw_text: str = "",
    debug: bool = False
):
    """
    Orchestrates compound color phrase extraction by applying:
    - extract_from_adjacent()
    - extract_from_split()
    - extract_from_glued()

    If none of these resolve a valid compound, a fallback fuzzy match is attempted.
    """
    # ✅ Normalize hyphenated input before tokenization
    raw_text = raw_text.replace("-", " ") if raw_text else ""
    if raw_text:
        tokens = nlp(raw_text)

    # 🔍 Main extraction passes
    extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, debug)
    extract_from_split(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)
    extract_from_glued(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)

    # 🩹 Fallback: attempt to resolve missed compound pairs
    for i in range(len(tokens) - 1):
        left = normalize_token(tokens[i].text)
        right = normalize_token(tokens[i + 1].text)

        if left in known_modifiers or left in known_tones or len(left) < 3:
            continue
        if right not in known_tones or not right.isalpha():
            continue

        mod = resolve_modifier_token(
            word=left,
            known_modifiers=known_modifiers,
            known_tones=known_tones,
            allow_fuzzy=True,
            is_tone=False,
            debug=debug,
        )
        if mod and f"{mod} {right}" not in compounds:
            compounds.add(f"{mod} {right}")
            raw_compounds.append((mod, right))
            if debug:
                print(f"[🩹 FALLBACK PATCH] {left}+{right} → {mod} {right}")

    # ⛔ Filter out blocked tone-modifier pairs
    blocked = {
        (m, t)
        for pair in raw_compounds
        if isinstance(pair, tuple) and len(pair) == 2
        for m, t in [pair]
        if is_blocked_modifier_tone_pair(m, t)
    }

    for mod, tone in blocked:
        compound = f"{mod} {tone}"
        if compound in compounds:
            compounds.discard(compound)
        raw_compounds.remove((mod, tone))
        if debug:
            print(f"[⛔ BLOCKED PAIR REMOVED] '{compound}'")


def extract_from_adjacent(
    tokens,
    compounds,
    raw_compounds,
    known_modifiers,
    known_tones,
    debug=True
):
    """
    Extracts compound color phrases from adjacent token pairs (e.g., "muted rose").
    Accepts a modifier followed by a tone.
    """
    for i in range(len(tokens) - 1):
        raw_mod = tokens[i].text.lower()
        raw_tone = singularize(tokens[i + 1].text.lower())

        if debug:
            print(f"\n[🔍 ADJACENT PAIR] '{raw_mod}' + '{raw_tone}'")

        mod = resolve_modifier_token(raw_mod, known_modifiers, known_tones, is_tone=False, debug=debug)
        tone = raw_tone if raw_tone in known_tones else None

        if mod and tone:
            phrase = f"{mod} {tone}"
            if phrase not in compounds:
                if debug:
                    print(f"[✅ ADJACENT COMPOUND ADDED] → '{phrase}'")
                compounds.add(phrase)
                raw_compounds.append(phrase)



def split_tokens_to_parts(
    text: str,
    known_color_tokens: set,
    debug: bool = False
) -> list[str] | None:
    """
    Attempts to split a single token into two known color components.

    Handles cases like:
    - 'dusty-rose' → ['dusty', 'rose']
    - 'softpink' → ['soft', 'pink']

    Args:
        text (str): The raw glued token.
        known_color_tokens (set): All known color vocab.
        debug (bool): If True, enables detailed logging.

    Returns:
        list[str] | None: A [modifier, tone] split or None if invalid.
    """
    if debug:
        print(f"\n[🔍 SPLIT START] Input: '{text}'")

    # First check for dash-based splits
    if "-" in text:
        parts = text.split("-", 1)
        if all(part in known_color_tokens for part in parts):
            if debug:
                print(f"[✅ DASH SPLIT] '{text}' → {parts}")
            return parts

    # Try recursive character-level splits
    for i in reversed(range(2, len(text) - 2)):
        left, right = text[:i], text[i:]

        resolved_left = match_suffix_fallback(left, known_color_tokens) or left
        resolved_right = match_suffix_fallback(right, known_color_tokens) or right

        if debug:
            print(f"[🔍 TRY] '{left}' + '{right}' → resolved: '{resolved_left}', '{resolved_right}'")

        if resolved_left in known_color_tokens and resolved_right in known_color_tokens:
            left_norm = normalize_token(left)
            right_norm = normalize_token(right)
            if debug:
                print(f"[✅ SPLIT SUCCESS] '{text}' → ['{left_norm}', '{right_norm}']")
            return [left_norm, right_norm]

    if debug:
        print(f"[⛔ NO SPLIT FOUND] '{text}'")
    return None

def extract_from_glued(
    tokens,
    compounds,
    raw_compounds,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    debug=True
):
    """
    Extracts compounds from single glued tokens (e.g., 'dustyrose', 'subtlealmond', 'purepearl').

    Accepts:
    - modifier + tone (e.g., 'subtlealmond')
    - tone + tone     (e.g., 'greylavender')
    - known_modifier + tone (fallback)
    - modifier + modifier (e.g., 'purepearl')
    """
    for token in tokens:
        raw = token.text.lower()

        if not raw.isalpha() or raw in known_color_tokens:
            if debug:
                print(f"[⛔ SKIP] Token '{raw}' is known or non-alpha")
            continue

        parts = split_glued_tokens(raw, known_color_tokens, known_modifiers)

        if not parts or len(parts) != 2:
            continue

        mod_candidate, tone_candidate = parts

        mod = resolve_modifier_token(mod_candidate, known_modifiers, known_tones, is_tone=False, debug=debug)
        if tone_candidate in known_tones or tone_candidate in all_webcolor_names:
            is_valid_tone = True
        elif tone_candidate.endswith("y") and tone_candidate[:-1] in known_tones:
            tone_candidate = tone_candidate[:-1]
            is_valid_tone = True
        elif tone_candidate.endswith("ish") and tone_candidate[:-3] in known_tones:
            tone_candidate = tone_candidate[:-3]
            is_valid_tone = True
        else:
            is_valid_tone = False
        tone_pair = mod_candidate in known_tones and tone_candidate in known_tones
        mod_fallback = mod_candidate in known_modifiers and is_valid_tone
        mod_mod_pair = mod_candidate in known_modifiers and tone_candidate in known_modifiers

        # 1. modifier resolved + valid tone
        if mod and is_valid_tone:
            compound = f"{mod} {tone_candidate}"
            if debug:
                print(f"[✅ GLUED MOD+TONE] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)
            continue

        # 2. known modifier + known tone (fallback)
        elif mod_fallback:
            compound = f"{mod_candidate} {tone_candidate}"
            if debug:
                print(f"[✅ GLUED MOD+TONE (fallback)] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)
            continue

        # 3. tone + tone
        elif tone_pair:
            compound = f"{mod_candidate} {tone_candidate}"
            if debug:
                print(f"[✅ GLUED TONE+TONE] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)
            continue

        # 4. modifier + modifier
        elif mod_mod_pair:
            compound = f"{mod_candidate} {tone_candidate}"
            if debug:
                print(f"[✅ GLUED MOD+MOD] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)
            continue


def extract_from_split(
    tokens,
    compounds,
    raw_compounds,
    known_color_tokens,
    known_modifiers,
    known_tones,
    all_webcolor_names,
    debug=False
):
    """
    Attempts to recover compound phrases from mis-tokenized or corrupted inputs.
    Works on tokens like 'dustyrose', 'taupeybeige', etc.
    """
    for token in tokens:
        text = token.text.lower()
        if text in known_color_tokens or any(text in c.replace(" ", "") for c in compounds):
            continue

        if debug:
            print(f"\n[🔍 SPLIT CANDIDATE] '{text}'")

        parts = split_tokens_to_parts(text, known_color_tokens)
        if not parts or len(parts) != 2:
            if debug:
                print(f"[⛔ INVALID SPLIT] {parts}")
            continue

        mod_candidate, tone_candidate = parts
        mod = resolve_modifier_token(mod_candidate, known_modifiers, known_tones, is_tone=False, debug=debug)

        is_valid_tone = tone_candidate in known_tones or tone_candidate in all_webcolor_names

        if mod and is_valid_tone:
            compound = f"{mod} {tone_candidate}"
            if debug:
                print(f"[✅ SPLIT COMPOUND] '{text}' → '{compound}'")
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

    # ─── Try resolving modifier
    mod = resolve_modifier_token(
        mod_candidate,
        known_modifiers,
        known_tones=known_tones,
        allow_fuzzy=False,
        is_tone=False
    )

    if not mod:
        # ✅ CORRECT: simplify mod_candidate, not tone_candidate
        simplified = simplify_phrase_if_needed(mod_candidate, known_modifiers, known_tones)
        if simplified:
            mod = simplified[0].split()[0]
            if mod not in known_modifiers and mod not in known_tones:
                if debug:
                    print(f"⛔ Rejected: simplified modifier '{mod}' not in known sets")
                return
            if debug:
                print(f"[✅ SIMPLIFIED MODIFIER] '{mod_candidate}' → '{mod}'")
        else:
            if debug:
                print(f"⛔ Rejected: modifier '{mod_candidate}' is not valid")
            return

    # ─── Try resolving tone
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
            # Try fallback simplification for tone
            simplified = simplify_phrase_if_needed(tone_candidate, known_modifiers, known_tones)
            if debug:
                print(f"[🧪 RAW SIMPLIFIED] {simplified}")
            if simplified:
                tone = simplified[0].split()[-1]
                if tone not in known_tones and tone not in all_webcolor_names:
                    if debug:
                        print(f"⛔ Rejected: simplified tone '{tone}' not valid")
                    return
                if debug:
                    print(f"[✅ SIMPLIFIED TONE] '{tone_candidate}' → '{tone}'")
            else:
                if debug:
                    print(f"⛔ Rejected: '{tone_candidate}' is not a strict tone")
                return

    # ─── Filter suffixy fake tones unless they're real
    if (tone.endswith("y") or tone.endswith("ish")) and tone not in known_tones and tone not in all_webcolor_names:
        if debug:
            print(f"⛔ Rejected: tone='{tone}' looks suffixy and is not a real tone")
        return

    # ─── Final suppression rule
    if should_suppress_compound(mod, tone):
        if debug:
            print(f"[⛔ SUPPRESSED] {mod} {tone}")
        return

    compound = f"{mod} {tone}"
    compounds.add(compound)
    raw_compounds.append(compound)
    if debug:
        print(f"[✅ COMPOUND DETECTED] → '{compound}'")
