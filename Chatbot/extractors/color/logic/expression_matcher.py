"""
expression_matcher.py
=====================

Handles stylistic expression matching based on defined tone mappings.
Supports direct token scanning, alias mapping, context-aware promotion, and priority-based suppression.
"""
from logging import debug
from typing import List, Set, Dict
import re
from Chatbot.extractors.color.shared.constants import EXPRESSION_SUPPRESSION_RULES
from Chatbot.extractors.color.utils.nlp_utils import are_antonyms
from Chatbot.extractors.color.utils.token_utils import singularize
from Chatbot.extractors.color.utils.config_loader import load_expression_context_rules

def get_valid_tokens(text: str, expression_map: Dict) -> List[str]:
    """
    Extracts valid full expression aliases (multi-word or single) from the input text.
    Avoids returning both 'soft' and 'glam' if 'soft glam' is already matched.
    """
    text_lower = text.lower()
    matched = set()

    all_aliases = set()
    for entry in expression_map.values():
        all_aliases.update(entry.get("aliases", []))
        all_aliases.update(entry.get("modifiers", []))

    # Sort aliases by descending length so "soft glam" is matched before "soft"
    for alias in sorted(all_aliases, key=lambda x: -len(x)):
        alias_lower = alias.lower()
        if re.search(rf"\b{re.escape(alias_lower)}\b", text_lower):
            # Check if it's already part of a longer match
            if not any(alias_lower in longer for longer in matched if alias_lower != longer):
                matched.add(alias_lower)

    return sorted(matched)


from rapidfuzz import fuzz


def extract_alias_matches(text: str, expression_def: dict) -> Set[str]:
    """
    Matches aliases using literal or fuzzy logic, and returns the expression tags
    that had at least one alias matched.

    Returns:
        Set[str]: Expression tags like {'elegant', 'romantic'}
    """
    text_lower = text.lower()
    tokens = [singularize(tok) for tok in text_lower.split()]
    matched_expressions = set()

    for expr, data in expression_def.items():
        for alias in data.get("aliases", []):
            alias_lower = alias.lower()

            # 1. Literal inclusion
            if re.search(rf"\b{re.escape(alias_lower)}\b", text_lower):
                matched_expressions.add(expr)

                break

            # 2. Fuzzy match (1-word only)
            if " " not in alias_lower:
                for word in tokens:
                    score = fuzz.ratio(alias_lower, word)

                    if are_antonyms(alias_lower, word):
                        if debug:
                            print(f"[🚫 FUZZY BLOCKED: ANTONYMS] alias='{alias_lower}' vs token='{word}'")
                        continue

                    # Special negation check: block fuzzy match if 'no-X' vs 'X' appears
                    if alias_lower.startswith("no-"):
                        positive = alias_lower.replace("no-", "")
                        if positive in tokens:
                            if debug:
                                print(
                                    f"[⚠️ FUZZY CONFLICT] alias='{alias_lower}' rejected due to presence of '{positive}' in input")
                            continue

                    if score >= 80:
                        matched_expressions.add(expr)
                        break

    return matched_expressions

def map_expressions_to_tones(
    text: str,
    expression_def: Dict[str, Dict[str, List[str]]],
    known_tones: Set[str],
    debug: bool = True
) -> Dict[str, List[str]]:
    results = {}
    text_lower = text.lower()
    raw_matched = extract_alias_matches(text, expression_def)
    tokens = [singularize(tok) for tok in text_lower.split()]
    context_map = load_expression_context_rules()

    # 🚀 Promote expressions via co-occurrence context
    promoted = apply_expression_context_rules(tokens, raw_matched, context_map)
    if debug and promoted:
        print(f"[📈 CONTEXT PROMOTED] → {promoted}")

    # Union matched + promoted before suppression
    raw_matched |= promoted

    longest_matched_aliases = apply_expression_suppression_rules(raw_matched)
    if debug:
        removed = raw_matched - longest_matched_aliases
        if removed:
            print(f"[🧹 SUPPRESSED] Removed lower-priority expressions → {removed}")

    for expr, data in expression_def.items():
        aliases = data.get("aliases", [])

        if expr not in longest_matched_aliases and not any(alias in longest_matched_aliases for alias in aliases):
            if debug:
                print(f"[❌ SKIP] {expr}: no aliases matched for '{expr}'")
            continue

        matched = [
            alias for alias in aliases
            if any(alias.lower() in longest_matched_aliases for alias in aliases)

        ]

        if not matched:
            if debug:
                print(f"[🚫 BLOCKED] {expr}: fuzzy passed, but no alias survived literal/fuzzy match")
                print(f"  Aliases: {aliases}")
                print(f"  Input: '{text}'")
                print(f"  longest_matched_aliases: {longest_matched_aliases}")
            continue

        if debug:
            print(f"[✅ ALIAS MATCH] {expr}: kept aliases → {matched}")

        modifiers = data.get("modifiers", [])
        valid_tones = [m for m in modifiers if m in known_tones]
        if valid_tones:
            results[expr] = valid_tones
            if debug:
                print(f"[✅ MAPPED] {expr} → {valid_tones}")

    return results


def apply_expression_context_rules(
    tokens: List[str],
    matched_expressions: Set[str],
    context_map: Dict[str, List[Dict[str, List[str]]]]
) -> Set[str]:
    token_set = set(tokens)
    promotions = set()

    for expression, rules in context_map.items():
        if expression in matched_expressions:
            continue

        for rule in rules:
            required = set(rule.get("require_tokens", []))
            clues = set(rule.get("context_clues", []))

            if required & token_set and clues & token_set:
                promotions.add(expression)
                break

    return promotions



def apply_expression_suppression_rules(matched: Set[str]) -> Set[str]:
    """
    Applies suppression rules to matched expressions.
    Removes lower-priority expressions if their dominant ones exist.
    """
    suppressed = set(matched)

    for dominant, to_remove in EXPRESSION_SUPPRESSION_RULES.items():
        if dominant in matched:
            suppressed -= to_remove

    return suppressed

