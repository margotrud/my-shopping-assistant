"""
Standalone Token Extraction
---------------------------
Handles:
- Valid standalone modifiers or tones (e.g., "soft", "pink")
- Lone noun tones not used in compounds
"""

from typing import List, Set
import spacy
from collections import Counter

from Chatbot.extractors.color.tokenizer_utils import singularize


def extract_standalone_phrases(
    tokens: List[spacy.tokens.Token],
    token_counts: Counter,
    compounds: Set[str],
    raw_compounds: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extract standalone tokens which are valid tones or modifiers
    not fully absorbed by compound phrases.

    Args:
        tokens: spaCy tokens.
        token_counts: Frequency of each token in original input.
        compounds: Set of compound phrases (to avoid duplication).
        raw_compounds: List of tokenized compound forms.
        known_tones: Valid base tones.
        known_modifiers: Known modifier terms.
        all_webcolor_names: Known color names from CSS/XKCD.
        hardcoded_blocked_nouns: Nouns to exclude as false positives.
        debug: Show debug output.

    Returns:
        List of standalone tone/modifier tokens.
    """
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())
    singles = []

    for token in tokens:
        text = token.text.lower()
        norm = singularize(text)
        compound_uses = compound_token_counts[text]
        total_uses = token_counts[text]

        if debug:
            print(f"\n[🔍 TOKEN CHECK] → '{text}' | POS={token.pos_} | norm={norm}")
            print(f"    → in_known_modifiers: {text in known_modifiers}")
            print(f"    → in_known_tones: {norm in known_tones}")
            print(f"    → in_all_webcolor_names: {norm in all_webcolor_names}")
            print(f"    → total uses: {total_uses} | in compounds: {compound_uses}")

        if (text in known_modifiers or norm in known_tones) and norm not in hardcoded_blocked_nouns:

            if (
                norm in known_tones and
                token.pos_ == "NOUN" and
                norm not in all_webcolor_names
            ):
                if debug:
                    print(f"[⛔ REJECTED] → '{text}' (noun, not in webcolors)")
                continue

            if total_uses > compound_uses:
                singles.append(text)
                if debug:
                    print(f"[✅ ADDED SINGLE] → '{text}'")
            else:
                if debug:
                    print(f"[⛔ SKIPPED] → '{text}' only appears in compounds")

    return singles


def extract_lone_tones(
    tokens: List[spacy.tokens.Token],
    raw_compounds: List[str],
    known_tones: Set[str],
    hardcoded_blocked_nouns: Set[str],
    debug: bool
) -> List[str]:
    """
    Extract standalone tones used as nouns that weren’t part of any compound.

    Args:
        tokens: spaCy token list.
        raw_compounds: Previously extracted compound token phrases.
        known_tones: Set of base tones.
        hardcoded_blocked_nouns: Blocklist for ambiguous cosmetic nouns.
        debug: Show debug output.

    Returns:
        List of lone tone tokens.
    """
    lone_tones = []
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())

    for t in tokens:
        norm = singularize(t.text.lower())
        if (
            norm in known_tones and
            t.pos_ == "NOUN" and
            norm not in compound_token_counts and
            norm not in hardcoded_blocked_nouns
        ):
            lone_tones.append(norm)
            if debug:
                print(f"[✅ LONE TONE ADDED] → '{norm}'")

    return lone_tones
