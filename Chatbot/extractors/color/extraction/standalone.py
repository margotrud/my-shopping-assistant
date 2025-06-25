# Chatbot/extractors/color/extraction/standalone.py
"""
standalone.py
=============

Handles extraction of standalone tone/modifier terms,
including simplified and injected expressions.
"""

from Chatbot.extractors.color.shared.constants import COSMETIC_NOUNS
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token


def extract_standalone_phrases(tokens, known_modifiers, known_tones, debug=False):
    all_terms = _inject_expression_modifiers(tokens, known_modifiers, debug)
    filtered_terms = _extract_filtered_tokens(tokens, known_modifiers, known_tones, debug)
    final = _finalize_standalone_phrases(all_terms, filtered_terms, debug)
    return final


def _inject_expression_modifiers(tokens, known_modifiers, debug):
    injected = set()
    for tok in tokens:
        if tok.pos_ in {"ADJ", "NOUN"}:
            word = normalize_token(tok.text)
            if word in known_modifiers and word not in COSMETIC_NOUNS:
                injected.add(word)
                if debug:
                    print(f"[🎯 INJECTED] '{word}' (modifier or useful noun)")
    return injected

def _extract_filtered_tokens(tokens, known_modifiers, known_tones, debug):
    result = set()
    for tok in tokens:
        raw = normalize_token(tok.text)
        if raw in COSMETIC_NOUNS:
            continue
        resolved = resolve_modifier_token(raw, known_modifiers, known_tones)
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
    matches = set()
    for tok in tokens:
        raw = normalize_token(tok.text)
        if raw in known_tones:
            matches.add(raw)
            if debug:
                print(f"[🎯 LONE TONE] Found '{raw}'")
    return matches

