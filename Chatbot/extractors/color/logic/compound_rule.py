#Chatbot/extractors/color/logic/compound_rules.py

"""
compound_rules.py
==================
Domain-specific rules for filtering invalid modifier-tone combinations
during compound color phrase extraction.

Includes:
- Blocklist suppression (e.g., 'light night')
- Symmetric matching for modifier-tone and tone-modifier pairs
"""

from typing import Set, Tuple


def is_blocked_modifier_tone_pair(
    modifier: str,
    tone: str,
    blocked_pairs: Set[Tuple[str, str]]
) -> bool:
    """
    Checks whether a given modifier-tone pair is explicitly blocked.

    This is used to suppress confusing or invalid compound color phrases
    such as 'light night' or 'romantic dramatic'.

    Args:
        modifier (str): Modifier candidate (e.g., 'light').
        tone (str): Tone or color candidate (e.g., 'night').
        blocked_pairs (Set[Tuple[str, str]]): Known bad pairs to suppress.

    Returns:
        bool: True if the (modifier, tone) pair or its reverse is blocked.
    """
    pair = (modifier.lower(), tone.lower())
    reverse = (tone.lower(), modifier.lower())
    return pair in blocked_pairs or reverse in blocked_pairs
