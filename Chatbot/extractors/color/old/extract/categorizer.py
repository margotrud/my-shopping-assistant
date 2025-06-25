# Chatbot/extractors/color/extract/categorizer.py

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
from Chatbot.extractors.color.old.core import match_multiword_expressions
from Chatbot.extractors.general.old.helpers import fuzzy_token_match, get_all_trigger_tokens
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token

# ──────────────────────────────────────────────────────────────
# NLP Setup
# ──────────────────────────────────────────────────────────────

nlp = spacy.load("en_core_web_sm")
IGNORED_POS = {"ADV", "PRON", "DET", "CCONJ", "ADP", "INTJ", "PART", "SCONJ", "VERB"}

# ──────────────────────────────────────────────────────────────
# Trigger Map Loader
# ──────────────────────────────────────────────────────────────
def load_expression_definitions(path: Path = None):
    """
    Loads expression-to-color definition mappings from a JSON file.

    This function reads a JSON file that maps expression categories
    (e.g., "neutral", "bold", "romantic") to associated color descriptors
    or tone suggestions. It allows a custom path to be provided; otherwise,
    a default path is used based on the project structure.

    Args:
        path (Path, optional): Custom path to the expression definition JSON file.
            Defaults to 'Data/expression_definition.json' relative to project root.

    Returns:
        dict: Dictionary mapping expression categories to lists of descriptive terms.

    Raises:
        FileNotFoundError: If the JSON file is not found at the specified path.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    if path is None:
        path = Path(__file__).resolve().parents[4] / "Data" / "expression_definition.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# ──────────────────────────────────────────────────────────────
# Token Preprocessing
# ──────────────────────────────────────────────────────────────

def get_valid_tokens(text: str, trigger_map: Dict[str, List[str]]) -> List[str]:
    """
       Extracts semantically relevant tokens from input text based on part-of-speech tags
       and a trigger map of expression phrases.

       This function uses spaCy to tokenize the input text and filters out irrelevant tokens
       (e.g., conjunctions, adverbs). It also allows for overrides to include verbs and auxiliaries
       that appear in the trigger map or end in common participle suffixes ('-ed', '-en').

       Args:
           text (str): Input string to tokenize and filter.
           trigger_map (Dict[str, List[str]]): Mapping from expression categories to trigger phrases.
               Used to include otherwise excluded tokens (like verbs or auxiliaries) if they're listed.

       Returns:
           List[str]: Lowercased list of valid token strings retained after filtering.

       Raises:
           AssertionError: If the token 'is' is not found in the extracted trigger tokens,
               indicating an issue with the input trigger map.
       """
    tokens = nlp(text)
    print(f"[🧪 TOKENS] → {[f'{t.text} ({t.pos_})' for t in tokens]}")

    cleaned = []
    trigger_tokens = get_all_trigger_tokens(trigger_map)
    print(f"[🔍 ALL TRIGGER TOKENS] → {sorted(trigger_tokens)}")
    assert "is" in trigger_tokens, "'is' is not in your expression definition"

    print(f"[🧪 INPUT TEXT] → {text}")
    print(f"[🧪 TOKENS] → {[f'{t.text} ({t.pos_})' for t in tokens]}")

    for token in tokens:
        word = normalize_token(token.text)

        if token.pos_ not in IGNORED_POS:
            cleaned.append(word)
        elif token.pos_ in {"VERB", "AUX"} and word in trigger_tokens:
            print(f"   🔓 OVERRIDE: {word} accepted (trigger-listed {token.pos_})")
            cleaned.append(word)
        elif token.pos_ in {"VERB", "AUX"} and (word.endswith("ed") or word.endswith("en")):
            print(f"   🔓 OVERRIDE: {word} accepted ({token.pos_} ending in -ed/-en)")
            cleaned.append(word)

    print(f"[🧹 VALID TOKENS] → {cleaned}")
    return cleaned

# ──────────────────────────────────────────────────────────────
# Expression Matching
# ──────────────────────────────────────────────────────────────

def find_matching_expressions(text: str, trigger_map: Dict[str, List[str]]) -> List[str]:
    """
       Identifies expression categories from input text using fuzzy token matching and context-aware rules.

       This function detects which expression categories (e.g., "bold", "romantic", "natural") are
       implied by the user input based on a trigger map. It matches both multi-word and single-word
       expressions using fuzzy matching, filters out overlapping hits, and applies contextual promotion
       rules to strengthen or infer weak matches.

       Args:
           text (str): User input text to analyze.
           trigger_map (Dict[str, List[str]]): Mapping from expression category names to lists of trigger phrases.

       Returns:
           List[str]: Sorted list of matched expression categories, with conflicts resolved and promotions applied.
       """
    matched = set()
    tokens = get_valid_tokens(text, trigger_map)
    context_map = load_expression_context_rules()

    multiword_hits = match_multiword_expressions(text, trigger_map)
    matched.update(multiword_hits)

    blocked_tokens = set()
    for phrase in multiword_hits:
        blocked_tokens.update(normalize_token(t) for t in phrase.split())

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
    """
       Maps detected expression categories in the input text to relevant color tones.

       This function first identifies matching expression categories from the text,
       then maps each expression to a list of associated color tones by checking
       if any of its trigger keywords appear as substrings in known tone names.

       Args:
           text (str): User input text to analyze.
           trigger_map (Dict[str, List[str]]): Mapping of expression categories to trigger keywords or phrases.
           known_tones (Set[str]): Set of recognized base tone names.

       Returns:
           Dict[str, List[str]]: Dictionary where keys are matched expression categories and
                                 values are sorted lists of relevant tone names.
       """
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
    """
      Loads expression context rules from a JSON file.

      These rules define additional logic for promoting expression categories
      based on the presence of specific contextual clues in the input text.
      Each rule typically includes required tokens and contextual hints.

      Args:
          path (Optional[str]): Optional custom path to the context rules JSON file.
              If not provided, a default path is used based on the project structure.

      Returns:
          Dict[str, Dict[str, List[str]]]: Mapping of expression names to their
          contextual promotion criteria, including 'require_tokens' and 'context_clues'.

      Raises:
          FileNotFoundError: If the JSON file is missing at the given path.
          json.JSONDecodeError: If the JSON file contains invalid content.
      """
    default_path = Path(__file__).resolve().parents[4] / "Data" / "expression_context_rules.json"
    with (Path(path) if path else default_path).open("r", encoding="utf-8") as f:
        return json.load(f)

def apply_expression_context_rules(
    tokens: List[str],
    matched_expressions: Set[str],
    context_map: Dict[str, Dict[str, List[str]]]
) -> Set[str]:
    """
       Applies context-based promotion rules to infer additional expression categories.

       This function promotes expressions that were not initially matched by direct triggers,
       by checking if the token list satisfies both required tokens and contextual clues
       defined in the context map. Expressions already matched are skipped.

       Args:
           tokens (List[str]): List of lowercase tokens from the input text.
           matched_expressions (Set[str]): Set of expressions already matched directly.
           context_map (Dict[str, Dict[str, List[str]]]): Mapping from expression names to their
               'require_tokens' and 'context_clues' for contextual promotion.

       Returns:
           Set[str]: Set of newly promoted expression categories based on context.
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

