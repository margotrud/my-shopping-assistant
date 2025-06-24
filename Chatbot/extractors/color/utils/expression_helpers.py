# Chatbot/extractors/color/utils/expression_helpers.py

"""
expression_helpers.py
=====================

Helpers to extract trigger vocabularies from expression definitions.

Used By:
--------
- Expression matching (contextual tone detection)
- Compound token splitting (glued token fallback)
"""

from typing import Dict, List, Set
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers


def get_all_trigger_tokens() -> Dict[str, List[str]]:
    """
    Extracts all modifier/alias tokens per expression.

    Loads 'expression_definition.json', which should look like:
    {
        "romantic": {
            "modifiers": ["soft", "flirty"],
            "aliases": ["date", "lovely"]
        },
        ...
    }

    Returns:
        Dict[str, List[str]]: Mapping from expression → list of tokens (modifiers + aliases).
    """
    expression_map = load_json_from_data_dir("expression_definition.json")
    trigger_map = {}

    for expr, rules in expression_map.items():
        mods = rules.get("modifiers", [])
        aliases = rules.get("aliases", [])
        tokens = list(set(mods + aliases))
        if tokens:
            trigger_map[expr] = tokens

    return trigger_map


def get_glued_token_vocabulary() -> Set[str]:
    """
    Constructs the full vocabulary of tokens eligible for glued compound matching.

    This includes:
    - Known tones
    - Known modifiers
    - All known CSS/XKCD webcolor names

    Returns:
        Set[str]: Vocabulary set used in compound splitting.
    """
    known_modifiers = load_known_modifiers()
    return known_tones.union(known_modifiers).union(all_webcolor_names)
