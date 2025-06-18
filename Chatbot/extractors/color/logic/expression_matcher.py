"""
expression_matcher.py
=====================
Expression tag matching logic for user input interpretation.

This module identifies high-level style or aesthetic expressions
from user-generated text based on known expression definitions
(e.g., "soft glam", "romantic", "natural").

It performs two primary tasks:
1. Extracts relevant tokens from input using part-of-speech filtering
   and expression-specific vocabularies (modifiers and aliases).
2. Matches expression categories by scanning for alias phrases
   using fuzzy and exact matching techniques.

Used to interpret abstract requests like:
- "I want something elegant and timeless"
- "A romantic look, soft and pink"
- "Something edgy for a night out"

Example Workflow:
-----------------
>>> tokens, _ = get_tokens_and_counts("I'm going for a soft glam wedding look")
>>> valid = get_valid_tokens(tokens, expression_definition)
>>> matches = match_expression_aliases("soft glam wedding look", expression_definition)
>>> # Result: {"soft glam", "romantic"}

Dependencies:
-------------
- spaCy for POS tagging
- expression_definition.json for alias + modifier vocab
- fuzzy_match.py for partial match resolution
"""

from spacy.tokens import Token
from typing import List, Dict, Set
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases
from Chatbot.extractors.color.shared.constants import EXPRESSION_SUPPRESSION_RULES



def get_valid_tokens(tokens: List, expression_map: dict) -> List[str]:
    """
    Filters input tokens to return only those relevant for expression classification.

    Tokens are considered valid if they:
    - Appear in any alias or modifier list of the expression definition

    Args:
        tokens (List[Token]): spaCy token objects.
        expression_map (dict): Parsed expression_definition.json

    Returns:
        List[str]: Lowercased valid token texts that match expression triggers.
    """
    all_triggers = set()
    for entry in expression_map.values():
        all_triggers.update(entry.get("aliases", []))
        all_triggers.update(entry.get("modifiers", []))

    return [token.text.lower() for token in tokens if token.text.lower() in all_triggers]

def map_expressions_to_tones(
    text: str,
    expression_def: Dict[str, Dict[str, List[str]]],
    known_tones: Set[str],
    debug: bool = False
) -> Dict[str, List[str]]:
    """
    Maps matched expression tags in the input to related color tones.

    This function:
    1. Identifies expression matches using fuzzy alias matching.
    2. For each matched expression, collects any MODIFIERS that
       overlap with known tone names.
    3. Returns a mapping of expression → relevant tone names.

    Args:
        text (str): User input.
        expression_def (dict): Full expression_definition.json content.
        known_tones (Set[str]): Valid tone names (e.g., CSS + XKCD + custom).
        debug (bool): If True, prints debug logs.

    Returns:
        Dict[str, List[str]]: Expression → matching tone names.
    """
    matched = match_expression_aliases(text, expression_def)
    result = {}

    if debug:
        print(f"\n[🔍 USER TEXT] → {text}")
        print(f"[📌 MATCHED EXPRESSIONS] → {matched}")
        print(f"[🎨 KNOWN TONES SAMPLE] → {sorted(list(known_tones))[:10]} ...")

    for expr in matched:
        modifiers = expression_def.get(expr, {}).get("modifiers", [])
        if debug:
            print(f"\n[💡 EXPRESSION] '{expr}' → Modifiers: {modifiers}")

        tones = [
            tone for tone in known_tones
            if any(mod in tone for mod in modifiers)
        ]

        if debug:
            print(f"[🎯 MATCHED TONES FOR '{expr}'] → {tones if tones else 'None'}")

        if tones:
            result[expr] = sorted(set(tones))

    if debug:
        print(f"\n[✅ FINAL RESULT] → {result}")

    return result



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


def apply_expression_suppression_rules(matched: Set[str]) -> Set[str]:
    """
    Applies priority-based suppression rules to eliminate lower-ranking expressions.

    For example, if 'glamorous' is present, this function may suppress
    'natural' or 'daytime' if they conflict semantically.

    Driven by:
        EXPRESSION_SUPPRESSION_RULES = {
            'glamorous': {'natural', 'daytime'},
            ...
        }

    Args:
        matched (Set[str]): Initially matched expressions.

    Returns:
        Set[str]: Filtered set after applying suppression rules.
    """
    suppressed = set(matched)

    for dominant, to_remove in EXPRESSION_SUPPRESSION_RULES.items():
        if dominant in matched:
            suppressed -= to_remove

    return suppressed

