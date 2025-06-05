"""
Modifier Resolution Logic
-------------------------
Provides logic to resolve modifier candidates:
- Exact match
- Heuristic suffix fallback (e.g., 'peachy' → 'peach')
- Fuzzy match
- Suppression of misclassified tone-modifier combos
"""

from typing import Optional, Set
from Chatbot.extractors.color.core.matcher import fuzzy_match_modifier


def resolve_modifier_with_suffix_fallback(
    word: str,
    known_modifiers: Set[str],
    known_tones: Optional[Set[str]] = None,
    allow_fuzzy: bool = True,
    is_tone: bool = False
) -> Optional[str]:
    """
    Resolve a modifier token using:
    - tone demotion (e.g., 'peachy' → 'peach')
    - exact match
    - suffix heuristics
    - fuzzy fallback (if enabled)

    Args:
        word: Raw token candidate.
        known_modifiers: Valid modifiers.
        known_tones: Valid base tones (optional).
        allow_fuzzy: Allow fuzzy match fallback.
        is_tone: Restrict to tone context.

    Returns:
        Resolved modifier or None.
    """
    # 1. Check suffix demotion (e.g., 'peachy' → 'peach' if tone)
    override = _override_if_tone_suffix(word, known_tones)
    if override and not is_tone:
        return override

    if _should_block_as_modifier(word, known_tones):
        return None

    # 2. Exact match
    if word in known_modifiers:
        return word

    # 3. Suffix heuristic: e.g., "glowy" → "glow"
    for mod in known_modifiers:
        if word.startswith(mod) and word.endswith(("ish", "y")) and len(word) <= len(mod) + 3:
            return mod

    # 4. Fuzzy match (optional)
    if allow_fuzzy or not is_tone:
        return fuzzy_match_modifier(word, known_modifiers)

    return None


def should_suppress_compound(
    raw_modifier: str,
    resolved_modifier: Optional[str],
    resolved_tone: Optional[str],
    known_tones: Set[str]
) -> bool:
    """
    Prevent misinterpretation of tone-based modifiers.

    Example: 'peachy pink' might falsely yield 'peach pink'
             → suppress if 'peach' is already a tone, and no valid tone was detected.

    Args:
        raw_modifier: Original token before resolution.
        resolved_modifier: Candidate resolved modifier.
        resolved_tone: Tone detected from phrase.
        known_tones: Valid tone vocabulary.

    Returns:
        True if compound should be suppressed.
    """
    if (
        raw_modifier.endswith("y")
        and resolved_modifier in known_tones
        and resolved_tone is None
    ):
        return True
    return False


def _override_if_tone_suffix(word: str, known_tones: Optional[Set[str]]) -> Optional[str]:
    if known_tones and word.endswith("y"):
        base = word[:-1]
        if base in known_tones:
            return base
    return None


def _should_block_as_modifier(word: str, known_tones: Optional[Set[str]]) -> bool:
    """
    Prevents demoted tones from being reused as modifiers.

    Args:
        word: Token to check.
        known_tones: Valid tones.

    Returns:
        True if token should be blocked.
    """
    if known_tones and word.endswith("y"):
        base = word[:-1]
        return base in known_tones
    return False
