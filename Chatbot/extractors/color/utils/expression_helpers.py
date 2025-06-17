# Chatbot/extractors/general/helpers/token_vocab.py

"""
Token Vocabulary Utilities
===========================

This module provides foundational vocabulary utilities used throughout
the color and expression analysis pipeline of the shopping assistant.

Functions included here serve two primary purposes:

1. **Token extraction from trigger expressions**
   - `get_all_trigger_tokens` flattens complex expression mappings
     into a set of lowercase word tokens, enabling fuzzy match lookups,
     especially for verbs and adjectives like "glow", "refined", or "shine".

2. **Glued token segmentation support**
   - `get_glued_token_vocabulary` generates a complete set of valid single-word
     tones and modifiers. This is used to split compound tokens (e.g., "greige")
     during parsing by matching to known vocabularies (XKCD, CSS3, and cosmetic modifiers).

These utilities are lightweight and optimized for reusability across modules like:
- `categorizer.py`
- `matcher.py`
- `phrase_extractor.py`
- `sentiment.py`

They are designed to be:
- Compact
- Readable
- Fully test-covered
- Free from hardcoding or mutation

This module is essential for enabling dynamic token-level analysis
within color expression matching and user preference extraction.

"""


from typing import Dict, List, Set

from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers


def get_all_trigger_tokens(trigger_map: Dict[str, List[str]]) -> Set[str]:
    """
    Extract individual lowercase tokens from all trigger phrases.
    Used to dynamically allow fuzzy matches (even verbs like 'glow').

    Args:
        trigger_map (Dict[str, List[str]]): Expression → phrases

    Returns:
        Set[str]: All unique lowercase words from trigger phrases
    """
    tokens = set()
    for phrases in trigger_map.values():
        for phrase in phrases:
            tokens.update(phrase.lower().split())
    return tokens

def get_glued_token_vocabulary() -> set[str]:
    """
    Returns the unified set of single-word color tokens for token splitting.
    Combines known tones and modifiers.
    """
    return {t for t in known_tones.union(load_known_modifiers()) if " " not in t}

