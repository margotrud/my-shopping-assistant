# Chatbot/extractors/color/extraction/standalone.py
"""
standalone.py
=============

Handles extraction of standalone tone/modifier terms,
including simplified and injected expressions.
"""

from Chatbot.extractors.color.shared.constants import COSMETIC_NOUNS
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token, fuzzy_match_modifier_safe
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def extract_standalone_phrases(tokens, known_modifiers, known_tones, debug=False):
    all_terms = _inject_expression_modifiers(tokens, known_modifiers, debug)
    filtered_terms = _extract_filtered_tokens(tokens, known_modifiers, known_tones, debug)
    final = _finalize_standalone_phrases(all_terms, filtered_terms, debug)
    return final


def levenshtein_distance(a, b):
    """Simple Levenshtein approximation: how many characters differ."""
    return sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))

def is_suffix_variant(word: str, base: str, debug=False) -> bool:
    if debug:
        print(f"[🧪 SUFFIX CHECK] word='{word}', base='{base}'")

    if word == base:
        if debug:
            print(f"[❌ NOT SUFFIX] word == base → no suffix")
        return False

    allowed_suffixes = {"y", "ish"}
    suffix = ""

    if word.startswith(base):
        suffix = word[len(base):]
        if debug:
            print(f"[🧪 SUFFIX EXTRACTED] word starts with base → suffix='{suffix}'")
        if suffix in allowed_suffixes:
            print(f"[✅ VALID SUFFIX] '{word}' = '{base}' + '{suffix}'")
            return True
    elif base.endswith("e") and word.startswith(base[:-1]):
        suffix = word[len(base) - 1:]
        if debug:
            print(f"[🧪 ALT-SUFFIX CHECK] Trying base minus 'e' → suffix='{suffix}'")
        if suffix in allowed_suffixes:
            print(f"[✅ ALT VALID SUFFIX] '{word}' = '{base[:-1]}' + '{suffix}' (from '{base}')")
            return True

    if debug:
        print(f"[❌ NOT A SUFFIX VARIANT] (word='{word}', base='{base}')")
    return False

def _inject_expression_modifiers(tokens, known_modifiers, debug):
    injected = set()
    for tok in tokens:
        print(f"[TOKEN LOOP] Raw token: '{tok.text}' | POS={tok.pos_} | TAG={tok.tag_}")

        word = normalize_token(tok.text)
        print(f"[🔍 NORMALIZED] '{tok.text}' → '{word}' | In known_modifiers? → {word in known_modifiers}")

        # ✅ Always allow fuzzy attempts for PROPN or VERB too
        if (
            tok.pos_ in {"ADJ", "NOUN"} or
            tok.tag_ in {"VBN", "VBD"} or
            tok.pos_ == "VERB" or
            tok.pos_ == "PROPN"
        ):
            print(f"\n[🧪 CHECKING] Token: '{tok.text}' → normalized: '{word}'")

            if tok.pos_ == "NOUN" and word in COSMETIC_NOUNS:
                if debug:
                    print(f"[⛔ SKIP] Token '{word}' is a cosmetic noun → blocked")
                continue

            # ✅ Direct match
            if word in known_modifiers:
                injected.add(word)
                print(f"[🎯 INJECTED] '{word}' (direct match in known_modifiers)")

            # ✅ Fuzzy match fallback
            else:
                fuzzy = fuzzy_match_modifier_safe(word, known_modifiers, threshold=85)
                print(f"[DEBUG] Best match: '{fuzzy}' with score 85" if fuzzy else "[❌ NO FUZZY MATCH FOUND]")

                if fuzzy:
                    distance = levenshtein_distance(fuzzy, word)
                    suffix_ok = is_suffix_variant(word, fuzzy, debug=True)

                    print(f"[📐 LEVENSHTEIN] '{word}' vs '{fuzzy}' → {distance}")
                    print(f"[🔎 FINAL DECISION FLAGS] fuzzy='{fuzzy}' | dist={distance} | suffix_ok={suffix_ok}")

                    if (
                        fuzzy == word or
                        (suffix_ok and distance <= 2) or
                        (not suffix_ok and 2 <= distance <= 3)
                    ):
                        injected.add(fuzzy)
                        print(f"[🎯 INJECTED] '{word}' (fuzzy → '{fuzzy}', dist={distance}, suffix_ok={suffix_ok})")
                    else:
                        print(f"[⛔ SKIPPED] '{word}' (fuzzy='{fuzzy}', dist={distance}, suffix_ok={suffix_ok})")

    return injected


