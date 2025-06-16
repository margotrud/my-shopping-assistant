#Chatbot/extractors/general/utils/fuzzy_match.py
"""
Fuzzy Match Utility
===================
Secure and extensible matching system for comparing user input to predefined aliases
and expressions in a domain-aware context (e.g., cosmetics, fashion, color).

Supports:
---------
- Normalization using WordNet + spaCy + heuristics
- Secure fuzzy string matching (with exact/prefix/multi-word logic)
- Blocklist enforcement to reject semantic overlaps
- Expression alias detection with multi-word heuristics

Used for:
---------
- Matching free-text to aesthetic expressions (e.g., "soft glam", "edgy", "natural")
- Avoiding false-positive matches from ambiguous or embedded aliases
"""

from typing import Set, Tuple, Optional, Dict, List
from nltk.stem import WordNetLemmatizer
import spacy
from fuzzywuzzy import fuzz
from rapidfuzz import fuzz as rapidfuzz_fuzz
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

# Load global models
wnl = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")

def normalize_token(token: str) -> str:
    """
       Normalize a word using suffix removal, WordNet lemmatization, and spaCy lemmatization.

       Args:
           token (str): Raw input string.

       Returns:
           str: Normalized token.
       """
    original = token
    token = token.lower().strip()

    # Rule 1: Strip suffix like "-ness"
    for suffix in ["ness"]:
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            return token[:-len(suffix)]

    # Rule 2: WordNet lemmatization
    for pos in ['a', 'n']:
        lemma = wnl.lemmatize(token, pos=pos)
        if lemma != token:
            return lemma

    # Rule 3: spaCy lemmatization
    if " " not in token:
        doc = nlp(token)
        if doc and doc[0].lemma_ != token:
            return doc[0].lemma_.lower()

    return token

def fuzzy_token_match(
        token: str,
        target: str,
        *,
        blocklist: Optional[Set[Tuple[str, str]]] = None,
        threshold: int = 75,
        allow_prefix: bool = True,
        allow_multiword: bool = True
) -> bool:
    """
       General-purpose fuzzy matcher between a token and a target string.

       Args:
           token (str): User-provided input string.
           target (str): Known label to compare against.
           blocklist (Optional[Set[Tuple[str, str]]]): Set of blocked token-target pairs.
           threshold (int): Fuzzy score threshold.
           allow_prefix (bool): If True, allows prefix match (1-word only).
           allow_multiword (bool): If True, allows multi-word partwise matching.

       Returns:
           bool: True if match passes, else False.
       """
    token = normalize_token(token)
    target = normalize_token(target)
    pair = (token, target)
    reverse = (target, token)

    if blocklist and (pair in blocklist or reverse in blocklist):
        return False
    if token == target:
        return True
    if allow_prefix and " " not in token and " " not in target and target.startswith(token):
        return True
    if " " in target and allow_multiword:
        token_parts = token.split()
        target_parts = target.split()
        if len(token_parts) != len(target_parts):
            return False
        return all(rapidfuzz_fuzz.ratio(a, b) >= threshold for a, b in zip(token_parts, target_parts))
    if " " not in token and " " not in target:
        return rapidfuzz_fuzz.ratio(token, target) >= threshold
    return False


def match_expression_aliases(
    text: str,
    expression_definition: Dict[str, Dict[str, list]],
    threshold: int = 85
) -> Set[str]:
    """
    Matches a user text against expression aliases with fuzzy logic.

    Args:
        text (str): Input text (e.g., "barely there glam and red carpet").
        expression_definition (Dict): Expression → {"aliases": [...], "modifiers": [...]}
        threshold (int): Minimum fuzzy score to accept alias match.

    Returns:
        Set[str]: Set of matched expression keys (e.g., {"soft glam", "natural"})
    """
    matches = set()
    lowered = text.lower()
    input_tokens = lowered.split()
    known_modifiers = load_known_modifiers()

    # Pre-check multi-word triggers
    for expression, definition in expression_definition.items():
        for alias in definition.get("aliases", []):
            if " " in alias and fuzz.token_sort_ratio(alias.lower(), lowered) >= threshold:
                matches.add(expression)
                break

    for expression, definition in expression_definition.items():
        for alias in definition.get("aliases", []):
            alias_lower = alias.lower()
            if is_exact_match(alias_lower, lowered):
                matches.add(expression)
                continue

            score = fuzz.partial_ratio(alias_lower, lowered)
            if is_strong_fuzzy_match(score, threshold):
                if is_embedded_alias_conflict(alias_lower, definition["aliases"], lowered, score):
                    continue
                if is_modifier_compound_conflict(alias_lower, input_tokens, known_modifiers, expression_definition):
                    continue
                matches.add(expression)
                continue

            if should_accept_multiword_alias(alias_lower, alias_lower.split(), lowered):
                matches.add(expression)

    return remove_subsumed_matches(matches, expression_definition, text)


def is_exact_match(alias: str, lowered_input: str) -> bool:
    return alias == lowered_input


def is_strong_fuzzy_match(score: int, threshold: int) -> bool:
    return score >= threshold or threshold - 5 <= score < threshold


def is_embedded_alias_conflict(alias: str, aliases: List[str], lowered_input: str, score: int) -> bool:
    if len(alias.split()) > 1:
        return False
    if alias in lowered_input:
        for other in aliases:
            if alias in other and alias != other and other in lowered_input and score < 88:
                return True
        if score < 88:
            return True
    return False


def is_modifier_compound_conflict(
    alias: str,
    input_tokens: List[str],
    known_modifiers: Set[str],
    expression_definition: Dict[str, Dict[str, list]]
) -> bool:
    """
    Prevents false-positive matching on modifier + tone (e.g., "soft pink")
    when alias is a standalone tone also present as compound.
    """
    if alias not in input_tokens:
        return False
    idx = input_tokens.index(alias)
    if idx == 0:
        return False

    prev_token = input_tokens[idx - 1]
    compound = f"{prev_token} {alias}"

    return (
        prev_token in known_modifiers and
        alias in known_modifiers and
        not any(compound in d.get("aliases", []) for d in expression_definition.values())
    )


def should_accept_multiword_alias(alias: str, words: List[str], lowered_input: str) -> bool:
    return len(words) > 1 and alias in lowered_input


def remove_subsumed_matches(
    matches: Set[str],
    expression_definition: Dict[str, Dict[str, list]],
    text: str
) -> Set[str]:
    """
    Remove expressions matched via partial alias embedding
    (e.g., remove "glamorous" if "soft glam" was matched).

    Returns:
        Set[str]: Filtered matches.
    """
    lowered = text.lower()
    alias_to_expr = {}
    for expr in matches:
        for alias in expression_definition[expr].get("aliases", []):
            alias_lower = alias.lower()
            score = fuzz.partial_ratio(alias_lower.replace(" ", ""), lowered.replace(" ", ""))
            if score >= 85:
                alias_to_expr[alias_lower] = expr

    final = set(matches)
    for a, expr_a in alias_to_expr.items():
        for b, expr_b in alias_to_expr.items():
            if expr_a != expr_b and a in b and len(a) < len(b):
                final.discard(expr_a)
    return final