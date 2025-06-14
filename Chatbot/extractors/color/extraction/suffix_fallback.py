def extract_suffix_fallbacks(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts tone candidates based on suffix fallback patterns (e.g., 'peachy', 'bluish').

    This function identifies adjectives ending in suffixes like 'y' or 'ish',
    which are often used to describe tones informally in cosmetic or fashion contexts.

    The function filters out:
    - Known modifiers (to avoid duplicate classification)
    - Non-adjectives
    - Invalid color names

    Args:
        tokens (List[spacy.tokens.Token]): Parsed spaCy tokens from user input.
        known_tones (Set[str]): Set of valid base tone terms.
        known_modifiers (Set[str]): Set of known modifiers (to exclude).
        all_webcolor_names (Set[str]): Known CSS/XKCD web color names.
        debug (bool): If True, enables verbose debug logging.

    Returns:
        List[str]: Valid suffix-based tone candidates.
    """
    results = []

    for t in tokens:
        norm = singularize(t.text.lower())

        if (
            t.pos_ == "ADJ"
            and norm.endswith(("y", "ish"))
            and norm not in known_modifiers
            and (norm in known_tones or norm in all_webcolor_names)
        ):
            results.append(norm)
            if debug:
                print(f"[✅ SUFFIX FALLBACK ADDED] → '{norm}'")

    return results
