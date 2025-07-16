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
from Chatbot.extractors.color.utils.token_utils import normalize_token, split_glued_tokens
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.general.utils.tokenizer import get_tokens_and_counts
known_modifiers = load_known_modifiers()
# ──────────────────────────────────────────────────────────────
# 🔹 Primary Interface: Expression Alias Matching
# ──────────────────────────────────────────────────────────────

def match_expression_aliases(input_text, expression_map, debug=True):
    tokens = list(get_tokens_and_counts(input_text).keys())
    matched_expressions = set()
    matched_aliases = set()

    for expr, props in expression_map.items():
        aliases = props.get("aliases", [])
        multiword_aliases = [a for a in aliases if " " in a]
        singleword_aliases = [a for a in aliases if " " not in a]

        # ⏫ First match multiword aliases (to suppress inner tokens like 'glam' in 'soft glam')
        for alias in multiword_aliases + singleword_aliases:
            if _should_accept_match(alias, input_text, tokens, matched_aliases, debug):
                if debug:
                    print(f"[✅ MATCH] Alias '{alias}' matched → {expr}")
                matched_expressions.add(expr)
                matched_aliases.add(alias.strip().lower())
                break
    # 🧩 Fallback: try matching by fuzzy modifier similarity
    if not matched_expressions:
        for expr, props in expression_map.items():
            modifiers = props.get("modifiers", [])
            for mod in modifiers:
                score = fuzz.ratio(mod.lower(), input_text.lower())
                if debug:
                    print(f"[🔍 MODIFIER FUZZ] '{input_text}' vs '{mod}' → {score}")
                if score >= 90:
                    matched_expressions.add(expr)
                    if debug:
                        print(f"[✅ MODIFIER MATCH] '{input_text}' ~ '{mod}' → {expr}")
                    break

    # 🧼 Final cleanup: suppress any expression whose alias is embedded in a longer match
    to_remove = set()
    for expr in matched_expressions:
        aliases = expression_map[expr].get("aliases", [])
        for alias in aliases:
            norm_alias = alias.strip().lower()
            input_norm = input_text.strip().lower()

            # Skip suppression if alias is a direct match
            if norm_alias == input_norm:
                continue

            # Don't suppress unless the shorter alias was actually matched independently
            if norm_alias not in matched_aliases:
                continue

            for matched in matched_aliases:
                if norm_alias in matched and norm_alias != matched:
                    if debug:
                        print(f"[🚫 EMBEDDED ALIAS REMOVED] '{norm_alias}' inside '{matched}'")
                    to_remove.add(expr)

    matched_expressions -= to_remove

    return matched_expressions


# ──────────────────────────────────────────────────────────────
# 🔹 Core Matching Dispatcher
# ──────────────────────────────────────────────────────────────

def _should_accept_match(alias, input_text, tokens, matched_aliases=None, debug=True):
    if input_text and alias in input_text.lower():
        if debug:
            print(f"[✅ DIRECT CONTAINS MATCH] alias '{alias}' found inside input → accepting")
        return True

    alias = alias.strip().lower()
    input_text = input_text.strip().lower()
    matched_aliases = matched_aliases or set()
    is_multiword = " " in alias

    for matched in matched_aliases:
        if alias in matched and matched != alias:
            if debug:
                print(f"[⛔ SKIP] '{alias}' is part of already matched multiword: '{matched}'")
            return False

    return (
        _handle_multiword_alias(alias, input_text, debug)
        if is_multiword
        else _handle_singleword_alias(alias, input_text, tokens, matched_aliases, debug)
    )

# ──────────────────────────────────────────────────────────────
# 🔹 Multiword Alias Handling
# ──────────────────────────────────────────────────────────────

def _handle_multiword_alias(alias, input_text, debug):
    if _is_exact_alias_match(alias, input_text):
        if debug: print(f"[✅ EXACT MATCH] '{alias}' == '{input_text}'")
        return True
    return _is_multiword_alias_match(alias, input_text, debug=debug)

def _is_multiword_alias_match(alias, input_text, threshold=85, debug=True):
    norm_alias = alias.strip().lower()
    norm_input = input_text.strip().lower()

    if fuzz.partial_ratio(norm_alias, norm_input) >= threshold:
        if debug: print(f"[🔍 FUZZ.partial_ratio] {norm_alias} ~ {norm_input}")
        return True

    alias_parts = norm_alias.split()
    input_parts = norm_input.split()

    if len(alias_parts) == 2 and sorted(alias_parts) == sorted(input_parts):
        if debug: print(f"[🔀 REORDERED MATCH] '{alias}' parts found in input")
        return True

    if fuzz.token_set_ratio(norm_alias, norm_input) >= 85 and _has_token_overlap(norm_alias, norm_input):
        if debug: print(f"[🌀 TOKEN SET MATCH] {norm_alias} ~ {norm_input}")
        return True

    return False
def _has_token_overlap(a: str, b: str) -> bool:
    return bool(set(a.split()) & set(b.split()))