def _extract_filtered_tokens(tokens, known_modifiers, known_tones, debug):
    result = set()

    for tok in tokens:
        raw = normalize_token(tok.text)

        if debug:
            print(f"\n[🧪 TOKEN] '{tok.text}' → normalized: '{raw}' (POS={tok.pos_})")
            print(f"[🔎 CHECK] In COSMETIC_NOUNS? → {raw in COSMETIC_NOUNS}")

        # ✅ Block known cosmetic nouns
        if raw in COSMETIC_NOUNS:
            if debug:
                print(f"[⛔ SKIPPED] Cosmetic noun '{raw}' blocked")
            continue

        # ✅ Skip connector words (and, or, etc.) via POS tag
        if tok.pos_ == "CCONJ":
            if debug:
                print(f"[⛔ SKIPPED] Connector '{raw}' ignored (POS=CCONJ)")
            continue

        # ✅ Resolve token
        resolved = resolve_modifier_token(raw, known_modifiers, known_tones)

        if debug:
            print(f"[🔍 RESOLVED] '{raw}' → '{resolved}'")
            print(f"[📌 raw ∈ tones?] {raw in known_tones}")
            print(f"[📌 resolved ∈ tones?] {resolved in known_tones if resolved else '—'}")
            print(f"[📏 resolved == raw?] {resolved == raw if resolved else '—'}")
            print(f"[📏 resolved starts with raw?] {resolved.startswith(raw) if resolved else '—'}")
            print(f"[📐 contains hyphen?] {'-' in resolved if resolved else '—'}")
            print(f"[🧮 total matches so far] {len(result)}")

        # 🔒 Block fuzzy match result if too short to trust
        if len(raw) <= 3 and resolved != raw:
            if debug:
                print(f"[⛔ REJECTED] Token '{raw}' too short for safe fuzzy match → '{resolved}'")
            continue

        # 🔒 Reject fuzzy compound result unless raw is root
        if resolved and "-" in resolved and not resolved.startswith(raw):
            if debug:
                print(f"[⛔ REJECTED] Fuzzy '{raw}' → '{resolved}' (compound mismatch)")
            continue

        # 🔒 Reject multi-word result from a single token
        if resolved and " " in resolved and " " not in raw:
            if debug:
                print(f"[⛔ REJECTED] Fuzzy '{raw}' → '{resolved}' (multi-word result from single token)")
            continue

        # 🔒 If already have strong matches, skip risky fuzzy ones
        if len(result) >= 3 and resolved != raw:
            if debug:
                print(f"[⛔ REJECTED] Skipping fuzzy '{raw}' → '{resolved}' (already 3+ matches)")
            continue

        if resolved:
            result.add(resolved)
            if debug:
                print(f"[🎯 STANDALONE MATCH] '{raw}' → '{resolved}'")

    return result

def _finalize_standalone_phrases(injected, filtered, debug):
    combined = injected.union(filtered)
    if debug:
        print(f"[✅ FINAL STANDALONE SET] {combined}")
    return combined
def extract_lone_tones(tokens, known_tones, debug=False):
    """
    Extracts standalone tone tokens directly from token stream.

    This version:
    - Uses normalize_token() for cleanup
    - Skips cosmetic product nouns (e.g., 'lipstick', 'blush')
    - Accepts any token directly in known_tones

    Args:
        tokens (List[spacy.tokens.Token]): spaCy tokens
        known_tones (Set[str]): Tone vocabulary
        debug (bool): If True, prints debug info

    Returns:
        Set[str]: Set of matched tone tokens
    """
    matches = set()
    for tok in tokens:
        raw = normalize_token(tok.text)
        if raw in COSMETIC_NOUNS:
            if debug:
                print(f"[⛔ COSMETIC BLOCK] '{raw}' blocked")
            continue
        if raw in known_tones:
            matches.add(raw)
            if debug:
                print(f"[🎯 LONE TONE] Found '{raw}'")
    return matches
