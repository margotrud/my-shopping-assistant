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

