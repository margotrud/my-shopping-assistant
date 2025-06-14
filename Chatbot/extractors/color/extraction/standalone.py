# Chatbot/extractors/color/extraction/standalone.py
"""
standalone.py
=============
Extracts valid standalone tone or modifier tokens that were not part of compounds.

This module serves as a second pass after compound extraction,
looking for individual descriptive words that:
- Are not absorbed in compound phrases
- Are valid adjectives or expression-derived tokens
- Match known tone or modifier vocabularies

Features:
---------
- Expression modifier injection (e.g., "romantic" → ["rosy", "soft"])
- Contextual noun blocking (e.g., avoid "lipstick" as a tone)
- Derivative suppression (e.g., avoid "rosy" if "rose" was matched)
- Frequency-aware filtering

Used in:
--------
- `extract_all_descriptive_color_phrases()` pipeline

"""

from typing import List, Set
from collections import Counter
import spacy

from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.token_utils import singularize
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_with_suffix_fallback
from Chatbot.extractors.color.logic.expression_matcher import find_matching_expressions, load_expression_definitions
from Chatbot.extractors.color.shared.constants import COSMETIC_NOUNS

nlp = spacy.load("en_core_web_sm")

def extract_standalone_phrases(
    tokens: List[spacy.tokens.Token],
    token_counts: Counter,
    raw_compounds: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts standalone modifier or tone tokens from input, excluding compound-covered terms.

    This function is the second pass of the color phrase extraction pipeline.
    It identifies valid descriptive terms that:
    - Were not part of compound phrases (e.g., "pink" in "soft pink")
    - Are adjectives (or known color-related tokens)
    - Match known tone or modifier vocabularies
    - Avoid conflict with cosmetic product nouns ("lipstick", "blush")

    It also injects modifiers from matched style expressions (e.g., "romantic" → ["rosy", "soft"]),
    filters duplicates, and applies derivative suppression (e.g., avoid "rosy" if "rose" already matched).

    Args:
        tokens (List[Token]): Parsed spaCy tokens.
        token_counts (Counter): Frequency of each token in original input.
        raw_compounds (List[str]): Tokens absorbed into compound phrases.
        known_tones (Set[str]): Valid tone vocabulary.
        known_modifiers (Set[str]): Valid modifier vocabulary.
        all_webcolor_names (Set[str]): Valid CSS3/XKCD tone names.
        hardcoded_blocked_nouns (Set[str]): Cosmetic nouns to avoid tone tagging in that context.
        debug (bool): If True, prints debug logs.

    Returns:
        List[str]: Unique sorted list of valid standalone modifiers and tones.
    """
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())
    singles = []

    # ───── Load expressions
    expression_definitions = load_expression_definitions()
    trigger_map = {k: v["aliases"] for k, v in expression_definitions.items() if "aliases" in v}

    # ───── Detect expressions
    text_input = " ".join([t.text for t in tokens]).lower()
    matched_expressions = find_matching_expressions(text_input, trigger_map)

    expression_tokens = {
        token for expr in matched_expressions
        for token in expr.lower().split()
    }

    if debug:
        print(f"[🔍 CHECK INPUT] → {text_input}")
        print(f"[📂 TRIGGER MAP KEYS] → {list(trigger_map.keys())}")
        print(f"[📦 MATCHED EXPRESSIONS] → {matched_expressions}")

    cosmetic_found = any(tok.lemma_ in COSMETIC_NOUNS for tok in tokens if tok.pos_ == "NOUN")

    for expr in matched_expressions:
        if cosmetic_found:
            if debug:
                print(f"[❌ BLOCK INJECTION] Cosmetic context active → skipping '{expr}' injection")
            continue

        expression_mods = expression_definitions.get(expr, {}).get("modifiers", [])
        modifiers = [m for m in expression_mods if m in known_modifiers]
        singles.extend(modifiers)

        if expr in known_tones and expr not in singles:
            singles.append(expr)
            if debug:
                print(f"[✅ INJECTED TONE] → '{expr}'")

    for token in tokens:
        text = token.text.lower()
        norm = singularize(text)
        compound_uses = compound_token_counts[text]
        total_uses = token_counts[text]
        resolved = resolve_modifier_with_suffix_fallback(text, known_modifiers)

        if token.pos_ == "NOUN" and token.lemma_ in COSMETIC_NOUNS:
            if debug:
                print(f"[❌ SKIP TOKEN] Cosmetic product mention detected → '{token.text}'")
            continue

        if text in expression_tokens:
            if debug:
                print(f"[❌ SKIP] '{text}' part of expression match → skipped")
            continue

        if (
            (resolved or norm in known_tones)
            and norm not in hardcoded_blocked_nouns
        ):
            if norm in known_tones and token.pos_ == "NOUN" and norm not in all_webcolor_names:
                if debug:
                    print(f"[❌ REJECTED] '{text}' (noun tone not in webcolors)")
                continue

            base = None
            if text.endswith(("y", "ish")):
                base = text.rstrip("y").rstrip("ish")

            if base in known_tones or base in singles:
                if debug:
                    print(f"[❌ SUPPRESSED DERIVATIVE] '{text}' because base tone '{base}' is valid")
                continue

            if total_uses > compound_uses:
                singles.append(text)
                if debug:
                    print(f"[✅ ADDED SINGLE] → '{text}'")

    return sorted(set(singles))


def extract_lone_tones(
    tokens: List[spacy.tokens.Token],
    raw_compounds: List[str],
    known_tones: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts lone tone tokens used as nouns that were not absorbed into compound phrases.

    This function handles edge cases where color tones (e.g., 'pink', 'beige') appear
    alone in the input as noun tokens. It avoids duplicate extraction by ensuring the tone
    wasn’t already used in a compound and doesn’t appear in a restricted noun blocklist.

    Args:
        tokens (List[Token]): spaCy tokens parsed from user input.
        raw_compounds (List[str]): List of previously detected compound phrases.
        known_tones (Set[str]): Valid tone vocabulary.
        hardcoded_blocked_nouns (Set[str]): Known cosmetic nouns to block (e.g., 'lipstick').
        debug (bool): Enable verbose debugging output.

    Returns:
        List[str]: Sorted list of standalone noun tone tokens.
    """
    lone_tones = []
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())

    for t in tokens:
        norm = singularize(t.text.lower())
        if (
            norm in known_tones
            and t.pos_ == "NOUN"
            and norm not in compound_token_counts
            and norm not in hardcoded_blocked_nouns
        ):
            lone_tones.append(norm)
            if debug:
                print(f"[✅ LONE TONE ADDED] → '{norm}'")

    return lone_tones
