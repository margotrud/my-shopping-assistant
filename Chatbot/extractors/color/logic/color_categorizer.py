#Chatbot/extractors/color/logic/color_categorizer.py
"""
color_categorizer.py
====================

Extracts tone-modifier relationships from descriptive color phrases.
Builds bidirectional mappings between tone keywords and modifier keywords.
"""
from typing import List, Set, Tuple, Dict
from collections import defaultdict

def build_tone_modifier_mappings(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Tuple[Set[str], Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Builds tone-modifier mappings from a list of descriptive color phrases.

    For example, given: ['soft pink', 'bold red']
    And vocab: tones = {'pink', 'red'}, modifiers = {'soft', 'bold'}

    It produces:
    - tone set: {'pink', 'red'}
    - modifier set: {'soft', 'bold'}
    - modifier → tones: {'soft': {'pink'}, 'bold': {'red'}}
    - tone → modifiers: {'pink': {'soft'}, 'red': {'bold'}}

    Args:
        phrases (List[str]): List of color phrases (e.g., 'deep nude').
        known_tones (Set[str]): All known tone tokens.
        known_modifiers (Set[str]): All known modifier tokens.

    Returns:
        Tuple[
            Set[str],                        # All matched tones
            Set[str],                        # All matched modifiers
            Dict[str, Set[str]],             # modifier → tones
            Dict[str, Set[str]]              # tone → modifiers
        ]
    """
    tones = set()
    modifiers = set()
    mod_to_tone = defaultdict(set)
    tone_to_mod = defaultdict(set)

    for phrase in phrases:
        parts = phrase.lower().split()
        if len(parts) != 2:
            continue

        mod, tone = parts
        if mod in known_modifiers and tone in known_tones:
            tones.add(tone)
            modifiers.add(mod)
            mod_to_tone[mod].add(tone)
            tone_to_mod[tone].add(mod)

    return tones, modifiers, mod_to_tone, tone_to_mod


def format_tone_modifier_mappings(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Dict[str, Dict[str, List[str]]]:
    """
    Produces a sorted and display-friendly mapping dictionary.

    Returns a structure like:
    {
        "modifiers": {
            "soft": ["pink", "peach"]
        },
        "tones": {
            "pink": ["soft", "dusty"]
        }
    }

    Args:
        phrases (List[str]): Input color phrases
        known_tones (Set[str]): Known tone vocab
        known_modifiers (Set[str]): Known modifier vocab

    Returns:
        Dict[str, Dict[str, List[str]]]
    """
    tones, modifiers, mod_to_tone, tone_to_mod = build_tone_modifier_mappings(
        phrases, known_tones, known_modifiers
    )

    return {
        "modifiers": {
            mod: sorted(list(tones)) for mod, tones in mod_to_tone.items()
        },
        "tones": {
            tone: sorted(list(mods)) for tone, mods in tone_to_mod.items()
        }
    }