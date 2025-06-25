#Chatbot/extractors/color/logic/compound_rules.py

"""
compound_rule.py
=================
Domain-specific rules for filtering invalid modifier-tone combinations
during compound color phrase extraction.

Used By:
--------
- extract_from_adjacent()
- extract_from_split()
- extract_from_glued()

Key Logic:
----------
- Explicit pair blocklist using known rejection tuples

Dependencies:
-------------
- BLOCKED_TOKENS from Chatbot.extractors.color.shared.constants
"""

from typing import Set, Tuple
from Chatbot.extractors.color.shared.constants import BLOCKED_TOKENS
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def is_blocked_modifier_tone_pair(
    modifier: str,
    tone: str,
    blocked_pairs: Set[Tuple[str, str]] = BLOCKED_TOKENS
) -> bool:
    """
    Checks whether a modifier-tone pair is explicitly blocked.

    This function helps suppress invalid or misleading combinations
    such as 'light night' or 'romantic dramatic', by consulting a
    domain-specific blocklist.

    Args:
        modifier (str): Modifier word (e.g., 'light').
        tone (str): Tone or color word (e.g., 'night').
        blocked_pairs (Set[Tuple[str, str]]): Optional override blocklist.

    Returns:
        bool: True if either (modifier, tone) or (tone, modifier) is blocked.
    """
    pair = (normalize_token(modifier), normalize_token(tone))
    reverse = (normalize_token(tone), normalize_token(modifier))
    return pair in blocked_pairs or reverse in blocked_pairs