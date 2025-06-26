# Chatbot/extractors/general/utils/fuzzy_match.py

"""
fuzzy_match.py
==============

Generic fuzzy token matcher with blocklist, prefix, and multi-word logic.

Designed for reuse across multiple domains (e.g., colors, brands, products).
Wraps common secure fuzzy matching behaviors into a single configurable function.

Features:
---------
- Exact match
- Safe prefix match (single-word only)
- Multi-word trigger matching
- Fuzzy string ratio fallback
- Optional semantic blocklist filtering
"""

from typing import List, Set
import re
from fuzzywuzzy import fuzz
from Chatbot.extractors.color.shared.constants import SEMANTIC_CONFLICTS
from Chatbot.extractors.color.utils.token_utils import singularize, normalize_token


def fuzzy_token_match(a: str, b: str) -> float:
    a = normalize_token(a)
    b = normalize_token(b)

    if a == b:
        return 100

    if frozenset({a, b}) in SEMANTIC_CONFLICTS:
        return 60  # hard semantic block

    partial = fuzz.partial_ratio(a, b)
    ratio = fuzz.ratio(a, b)
    bonus = 10 if a[:3] == b[:3] or a[:2] == b[:2] else 0

    return min(100, round((partial + ratio) / 2 + bonus))

from Chatbot.extractors.color.utils.token_utils import normalize_token
from fuzzywuzzy import fuzz

def fuzzy_fallback_unmatched_tokens(original_tokens, expression_map, matched_expressions, consumed_spans, threshold=90, debug=False):
    for idx, raw_token in enumerate(original_tokens):
        if idx in consumed_spans:
            continue  # already matched

        for expression, props in expression_map.items():
            for alias in props.get("aliases", []):
                alias_words = alias.lower().split()
                if len(alias_words) == 1:
                    score = fuzz.ratio(raw_token.lower(), alias_words[0])
                    if score >= threshold:
                        matched_expressions.add(expression)
                        if debug:
                            print(f"[🌀 FUZZY MATCH] '{raw_token}' ~ '{alias_words[0]}' ({score}) → Expression: '{expression}'")
                        break

def match_expression_aliases(text: str, expression_map: dict, debug: bool = False) -> set[str]:
    """
    Matches known expression aliases to user input using:
    - Literal span match (multi-word or token-by-token)
    - Normalized token match
    - Fuzzy fallback on raw tokens (only if nothing matched literally)

    Args:
        text (str): Raw user input, e.g., "barely there glam"
        expression_map (dict): Expression → alias list
        debug (bool): Whether to print debug info

    Returns:
        set[str]: Expressions matched (e.g., {"natural", "soft glam"})
    """
    from Chatbot.extractors.color.utils.token_utils import normalize_token

    tokens = text.lower().split()
    matched_expressions = set()
    seen_aliases = set()

    if debug:
        print(f"[🧪 INPUT TEXT] → '{text}'")
        print(f"[🧬 TOKENS] → {tokens}")
        print(f"[📂 TOTAL EXPRESSIONS] → {len(expression_map)}")

    for expression, aliases in expression_map.items():
        if debug:
            print(f"\n🔍 [CHECKING EXPRESSION] '{expression}' with {len(aliases)} aliases")

        for alias in aliases:
            alias_tokens = alias.lower().split()
            n = len(alias_tokens)

            # Try literal match at each span
            for i in range(len(tokens) - n + 1):
                window = tokens[i:i+n]
                if window == alias_tokens:
                    matched_expressions.add(expression)
                    seen_aliases.add(alias)
                    if debug:
                        print(f"✅ [MATCH] Alias '{alias}' at span ({i}, {i+n}) → {window}")
                    break

    # Build token-to-expression fuzzy fallbacks (if nothing literal matched)
    if debug:
        print("\n[🌀 FUZZY FALLBACK STARTED]")

    for token in tokens:
        norm = normalize_token(token)

        for expression, aliases in expression_map.items():
            for alias in aliases:
                alias_norm = normalize_token(alias)

                # 🧷 Safeguard: avoid matching a short alias if token embeds it
                if len(alias.split()) == 1 and alias in token and len(token) > len(alias) + 3:
                    if debug:
                        print(f"[⛔ SKIP: alias too short for glue token] '{token}' ~ '{alias}'")
                    continue

                score = fuzzy_token_match(norm, alias_norm)
                if score >= 100:
                    matched_expressions.add(expression)
                    if debug:
                        print(f"🌀 [FUZZY FALLBACK] '{token}' ~ '{alias}' → {expression} (score={score})")

    # 🔁 Try splitting glued tokens like 'softglam'
    for token in tokens:
        for expression, aliases in expression_map.items():
            for alias in aliases:
                if " " not in alias:
                    continue  # Only check compound aliases

                parts = alias.lower().split()
                joined = "".join(parts)
                if token == joined:
                    matched_expressions.add(expression)
                    if debug:
                        print(f"🧩 [GLUED MATCH] '{token}' → '{alias}' → {expression}")

    if debug:
        print(f"\n[🎯 FINAL MATCHED EXPRESSIONS] → {matched_expressions}")

    return matched_expressions


