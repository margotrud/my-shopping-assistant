"""
expression_matcher.py
=====================

Handles stylistic expression matching based on defined tone mappings.
Supports direct token scanning, alias mapping, context-aware promotion, and priority-based suppression.
"""
from typing import List, Set, Dict
from spacy.tokens import Token
from Chatbot.extractors.color.shared.constants import EXPRESSION_SUPPRESSION_RULES
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases


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
        if alias_lower in text_lower:
            # Check if it's already part of a longer match
            if not any(alias_lower in longer for longer in matched if alias_lower != longer):
                matched.add(alias_lower)

    return sorted(matched)
def map_expressions_to_tones(
    text: str,
    expression_def: Dict[str, Dict[str, List[str]]],
    known_tones: Set[str],
    debug: bool = False
) -> Dict[str, List[str]]:
    """
    Maps expression names to tone keywords based on modifiers declared in expression_def.
    Returns a dictionary: expression → matched tones
    """
    matches = match_expression_aliases(text, expression_def)
    results = {}

    for expr in matches:
        modifiers = expression_def.get(expr, {}).get("modifiers", [])
        matched = [mod for mod in modifiers if mod in known_tones]
        if matched:
            results[expr] = matched
            if debug:
                print(f"[🎨 MAPPED] '{expr}' → {matched}")
    return results




def apply_expression_context_rules(
    tokens: List[str],
    matched_expressions: Set[str],
    context_map: Dict[str, Dict[str, List[str]]]
) -> Set[str]:
    """
    Promotes additional expressions based on contextual co-occurrence logic.

    This function checks each expression not already matched and evaluates whether
    the input tokens satisfy both:
    - Required tokens (hard anchors)
    - Contextual clues (softer hints)

    If both are found, the expression is "promoted" as if matched.

    Args:
        tokens (List[str]): Lowercased user tokens (raw text, not spaCy tokens).
        matched_expressions (Set[str]): Expressions matched via direct alias/fuzzy matching.
        context_map (Dict): Maps expression names to:
            - require_tokens: list of mandatory anchors
            - context_clues: list of softer associated keywords

    Returns:
        Set[str]: Newly promoted expression tags.
    """
    token_set = set(tokens)
    promotions = set()

    for expression, rule in context_map.items():
        if expression in matched_expressions:
            continue

        required = set(rule.get("require_tokens", []))
        clues = set(rule.get("context_clues", []))

        if required & token_set and clues & token_set:
            print(f"[🎯 CONTEXT PROMOTION] '{expression}' ← context={clues & token_set}")
            promotions.add(expression)

    return promotions


def apply_expression_context_rules(
    tokens: List[str],
    matched_expressions: Set[str],
    context_map: Dict[str, Dict[str, List[str]]]
) -> Set[str]:
    """
    Promotes additional expressions based on token context (require_tokens and context_clues).
    """
    added = set()

    for expr, ctx in context_map.items():
        if expr in matched_expressions:
            continue

        req_tokens = set(ctx.get("require_tokens", []))
        context_clues = set(ctx.get("context_clues", []))

        if req_tokens and not req_tokens.issubset(tokens):
            continue

        if context_clues and context_clues.intersection(tokens):
            added.add(expr)

    return matched_expressions.union(added)


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