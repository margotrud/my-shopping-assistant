# Chatbot/extractors/color/categorizer.py

"""
Color Categorizer
------------------
Provides utilities to analyze simplified color phrases,
extract unique tones and modifiers, and build bidirectional mappings
between modifiers and tones.

This module is essential for organizing and structuring
user-provided color preferences into meaningful categories,
helping the shopping assistant understand color relationships.
"""

# ──────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────

from typing import List, Set, Dict, Tuple, Optional
from collections import defaultdict
import json
from pathlib import Path
import spacy

from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.core.matcher import match_multiword_expressions
from Chatbot.extractors.general.helpers import fuzzy_token_match, get_all_trigger_tokens

# ──────────────────────────────────────────────────────────────
# NLP Setup
# ──────────────────────────────────────────────────────────────

nlp = spacy.load("en_core_web_sm")
IGNORED_POS = {"ADV", "PRON", "DET", "CCONJ", "ADP", "INTJ", "PART", "SCONJ", "VERB"}

# ──────────────────────────────────────────────────────────────
# Trigger Map Loader
# ──────────────────────────────────────────────────────────────
def load_expression_definitions(path: Path = None):
    if path is None:
        path = Path(__file__).resolve().parents[4] / "Data" / "expression_definition.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# ──────────────────────────────────────────────────────────────
# Token Preprocessing
# ──────────────────────────────────────────────────────────────

def get_valid_tokens(text: str, trigger_map: Dict[str, List[str]]) -> List[str]:
    tokens = nlp(text)
    print(f"[🧪 TOKENS] → {[f'{t.text} ({t.pos_})' for t in tokens]}")

    cleaned = []
    trigger_tokens = get_all_trigger_tokens(trigger_map)

    print(f"[🧪 INPUT TEXT] → {text}")
    print(f"[🧪 TOKENS] → {[f'{t.text} ({t.pos_})' for t in tokens]}")

    for token in tokens:
        word = token.text.lower()

        if token.pos_ not in IGNORED_POS:
            cleaned.append(word)
        elif token.pos_ == "VERB" and word in trigger_tokens:
            print(f"   🔓 OVERRIDE: {word} accepted (trigger-listed verb)")
            cleaned.append(word)
        elif token.pos_ == "VERB" and (word.endswith("ed") or word.endswith("en")):
            print(f"   🔓 OVERRIDE: {word} accepted (VERB ending in -ed/-en)")
            cleaned.append(word)

    print(f"[🧹 VALID TOKENS] → {cleaned}")
    return cleaned

# ──────────────────────────────────────────────────────────────
# Expression Matching
# ──────────────────────────────────────────────────────────────

def find_matching_expressions(text: str, trigger_map: Dict[str, List[str]]) -> List[str]:
    matched = set()
    tokens = get_valid_tokens(text, trigger_map)
    context_map = load_expression_context_rules()

    multiword_hits = match_multiword_expressions(text, trigger_map)
    matched.update(multiword_hits)

    blocked_tokens = set()
    for phrase in multiword_hits:
        blocked_tokens.update(phrase.lower().split())

    for token in tokens:

        if token in blocked_tokens:
            continue

        for vibe, triggers in trigger_map.items():
            for trig in triggers:
                if fuzzy_token_match(token, trig):
                    matched.add(vibe)
                    break

    promoted = apply_expression_context_rules(tokens, matched, context_map)
    matched.update(promoted)

    return sorted(suppress_conflicting_expressions(matched))

def map_expressions_to_tones(text: str, trigger_map: Dict[str, List[str]], known_tones: Set[str]) -> Dict[str, List[str]]:
    matched = find_matching_expressions(text, trigger_map)
    result = {}

    for expr in matched:
        keywords = trigger_map[expr]
        tones = [tone for tone in known_tones if any(k in tone for k in keywords)]
        if tones:
            result[expr] = sorted(set(tones))

    return result

# ──────────────────────────────────────────────────────────────
# Contextual Promotion and Suppression
# ──────────────────────────────────────────────────────────────

def load_expression_context_rules(path: Optional[str] = None) -> Dict[str, Dict[str, List[str]]]:
    default_path = Path(__file__).resolve().parents[4] / "Data" / "expression_context_rules.json"
    with (Path(path) if path else default_path).open("r", encoding="utf-8") as f:
        return json.load(f)

def apply_expression_context_rules(
    tokens: List[str],
    matched_expressions: Set[str],
    context_map: Dict[str, Dict[str, List[str]]]
) -> Set[str]:
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

EXPRESSION_SUPPRESSION_RULES = {
    "soft glam": {"glamorous"}
}

def suppress_conflicting_expressions(matched: Set[str]) -> Set[str]:
    suppressed = set(matched)
    for dominant, to_remove in EXPRESSION_SUPPRESSION_RULES.items():
        if dominant in matched:
            suppressed -= to_remove
    return suppressed

# ──────────────────────────────────────────────────────────────
# Tone + Modifier Categorization
# ──────────────────────────────────────────────────────────────

def build_tone_modifier_mappings(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Tuple[Set[str], Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]:
    tones = set()
    modifiers = set()
    modifier_to_tone = defaultdict(set)
    tone_to_modifier = defaultdict(set)

    for phrase in phrases:
        tokens = phrase.lower().split()
        matched_tones = [t for t in tokens if t in known_tones]
        matched_modifiers = [t for t in tokens if t in known_modifiers]

        tones.update(matched_tones)
        modifiers.update(matched_modifiers)

        for mod in matched_modifiers:
            for tone in matched_tones:
                modifier_to_tone[mod].add(tone)
                tone_to_modifier[tone].add(mod)

    return tones, modifiers, modifier_to_tone, tone_to_modifier

def categorize_color_tokens_with_mapping(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Dict[str, object]:
    tones, modifiers, modifier_to_tone, tone_to_modifier = build_tone_modifier_mappings(
        phrases, known_tones, known_modifiers
    )
    return {
        "tones": sorted(tones),
        "modifiers": sorted(modifiers),
        "modifier_to_tone": {mod: sorted(tones) for mod, tones in modifier_to_tone.items()},
        "tone_to_modifier": {tone: sorted(mods) for tone, mods in tone_to_modifier.items()},
    }

def clean_and_categorize(
    phrases: List[str],
    known_modifiers: Set[str]
) -> Dict[str, List[str]]:
    return categorize_color_tokens_with_mapping(phrases, known_tones, known_modifiers)
