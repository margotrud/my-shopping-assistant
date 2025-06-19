from typing import List, Set

import spacy

from Chatbot.extractors.color.utils.token_utils import singularize


from Chatbot.extractors.color.llm. import simplify_phrase_if_needed

def extract_suffix_fallbacks(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts suffix-based tone candidates like 'peachy', 'bluish', even if not in known sets,
    by validating via simplification cache/LLM if needed.
    """
    results = []

    for t in tokens:
        norm = singularize(t.text.lower())

        if (
            t.pos_ == "ADJ"
            and norm.endswith(("y", "ish"))
            and norm not in known_modifiers
        ):
            if norm in known_tones or norm in all_webcolor_names:
                results.append(norm)
                if debug:
                    print(f"[✅ SUFFIX FALLBACK ADDED] (direct match) → '{norm}'")
            else:
                simplified = simplify_phrase_if_needed(norm)
                if simplified and any(tone in known_tones for tone in " ".join(simplified).split()):
                    results.append(norm)
                    if debug:
                        print(f"[✅ SUFFIX FALLBACK ADDED] (validated by simplifier) → '{norm}'")

    return results
