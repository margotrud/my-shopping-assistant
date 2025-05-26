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

from typing import List, Set, Dict, Tuple
from collections import defaultdict
from Chatbot.extractors.color import known_tones

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
    """
    Analyze color phrases to extract unique tones, modifiers, and their mappings.
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
    Convenience wrapper function to categorize color phrases.
    Invokes categorize_color_tokens_with_mapping with parameters
    reordered to improve semantic clarity.

    Args:
        phrases (List[str]): List of descriptive color phrases.
        known_modifiers (Set[str]): Set of recognized modifiers.
        known_tones (Set[str]): Set of recognized tones.

    Returns:
        Dict[str, List[str]]: Categorized tone and modifier data.
    """
    return categorize_color_tokens_with_mapping(phrases, known_tones, known_modifiers)