def should_accept_multiword_alias(alias: str, input_text: str, threshold: int = 80, debug: bool = True, strict: bool = True):
    norm_alias = normalize_token(alias)
    norm_input = normalize_token(input_text)

    if norm_alias == norm_input:
        if debug: print("[✅ MATCH] Exact normalized match")
        return True

    score = fuzz.partial_ratio(norm_alias, norm_input)
    if debug: print(f"[🔍 FUZZ.partial_ratio] → {score}")
    if score >= threshold:
        return True

    alias_parts = norm_alias.split()
    input_parts = norm_input.split()

    if len(alias_parts) == 2 and len(input_parts) == 2 and sorted(alias_parts) == sorted(input_parts):
        return True

    matched = 0
    for token in alias_parts:
        best_score = max(fuzz.partial_ratio(token, other) for other in input_parts)
        if best_score >= 85 and (not strict or not any([
            token.startswith(other) or other.startswith(token)
            or token.endswith(other) or other.endswith(token)
            for other in input_parts])):
            matched += 1

    if matched == len(alias_parts):
        if debug: print("[✅ MATCH] All alias parts passed strict fuzzy containment")
        return True

    loose_score = fuzz.token_set_ratio(alias, input_text)
    if debug: print(f"[🧪 FUZZ.token_set_ratio] → {loose_score}")
    return loose_score >= 92 and (len(alias.split()) > 2 or len(input_text.split()) > 2)

# ──────────────────────────────────────────────────────────────
# 🔹 Singleword Alias Handling
# ──────────────────────────────────────────────────────────────

def _handle_singleword_alias(alias, input_text, tokens, matched_aliases, debug):
    for matched in matched_aliases:
        if alias in matched and len(matched.split()) > 1:
            if debug:
                print(f"[⛔ BLOCKED: token inside multiword] '{alias}' in '{matched}'")
            return False

    if _is_exact_alias_match(alias, input_text):
        if debug: print(f"[✅ EXACT MATCH] '{alias}' == '{input_text}'")
        return True

    return _is_token_fuzzy_match(alias, tokens, matched_aliases=matched_aliases, debug=debug)

# ──────────────────────────────────────────────────────────────
# 🔹 Fuzzy Token Logic
# ──────────────────────────────────────────────────────────────

def fuzzy_token_match(a: str, b: str) -> float:
    a = normalize_token(a)
    b = normalize_token(b)

    if a == b:
        return 100

    if frozenset({a, b}) in SEMANTIC_CONFLICTS:
        return 50

    partial = fuzz.partial_ratio(a, b)
    ratio = fuzz.ratio(a, b)
    bonus = 10 if a[:3] == b[:3] or a[:2] == b[:2] else 0

    return min(100, round((partial + ratio) / 2 + bonus))

def _is_token_fuzzy_match(
    alias,
    tokens,
    input_text=None,
    matched_aliases=None,
    debug=True,
    min_score=85
):
    alias = alias.strip().lower()
    matched_aliases = matched_aliases or set()

    if input_text:
        input_tokens = input_text.strip().lower().split()
        if len(input_tokens) == 2 and alias in input_tokens:
            if debug:
                print(f"[⛔ BLOCKED: TOKEN FUZZY] '{alias}' inside 2-word phrase: '{input_text}'")
            return False

    for token in tokens:
        token = token.strip().lower()

        if frozenset({alias, token}) in SEMANTIC_CONFLICTS:
            if debug:
                print(f"[🚫 FUZZY BLOCKED by SEMANTIC_CONFLICTS] '{token}' vs '{alias}'")
            return False

        score = fuzz.ratio(token, alias)
        if debug:
            print(f"[🔍 FUZZ.ratio] '{token}' vs '{alias}' → {score}")
        if score >= min_score:
            return True

        # ✅ Soft y-suffix fallback: 'edge' → 'edgy'
        if 70 <= score < min_score and alias.endswith("y"):
            root = alias[:-1]
            if token.startswith(root) or root.startswith(token):
                if debug:
                    print(f"[🌱 ROOT MATCH] '{token}' vs '{alias}' → accepting by suffix root")
                return True

    return False

# ──────────────────────────────────────────────────────────────
# 🔹 Utility Functions (Normalization & Conflict Resolution)
# ──────────────────────────────────────────────────────────────

def _is_exact_alias_match(alias, input_text):
    return alias.strip().lower() == input_text.strip().lower()

def is_exact_match(a: str, b: str) -> bool:
    """
    Smart matching for exact/near-exact comparison:
    - Lowercase
    - Singularized
    - Strips spaces/punctuation
    - Allows minor spelling variations (e.g., 'glamourous' ~ 'glamorous')
    """
    def clean(text):
        norm = normalize_token(text)
        return re.sub(r'[^a-z0-9]', '', norm.lower())

    a_clean = clean(a)
    b_clean = clean(b)

    if a_clean == b_clean:
        return True

    # Fallback: allow slight fuzzy variations
    return fuzz.ratio(a_clean, b_clean) >= 90
def is_strong_fuzzy_match(a: str, b: str, threshold: int = 85) -> bool:
    a_norm = normalize_token(a)
    b_norm = normalize_token(b)

    if frozenset({a_norm, b_norm}) in SEMANTIC_CONFLICTS or is_negation_conflict(a_norm, b_norm):
        return False

    return fuzzy_token_match(a_norm, b_norm) >= threshold

def is_embedded_alias_conflict(longer: str, shorter: str) -> bool:
    return shorter in longer and shorter != longer

def is_modifier_compound_conflict(expression: str, modifier_tokens: Set[str]) -> bool:
    return expression in modifier_tokens

def is_negation_conflict(a: str, b: str) -> bool:
    a = normalize_token(a)
    b = normalize_token(b)
    return (a.startswith("no ") and a[3:] == b) or (b.startswith("no ") and b[3:] == a)

def remove_subsumed_matches(matches: List[str]) -> List[str]:
    filtered = []
    matches = sorted(matches, key=len, reverse=True)

    for candidate in matches:
        is_subsumed = any(
            candidate != existing and (
                (" " not in existing and existing.startswith(candidate)) or
                re.search(rf'\b{re.escape(candidate)}\b', existing)
            )
            for existing in filtered
        )
        if not is_subsumed:
            filtered.append(candidate)

    return filtered