def should_accept_multiword_alias(alias: str, input_text: str, threshold: int = 85) -> bool:
    """
    Evaluates whether a multi-word alias should be accepted as a match based on fuzzy similarity.

    Args:
        alias (str): The multi-word alias (e.g., "work appropriate").
        input_text (str): Lowercased user input text (e.g., "something more work appropriate").
        threshold (int): Minimum fuzzy ratio required for match.

    Returns:
        bool: True if match is confident, else False.
    """
    score = fuzz.partial_ratio(normalize_token(alias), normalize_token(input_text))
    return score >= threshold


def is_exact_match(a: str, b: str) -> bool:
    """
    Checks for normalized equality.

    Args:
        a (str): First token.
        b (str): Second token.

    Returns:
        bool: True if equal after normalization.
    """
    return normalize_token(a) == normalize_token(b)


def is_strong_fuzzy_match(a: str, b: str, threshold: int = 85) -> bool:
    a_norm = normalize_token(a)
    b_norm = normalize_token(b)

    if frozenset({a_norm, b_norm}) in SEMANTIC_CONFLICTS:
        return False

    if is_negation_conflict(a_norm, b_norm):
        return False

    return fuzzy_token_match(a_norm, b_norm) >= threshold
def is_embedded_alias_conflict(longer: str, shorter: str) -> bool:
    """
    Detects conflict where one alias is embedded in another (e.g., 'glamorous' vs 'glam').

    Args:
        longer (str): Full phrase matched.
        shorter (str): Alias token.

    Returns:
        bool: True if alias is strictly embedded and not equal.
    """
    return shorter in longer and shorter != longer


def is_modifier_compound_conflict(expression: str, modifier_tokens: Set[str]) -> bool:
    """
    Flags if an expression token conflicts with a known modifier,
    e.g., 'natural' being interpreted both as an expression and a modifier.

    Args:
        expression (str): Candidate expression token.
        modifier_tokens (Set[str]): Set of known modifiers.

    Returns:
        bool: True if conflict exists.
    """
    return expression in modifier_tokens


def remove_subsumed_matches(matches: List[str]) -> List[str]:
    """
    Removes redundant short matches that are:
    - Prefixes of longer tokens (e.g., 'glam' vs 'glamorous')
    - Full-word components inside longer multi-word expressions (e.g., 'glam' in 'soft glam')

    Args:
        matches (List[str]): List of matched phrases.

    Returns:
        List[str]: Filtered list with minimal semantic redundancy.
    """
    filtered = []
    matches = sorted(matches, key=len, reverse=True)

    for candidate in matches:
        is_subsumed = False
        for existing in filtered:
            if candidate == existing:
                continue

            # Case 1: strict prefix in a single-word token (e.g., glam → glamorous)
            if " " not in existing and existing.startswith(candidate):
                is_subsumed = True
                break

            # Case 2: full-word contained in a multi-word expression (e.g., glam in soft glam)
            if re.search(rf'\b{re.escape(candidate)}\b', existing):
                is_subsumed = True
                break

        if not is_subsumed:
            filtered.append(candidate)

    return filtered
def is_negation_conflict(a: str, b: str) -> bool:
    a = normalize_token(a)
    b = normalize_token(b)

    return (
        (a.startswith("no ") and a[3:] == b) or
        (b.startswith("no ") and b[3:] == a)
    )
