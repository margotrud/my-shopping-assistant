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

from Chatbot.extractors.color.core.modifier_resolution import resolve_modifier_with_suffix_fallback
from Chatbot.extractors.color.core.tokenizer import singularize
from Chatbot.extractors.color.extract.categorizer import load_expression_definitions, find_matching_expressions
from Chatbot.extractors.color.core.matcher import match_multiword_expressions
import spacy

nlp = spacy.load("en_core_web_sm")

# Define once globally
COSMETIC_NOUNS = {
    "blush", "foundation", "lipstick", "concealer",
    "bronzer", "highlighter", "mascara", "eyeliner"
}


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
    compound_token_counts = Counter(tok for phrase in raw_compounds for tok in phrase.split())
    singles = []

    # ───── Load expressions
    expression_definitions = load_expression_definitions()
    trigger_map = {k: v["aliases"] for k, v in expression_definitions.items() if "aliases" in v}

    # ───── Detect expressions
    text_input = " ".join([t.text for t in tokens]).lower()
    doc = nlp(text_input)
    matched_expressions = find_matching_expressions(text_input, trigger_map)

    # ───── Collect tokens from matched expressions
    expression_tokens = {
        token for expr in matched_expressions
        for token in expr.lower().split()
    }

    if debug:
        print(f"[🔍 CHECK INPUT] → {text_input}")
        print(f"[📂 TRIGGER MAP KEYS] → {list(trigger_map.keys())}")
        print(f"[📦 MATCHED EXPRESSIONS] → {matched_expressions}")

    # ───── Inject modifiers or tones from expressions
    # Skip expression injection if cosmetic product detected in noun tokens
    cosmetic_found = any(tok.lemma_ in COSMETIC_NOUNS for tok in tokens if tok.pos_ == "NOUN")

    for expr in matched_expressions:
        if cosmetic_found:
            if debug:
                print(f"[⛔ BLOCK INJECTION] Cosmetic context active → skipping '{expr}' injection")
            continue

        expression_mods = expression_definitions.get(expr, {}).get("modifiers", [])
        modifiers = [m for m in expression_mods if m in known_modifiers]
        singles.extend(modifiers)
        if debug:
            print(f"[🧠 EXPRESSION INJECT] → '{expr}' → {modifiers}")

        if debug:
            print(f"[🧠 EXPRESSION INJECT] → '{expr}' → {modifiers}")

        if expr in known_tones and expr not in singles:
            singles.append(expr)
            if debug:
                print(f"[✅ INJECTED TONE] → '{expr}'")

    # ───── Token-level check
    for token in tokens:
        text = token.text.lower()
        norm = singularize(text)
        compound_uses = compound_token_counts[text]
        total_uses = token_counts[text]
        resolved = resolve_modifier_with_suffix_fallback(text, known_modifiers)

        if token.pos_ == "NOUN" and token.lemma_ in COSMETIC_NOUNS:
            if debug:
                print(f"[⛔ SKIP TOKEN] Cosmetic product mention detected → '{token.text}' → skipped")
            continue

        if text in expression_tokens:
            if debug:
                print(f"[⛔ SKIP] '{text}' part of expression match → skipped")
            continue

        if (
            (resolved or norm in known_tones)
            and norm not in hardcoded_blocked_nouns
        ):
            if norm in known_tones and token.pos_ == "NOUN" and norm not in all_webcolor_names:
                if debug:
                    print(f"[⛔ REJECTED] '{text}' (noun tone not in webcolors)")
                continue

            # Check for base tone collision
            base = None
            if text.endswith(("y", "ish")):
                base = text.rstrip("y").rstrip("ish")

            if base in known_tones or base in singles:
                if debug:
                    print(f"[⛔ SUPPRESSED DERIVATIVE] '{text}' because base tone '{base}' is valid")
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
