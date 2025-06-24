"""
color_pipeline.py
=================

Orchestrates color phrase simplification and resolution using rules, fallback, and LLM.
"""
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.rgb_distance import choose_representative_rgb
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.color.llm.llm_rgb import resolve_rgb_with_llm
from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed
from Chatbot.extractors.color.llm.simplifier import simplify_color_description_with_llm

def process_color_phrase(
    phrase,
    known_modifiers,
    all_webcolor_names,
    llm_client=None,
    cache=None,
    debug=False
):
    """
    Full pipeline: simplify phrase (rule → suffix → LLM), resolve RGB, and return final RGB match.
    """
    simplified = simplify_phrase_if_needed(phrase, known_modifiers, known_tones, debug)

    if simplified == phrase and llm_client:
        if debug:
            print(f"[🧠 LLM FALLBACK] No simplification found for '{phrase}', trying LLM")
        simplified = simplify_color_description_with_llm(phrase, llm_client, cache, debug)

    rgb = resolve_rgb_with_llm(simplified, all_webcolor_names, llm_client, cache, debug)
    if debug:
        print(f"[🎨 FINAL RGB] '{simplified}' → {rgb}")
    return simplified, rgb


def process_segment_colors(
    color_phrases,
    known_modifiers,
    all_webcolor_names,
    llm_client=None,
    cache=None,
    debug=False
):
    """
    Process a list of raw color phrases → simplified + RGB list
    """
    simplified = []
    rgb_list = []

    for phrase in color_phrases:
        simple, rgb = process_color_phrase(
            phrase,
            known_modifiers,
            all_webcolor_names,
            llm_client=llm_client,
            cache=cache,
            debug=debug
        )
        simplified.append(simple)
        rgb_list.append(rgb)

    return simplified, rgb_list


def resolve_fallback_tokens(tokens, known_modifiers, known_tones, debug=False):
    """
    Fallback logic to recover missed tokens in compound extraction.
    Typically uses part-of-speech or suffix recovery logic.
    """
    resolved = set()
    for tok in tokens:
        raw = tok.text.lower()
        if raw in known_tones:
            resolved.add(raw)
            continue

        mod = resolve_modifier_token(raw, known_modifiers, known_tones)
        if mod:
            resolved.add(mod)
            if debug:
                print(f"[🧪 FALLBACK TOKEN] '{raw}' → '{mod}'")

    return resolved