EXPRESSION_SUPPRESSION_RULES = {
    "soft glam": {"glamorous"}
}

def suppress_conflicting_expressions(matched: Set[str]) -> Set[str]:
    """
        Suppresses conflicting expression categories based on predefined dominance rules.

        This function enforces logical consistency by removing lower-priority expressions
        if a dominant expression is already present. The suppression logic is driven by
        the `EXPRESSION_SUPPRESSION_RULES` mapping, which defines which expressions should
        be excluded when a dominant one is matched.

        Args:
            matched (Set[str]): Set of initially matched expression categories.

        Returns:
            Set[str]: Filtered set of expression categories with conflicts resolved.
        """
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
    """
        Analyzes color phrases to extract tones and modifiers, and builds bidirectional mappings between them.

        This function parses each phrase into tokens, identifies which tokens are recognized as tones
        or modifiers, and constructs mappings that associate modifiers with tones and vice versa.

        Args:
            phrases (List[str]): List of simplified color phrases (e.g., ['soft pink', 'vibrant red']).
            known_tones (Set[str]): Set of valid tone names.
            known_modifiers (Set[str]): Set of recognized modifier terms.

        Returns:
            Tuple containing:
                - Set[str]: All tones found in the input phrases.
                - Set[str]: All modifiers found in the input phrases.
                - Dict[str, Set[str]]: Mapping from modifier → associated tones.
                - Dict[str, Set[str]]: Mapping from tone → associated modifiers.
        """
    tones = set()
    modifiers = set()
    modifier_to_tone = defaultdict(set)
    tone_to_modifier = defaultdict(set)

    for phrase in phrases:
        tokens = [normalize_token(part) for part in phrase.split()]
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
    """
       Categorizes color-related phrases into tones, modifiers, and their bidirectional mappings.

       This function analyzes a list of simplified phrases to extract recognized tones and modifiers,
       and builds structured mappings between them. The output is sorted and formatted for downstream
       use in recommendation, filtering, or visualization tasks.

       Args:
           phrases (List[str]): List of simplified color phrases (e.g., ['soft pink', 'bold red']).
           known_tones (Set[str]): Set of valid base tone names.
           known_modifiers (Set[str]): Set of known color modifiers.

       Returns:
           Dict[str, object]: A dictionary containing:
               - "tones" (List[str]): Sorted list of detected tones.
               - "modifiers" (List[str]): Sorted list of detected modifiers.
               - "modifier_to_tone" (Dict[str, List[str]]): Mapping from each modifier to its associated tones.
               - "tone_to_modifier" (Dict[str, List[str]]): Mapping from each tone to its associated modifiers.
       """
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
    """
        Categorizes a list of color phrases into tones and modifiers using known vocabularies.

        This function is a convenience wrapper around `categorize_color_tokens_with_mapping`,
        using the globally available `known_tones` set. It returns structured mappings of tones
        and modifiers for downstream color preference logic.

        Args:
            phrases (List[str]): List of simplified color phrases (e.g., ['muted coral', 'vibrant pink']).
            known_modifiers (Set[str]): Set of valid color modifiers.

        Returns:
            Dict[str, List[str]]: Dictionary with:
                - "tones": Sorted list of tones.
                - "modifiers": Sorted list of modifiers.
                - "modifier_to_tone": Mapping of each modifier to its related tones.
                - "tone_to_modifier": Mapping of each tone to its related modifiers.
        """
    return categorize_color_tokens_with_mapping(phrases, known_tones, known_modifiers)
