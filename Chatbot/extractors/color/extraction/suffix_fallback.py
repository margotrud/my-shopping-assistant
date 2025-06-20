from typing import List, Set

import spacy

from Chatbot.extractors.color.utils.token_utils import singularize


from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed

def extract_suffix_fallbacks(
    tokens: List[spacy.tokens.Token],
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool
) -> List[str]:
    """
    Extracts suffix-based tone candidates like 'peachy', 'bluish', etc.,
    by checking direct tone/webcolor inclusion or validating via simplification.

    Args:
        tokens (List[spacy.tokens.Token]): spaCy tokenized input.
        known_tones (Set[str]): Valid tone vocabulary (CSS, XKCD, etc.).
        known_modifiers (Set[str]): Known color modifiers (e.g., 'soft').
        all_webcolor_names (Set[str]): Web-safe color names (CSS3, CSS21).
        debug (bool): If True, prints diagnostic messages.

    Returns:
        List[str]: Valid suffix fallback matches.
    """
    results = []

    for t in tokens:
        norm = singularize(t.text.lower())

        if not norm.endswith(("y", "ish")):
            continue  # Skip if it doesn't match suffix pattern

        if debug:
            print("\n[🔍 TOKEN CHECK]")
            print(f"→ Raw text     : {t.text}")
            print(f"→ Lowered norm : {norm}")
            print(f"→ POS tag      : {t.pos_}")
            print(f"→ Modifier?    : {norm in known_modifiers}")
            print(f"→ Known tone?  : {norm in known_tones}")
            print(f"→ Webcolor?    : {norm in all_webcolor_names}")

        # Direct inclusion (skip modifier check to allow peachy etc.)
        if norm in known_tones or norm in all_webcolor_names:
            results.append(norm)
            if debug:
                print(f"[✅ SUFFIX FALLBACK ADDED] (direct match) → '{norm}'")
            continue

        # Fallback via simplifier
        simplified = simplify_phrase_if_needed(norm)
        flat_simplified = " ".join(simplified)
        simplified_tokens = flat_simplified.split()
        simplified_tokens_lower = [tok.lower() for tok in simplified_tokens]

        if debug:
            print(f"[🔁 SIMPLIFIER OUTPUT] for '{norm}' → {simplified}")
            print(f"[🧪 VALIDATING SIMPLIFIED TOKENS] → {simplified_tokens_lower}")
            print(f"[✅ TOKENS IN KNOWN TONES] → {[tok for tok in simplified_tokens_lower if tok in known_tones]}")

        if simplified and any(tok in known_tones for tok in simplified_tokens_lower):
            results.append(norm)
            if debug:
                print(f"[✅ SUFFIX FALLBACK ADDED] (validated by simplifier) → '{norm}'")
        else:
            if debug:
                print(f"[⛔ IGNORED] No valid simplified tone match for → '{norm}'")

    if debug:
        print(f"\n[🏁 FINAL FALLBACK RESULTS] → {results}")

    return results


