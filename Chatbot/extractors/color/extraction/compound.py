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




def extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, debug=True):
    for i in range(len(tokens) - 1):
        raw_mod = tokens[i].text.lower()
        raw_tone = tokens[i + 1].text.lower()

        if debug:
            print(f"\n[🔍 ADJACENT PAIR] '{raw_mod}' + '{raw_tone}'")

        # Modifier resolution: try exact match first
        if raw_mod in known_modifiers or raw_mod in known_tones:
            mod = raw_mod
            if debug:
                print(f"[✅ MODIFIER MATCH] '{raw_mod}' accepted (modifier or tone)")

        elif raw_mod.endswith(("y", "ish")):
            fallback = raw_mod.rstrip("y").rstrip("ish")
            mod = fallback if fallback in known_modifiers else None
            if debug:
                if mod:
                    print(f"[🔁 MODIFIER SUFFIX] '{raw_mod}' → '{mod}'")
                else:
                    print(f"[⛔ MODIFIER FAIL] '{raw_mod}' not found, even after suffix")
        else:
            mod = None
            if debug:
                print(f"[⛔ MODIFIER FAIL] '{raw_mod}' not found")

        # Tone resolution: singularize and check
        tone = singularize(raw_tone)
        if tone in known_tones:
            if debug:
                print(f"[✅ TONE MATCH] '{raw_tone}' → '{tone}' accepted as tone")
        else:
            if debug:
                print(f"[⛔ TONE FAIL] '{raw_tone}' → '{tone}' not in known tones")
            tone = None

        # Final compound
        if mod and tone:
            phrase = f"{mod} {tone}"
            if phrase not in compounds:
                if debug:
                    print(f"[🧱 COMPOUND ADDED] → '{phrase}'")
                compounds.add(phrase)
                raw_compounds.append(phrase)
            else:
                if debug:
                    print(f"[🔁 SKIPPED DUPLICATE] '{phrase}' already added")



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
            return [normalize_token(left), normalize_token(right)]

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
    Attempts to extract compound color phrases from single glued tokens.

    Args:
        tokens: spaCy tokenized Doc
        compounds: Set[str] to collect final compounds (e.g., "dusty rose")
        raw_compounds: List[str] for unfiltered raw compound results
        known_color_tokens: Union of all color vocab (modifiers, tones, webcolors)
        known_modifiers: Set of known modifiers
        known_tones: Set of known tones
        all_webcolor_names: Set of web-safe color names
        debug: Whether to print debug output
    """
    for token in tokens:
        if debug:
            print("[🧪 TOKENS RECEIVED]", [t.text for t in tokens])

        raw = token.text.lower()
        if raw in known_color_tokens:
            print(f"[⛔ SKIP: known token] {raw}")
        elif not raw.isalpha():
            print(f"[⛔ SKIP: non-alpha] {raw}")
        else:
            print(f"[✅ ANALYZE] {raw}")

        if raw in known_color_tokens or not raw.isalpha():
            continue

        if debug:
            print(f"\n🔍 Starting split for: '{raw}'")
            print(f"📦 Augmented vocab size: {len(known_color_tokens)}")

        parts = split_glued_tokens(raw, known_color_tokens, known_modifiers)

        # 🪄 Fallback split if token starts with known color
        if parts == [raw]:
            for tok in known_color_tokens:
                if raw.startswith(tok) and len(tok) >= 4:
                    remainder = raw[len(tok):]
                    if remainder:
                        parts = [tok, remainder]
                        if debug:
                            print(f"🪄 Fallback split at '{tok}': {parts}")
                        break

        if len(parts) != 2:
            continue

        mod_candidate, tone_candidate = parts

        # Direct modifier resolution
        mod = resolve_modifier_token(mod_candidate, known_modifiers, known_tones, is_tone=False, debug=debug)
        is_valid = (
                tone_candidate in known_tones
                or tone_candidate in known_modifiers
                or tone_candidate in all_webcolor_names
        )

        both_valid = (
            mod_candidate in known_modifiers and
            tone_candidate in known_tones
        )

        # Accept tone+tone combinations directly
        both_are_valid_tones = mod_candidate in known_tones and tone_candidate in known_tones

        if both_are_valid_tones or (mod and is_valid) or both_valid:
            compound = f"{mod or mod_candidate} {tone_candidate}"
            if debug:
                print(f"[✅ COMPOUND FOUND] '{raw}' → '{compound}'")
            compounds.add(compound)
            raw_compounds.append(compound)
            continue

        # 💥 Force-add fallback compound
        compound = f"{mod_candidate} {tone_candidate}"
        if debug:
            print(f"[🔥 FORCE ADD] '{raw}' → '{compound}' (fallback accepted)")
        compounds.add(compound)
        raw_compounds.append(compound)


def fallback_split(raw, known_color_tokens, debug=False):
    for i in range(3, len(raw) - 2):
        left, right = normalize_token(raw[:i]), normalize_token(raw[i:])
        if left in known_color_tokens and right in known_color_tokens:
            if debug:
                print(f"🪄 Fallback split at '{left}': ['{left}', '{right}']")
            return f"{left} {right}"
    return None




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

