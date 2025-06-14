#Chatbot/extractors/color/logic/color_categorizer.py
# color_categorizer.py
"""
color_categorizer.py
=====================
Analyzes modifier-tone relationships from cleaned descriptive color phrases.

Used to:
- Build mappings of tone ↔ modifier for filtering, clustering, or tag scoring
- Derive simplified tone/modifier sets from extracted phrases

Called during:
- Post-processing of extracted color expressions
- Expression context refinement pipelines
"""

from typing import List, Set, Dict, Tuple
from collections import defaultdict

def build_tone_modifier_mappings(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Tuple[Set[str], Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Extracts tone-modifier relationships from a list of color phrases.

    For each phrase like 'soft pink' or 'vibrant red', this function:
    - Identifies known tone and modifier tokens
    - Records bidirectional links between tones and modifiers
    - Returns:
        - Unique tones and modifiers
        - Mapping from modifier → associated tones
        - Mapping from tone → associated modifiers

    Args:
        phrases (List[str]): Descriptive color phrases (e.g., ['soft pink']).
        known_tones (Set[str]): Valid tone names.
        known_modifiers (Set[str]): Recognized modifier tokens.

    Returns:
        Tuple:
            Set[str]: All tones found in input.
            Set[str]: All modifiers found in input.
            Dict[str, Set[str]]: modifier → tones
            Dict[str, Set[str]]: tone → modifiers
    """
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


def format_tone_modifier_mappings(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Dict[str, object]:
    """
    Produces a sorted, presentation-friendly mapping of tones and modifiers from color phrases.

    This wraps the raw tone/modifier extraction with sorted lists and dict formatting
    to enable easy downstream use (e.g., UI display, API payloads, or visualization layers).

    Args:
        phrases (List[str]): List of simplified color phrases (e.g., ['soft pink']).
        known_tones (Set[str]): Recognized tone names.
        known_modifiers (Set[str]): Recognized modifier tokens.

    Returns:
        Dict[str, object]: Structured tone-modifier representation:
            - "tones": Sorted list of matched tones
            - "modifiers": Sorted list of matched modifiers
            - "modifier_to_tone": Dict of modifier → sorted tones
            - "tone_to_modifier": Dict of tone → sorted modifiers
    """
    tones, modifiers, modifier_to_tone, tone_to_modifier = build_tone_modifier_mappings(
        phrases, known_tones, known_modifiers
    )

    return {
        "tones": sorted(tones),
        "modifiers": sorted(modifiers),
        "modifier_to_tone": {mod: sorted(tset) for mod, tset in modifier_to_tone.items()},
        "tone_to_modifier": {tone: sorted(mset) for tone, mset in tone_to_modifier.items()},
    }
