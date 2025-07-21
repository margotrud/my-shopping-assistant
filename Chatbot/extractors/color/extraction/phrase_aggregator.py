#Chatbot/extractors/color/extraction/phrase_aggregator.py
"""
phrase_aggregator.py
====================

Extracts and aggregates descriptive color phrases from raw user input,
then maps them to RGB using known vocabularies and resolution pipelines.
"""
from typing import List, Set, Tuple, Dict

from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.extraction.compound import extract_compound_phrases
from Chatbot.extractors.color.extraction.standalone import extract_standalone_phrases, extract_lone_tones
from Chatbot.extractors.color.llm.simplifier import extract_suffix_fallbacks
from Chatbot.extractors.color.logic.color_pipeline import process_segment_colors

def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool = False
) -> List[str]:
    """
    Full pipeline to extract all valid descriptive color phrases from raw input.
    Combines compound, standalone, tone, and suffix fallback extraction.
    """
    import spacy
    nlp = spacy.load("en_core_web_sm")
    tokens = nlp(text)

    phrases = set()

    # Compound
    extract_compound_phrases(tokens, phrases, [], known_tones | known_modifiers | all_webcolor_names, known_modifiers, known_tones, all_webcolor_names, debug)

    # Standalone
    phrases.update(extract_standalone_phrases(tokens, known_modifiers, known_tones, debug))

    # Lone tones
    phrases.update(extract_lone_tones(tokens, known_tones, debug))

    # Suffix fallback
    phrases.update(extract_suffix_fallbacks(tokens, known_modifiers, known_tones, debug))

    return list(set(map(str.lower, phrases)))



def extract_phrases_from_segment(segment: str, debug: bool = False) -> List[str]:
    """
    Thin wrapper that injects globals into the phrase extraction pipeline.
    Used for segment-level color parsing.
    """
    known_modifiers = load_known_modifiers()
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones,
        known_modifiers,
        all_webcolor_names,
        debug
    )


def aggregate_color_phrase_results(
    segments: List[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    llm_client,
    cache=None,
    debug: bool = False
) -> Tuple[Set[str], List[str], Dict[str, Tuple[int, int, int]]]:
    """
    Aggregates color tone and RGB values from all segments.

    Returns:
    - set of matched tone names
    - list of simplified phrases
    - dict: phrase → RGB
    """
    tone_set = set()
    all_phrases = []
    rgb_map = {}

    for seg in segments:
        simplified, rgb_list = process_segment_colors(
            color_phrases=extract_phrases_from_segment(seg, debug),
            known_modifiers=known_modifiers,
            all_webcolor_names=all_webcolor_names,
            llm_client=llm_client,
            cache=cache,
            debug=debug
        )

        all_phrases.extend(simplified)
        for phrase, rgb in zip(simplified, rgb_list):
            if rgb:
                rgb_map[phrase] = rgb
                tone_set.add(phrase)

    return tone_set, all_phrases, rgb_map
