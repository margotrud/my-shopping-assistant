#Chatbot/extractors/color/logic/color_categorizer.py
"""
color_categorizer.py
====================

Extracts tone-modifier relationships from descriptive color phrases.
Builds bidirectional mappings between tone keywords and modifier keywords.
"""
from typing import List, Set, Tuple, Dict
from collections import defaultdict

from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def build_tone_modifier_mappings(
        phrases: List[str],
        known_tones: Set[str],
        known_modifiers: Set[str]
) -> Tuple[Set[str], Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Builds tone-modifier mappings from descriptive phrases.
    Automatically accepts derived suffix forms like 'glowy' → 'glow'
    or 'rosy' → 'rose' if the base is in known_modifiers.

    Args:
        phrases (List[str]): Descriptive phrases (e.g., ['soft pink']).
        known_tones (Set[str]): Set of recognized tone tokens.
        known_modifiers (Set[str]): Set of recognized modifier tokens.

    Returns:
        Tuple:
            - tones (Set[str]): All matched tone tokens.
            - modifiers (Set[str]): All matched modifier tokens (including suffix forms).
            - mod_to_tone (Dict[str, Set[str]]): Modifier → Tones mapping.
            - tone_to_mod (Dict[str, Set[str]]): Tone → Modifiers mapping.
    """

    def normalize_modifier(token: str) -> str | None:
        for suffix in ("y", "ish"):
            if token.endswith(suffix):
                base = token[:-len(suffix)]
                if base in known_modifiers:
                    return token
                if base + "e" in known_modifiers:
                    return token
        return token if token in known_modifiers else None

    tones = set()
    modifiers = set()
    mod_to_tone = defaultdict(set)
    tone_to_mod = defaultdict(set)

    for phrase in phrases:
        parts = [normalize_token(t) for t in phrase.split()]
        if len(parts) != 2:
            continue

        mod_raw, tone = parts
        mod = normalize_modifier(mod_raw)

        if mod and tone in known_tones:
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

