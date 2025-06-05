"""
Color Phrase Extractor Module
-----------------------------
Extracts descriptive color phrases from user input text segments.

Public interface only:
- extract_all_descriptive_color_phrases()
- extract_phrases_from_segment()
"""

from typing import List, Set

from Chatbot.extractors.color import known_tones, all_webcolor_names
from Chatbot.extractors.color.modifier_resolution import resolve_modifier_with_suffix_fallback
from Chatbot.extractors.color.tokenizer_utils import tokenize_text
from Chatbot.extractors.color.compound_extraction import extract_compound_phrases
from Chatbot.extractors.color.standalone_extraction import extract_standalone_phrases, extract_lone_tones
from Chatbot.extractors.color.fallback_extraction import extract_suffix_fallbacks


def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],
    debug: bool = False
) -> List[str]:
    """
    Extracts descriptive color phrases from input text:
    - Compounds (e.g., "soft pink")
    - Standalone tones or modifiers (e.g., "pink")
    - Fallback suffix tones (e.g., "peachy")

    Args:
        text: User input.
        known_tones: Valid base color tones.
        known_modifiers: Valid modifiers.
        all_webcolor_names: Known CSS3/XKCD color names.
        debug: Enable debug print statements.

    Returns:
        List of extracted phrases (normalized, lowercase, sorted).
    """
    tokens, token_counts = tokenize_text(text)
    blocked_nouns = {"lipstick", "blush"}

    compounds, raw_compounds = extract_compound_phrases(
        tokens, known_tones, known_modifiers, all_webcolor_names, debug
    )
    singles = extract_standalone_phrases(
        tokens, token_counts, compounds, raw_compounds,
        known_tones, known_modifiers, all_webcolor_names, blocked_nouns, debug
    )
    lone_tones = extract_lone_tones(tokens, raw_compounds, known_tones, blocked_nouns, debug)
    suffix_tokens = extract_suffix_fallbacks(tokens, known_tones, known_modifiers, all_webcolor_names, debug)

    phrases = sorted(set(compounds) | set(singles) | set(lone_tones) | set(suffix_tokens))
    if debug:
        print(f"[✅ FINAL PHRASES] {phrases}")
    return phrases


def extract_phrases_from_segment(segment: str, known_modifiers: Set[str]) -> List[str]:
    """
    Wrapper to extract phrases using default tone/color vocabularies.

    Args:
        segment: User input.
        known_modifiers: Modifiers to apply (e.g., {"soft", "bold"}).

    Returns:
        List of extracted phrases.
    """
    return extract_all_descriptive_color_phrases(
        segment,
        known_tones=known_tones,
        known_modifiers=known_modifiers,
        all_webcolor_names=all_webcolor_names,
        debug=False
    )



# # Chatbot/extractors/color/phrase_extractor.py
#
# """
# Color Phrase Extractor Module
# -----------------------------
# Extracts descriptive color phrases from user input text segments.
#
# Features:
# - Identifies compound color phrases like 'soft pink'
# - Extracts standalone tones or modifiers like 'pink' or 'soft'
# - Handles plural forms and suffix-based fallback (e.g., 'peachy')
#
# Uses spaCy for syntactic parsing and token analysis,
# and relies on known vocabularies for tones, modifiers, and web color names.
# """
#
# # ─────────────────────────────────────────────────────────────
# # Imports and Globals
# # ─────────────────────────────────────────────────────────────
#
# import spacy
# from typing import List, Set, Tuple, Optional
# from collections import Counter
# from Chatbot.extractors.color import known_tones, all_webcolor_names
# from Chatbot.extractors.color.matcher import fuzzy_match_modifier, load_known_modifiers
# from Chatbot.extractors.general.helpers import split_glued_tokens
#
# nlp = spacy.load("en_core_web_sm")
# known_modifiers = load_known_modifiers()
#
# # ─────────────────────────────────────────────────────────────
# # Public Interface
# # ─────────────────────────────────────────────────────────────
#
# def _tokenize_and_prepare(text: str) -> Tuple[List[spacy.tokens.Token], Counter]:
#     doc = nlp(text.lower())
#     tokens = list(doc)
#     token_texts = [t.text for t in tokens]
#     return tokens, Counter(token_texts)
#
# def _extract_all_color_phrases(
#     tokens: List[spacy.tokens.Token],
#     token_counts: Counter,
#     known_tones: Set[str],
#     known_modifiers: Set[str],
#     all_webcolor_names: Set[str],
#     debug: bool
# ) -> Set[str]:
#     hardcoded_blocked_nouns = {"lipstick", "blush"}
#
#     compounds, raw_compounds = _extract_compounds(tokens, known_tones, known_modifiers, all_webcolor_names, debug)
#     singles = _extract_standalone_tokens(tokens, token_counts, compounds, raw_compounds, known_tones, known_modifiers, hardcoded_blocked_nouns, debug)
#     lone_tones = _extract_lone_tones(tokens, raw_compounds, known_tones, hardcoded_blocked_nouns, debug)
#     suffix_tokens = _extract_suffix_fallback_tokens(tokens, known_tones, known_modifiers, all_webcolor_names, debug)
#
#     return set(compounds) | set(singles) | set(lone_tones) | set(suffix_tokens)
#
# def _sort_and_debug_phrases(phrases: Set[str], debug: bool) -> List[str]:
#     sorted_list = sorted(phrases)
#     if debug:
#         print(f"Final extracted phrases: {sorted_list}")
#     return sorted_list
##
# # ─────────────────────────────────────────────────────────────
# # Compound Extraction Pipeline
# # ─────────────────────────────────────────────────────────────
# def _extract_compounds(
#     tokens: List[spacy.tokens.Token],
#     known_tones: Set[str],
#     known_modifiers: Set[str],
#     all_webcolor_names: Set[str],
#     debug: bool
# ) -> Tuple[Set[str], List[str]]:
#     compounds = set()
#     raw_compounds = []
#     known_color_tokens = known_modifiers | known_tones | all_webcolor_names
#     token_texts = [t.text.lower() for t in tokens]
#
#     _extract_from_adjacent_tokens(tokens, compounds, raw_compounds, known_tones, known_modifiers, all_webcolor_names, debug)
#     _extract_from_split_tokens(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)
#     _extract_from_glued_tokens(tokens, compounds, raw_compounds, token_texts, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug)
#
#     return compounds, raw_compounds
#
# # ─────────────────────────────────────────────────────────────
# # Compound Extraction: Strategies
# # ─────────────────────────────────────────────────────────────
# def _extract_from_adjacent_tokens(tokens, compounds, raw_compounds, known_tones, known_modifiers, all_webcolor_names, debug):
#     for i in range(len(tokens) - 1):
#         raw_t1, raw_t2 = get_adjacent_token_pair(tokens, i)
#         resolved = resolve_modifier_and_tone(raw_t1, raw_t2, known_modifiers, known_tones, all_webcolor_names)
#         if resolved:
#             mod, tone = resolved
#             register_compound_if_valid(mod, tone, raw_t1, known_tones, compounds, raw_compounds, debug)
#
#
#
# def _extract_from_split_tokens(tokens, compounds, raw_compounds, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug):
#     for i in range(len(tokens) - 1):
#         raw_t1 = tokens[i].text.lower()
#         raw_t2 = singularize(tokens[i + 1].text.lower())
#
#         t1_parts = split_glued_tokens(raw_t1, known_color_tokens)
#         t2_parts = split_glued_tokens(raw_t2, known_color_tokens)
#
#         for mod_candidate in t1_parts:
#             mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers)
#             for tone_candidate in t2_parts:
#                 is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names
#                 if mod and is_valid:
#                     if should_suppress_compound(mod_candidate, mod, tone_candidate, known_tones):
#                         if debug:
#                             print(f"[⛔ SUPPRESSED FALLBACK] {mod} {tone_candidate}")
#                         continue
#                     compound = f"{mod} {tone_candidate}"
#                     compounds.add(compound)
#                     raw_compounds.append(compound)
#                     if debug:
#                         print(f"[✅ COMPOUND DETECTED] → '{compound}'")
# def _extract_from_glued_tokens(tokens, compounds, raw_compounds, token_texts, known_color_tokens, known_modifiers, known_tones, all_webcolor_names, debug):
#     for token in tokens:
#         raw = singularize(token.text.lower())
#         if any(raw in c.replace(" ", "") for c in compounds):
#             if debug:
#                 print(f"[⛔ SKIPPED GLUED TOKEN] '{raw}' already present")
#             continue
#
#         parts = split_glued_tokens(raw, known_color_tokens)
#         if debug:
#             print(f"[🔬 SPLIT GLUED TOKEN] '{raw}' → {parts}")
#         if len(parts) != 2:
#             continue
#
#         mod_candidate, tone_candidate = parts
#         mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers, known_tones)
#         is_valid = tone_candidate in known_tones or tone_candidate in all_webcolor_names
#         original_form = mod_candidate + tone_candidate
#
#         if mod and is_valid and original_form in token_texts:
#             compound = f"{mod} {tone_candidate}"
#             compounds.add(compound)
#             raw_compounds.append(compound)
#             if debug:
#                 print(f"[✅ GLUED COMPOUND] '{raw}' → '{compound}'")
#         elif debug:
#             print(f"[⛔ REJECTED GLUED COMPOUND] '{raw}' not in original text or invalid tone")
#
# # ─────────────────────────────────────────────────────────────
# # Standalone & Fallback Extractors
# # ─────────────────────────────────────────────────────────────
# def _should_add_standalone_token(
#     token: spacy.tokens.Token,
#     token_counts: Counter,
#     compound_token_counts: Counter,
#     known_tones: Set[str],
#     known_modifiers: Set[str],
#     all_webcolor_names: Set[str],
#     hardcoded_blocked_nouns: Set[str],
#     debug: bool
# ) -> bool:
#     text = token.text.lower()
#     norm = singularize(text)
#     compound_uses = compound_token_counts[text]
#     total_uses = token_counts[text]
#
#     if debug:
#         print(f"\n[🔍 TOKEN CHECK] → '{text}' | POS={token.pos_} | norm={norm}")
#         print(f"    → in_known_modifiers: {text in known_modifiers}")
#         print(f"    → in_known_tones: {norm in known_tones}")
#         print(f"    → in_all_webcolor_names: {norm in all_webcolor_names}")
#         print(f"    → POS: {token.pos_}")
#         print(f"    → total uses: {total_uses} | in compounds: {compound_uses}")
#
#     if (text in known_modifiers or norm in known_tones) and norm not in hardcoded_blocked_nouns:
#         if norm in known_tones and token.pos_ == "NOUN" and norm not in all_webcolor_names:
#             if debug:
#                 print(f"[⛔ REJECTED] → '{text}' (noun, not in webcolors)")
#             return False
#
#         if total_uses > compound_uses:
#             if debug:
#                 print(f"[✅ ADDED SINGLE] → '{text}'")
#             return True
#         else:
#             if debug:
#                 print(f"[⛔ SKIPPED] → '{text}' only appears in compounds")
#
#     return False
#
#
# def _extract_suffix_fallback_tokens(
#     tokens: List[spacy.tokens.Token],
#     known_tones: Set[str],
#     known_modifiers: Set[str],
#     all_webcolor_names: Set[str],
#     debug: bool
# ) -> List[str]:
#     """
#     Extract tokens based on suffix fallbacks, e.g., adjectives
#     ending with 'ish' or 'y' that are tones or webcolors, excluding modifiers.
#
#     Args:
#         tokens: List of spaCy tokens.
#         known_tones: Valid base tones.
#         known_modifiers: Valid modifiers.
#         all_webcolor_names: Known CSS3 color names.
#         debug: Enable debug output.
#
#     Returns:
#         List of suffix-fallback tokens.
#     """
#     suffix_tokens = []
#
#     for t in tokens:
#         norm = singularize(t.text.lower())
#         if (
#             t.pos_ == "ADJ"
#             and norm.endswith(("ish", "y"))
#             and norm not in known_modifiers
#             and (norm in known_tones or norm in all_webcolor_names)
#         ):
#             suffix_tokens.append(norm)
#             if debug:
#                 print(f"Suffix fallback token added: {norm}")
#
#     return suffix_tokens
#
# # ─────────────────────────────────────────────────────────────
# # Helper Utilities
# # ─────────────────────────────────────────────────────────────
# def _override_with_suffix_if_tone(word: str, known_tones: Optional[Set[str]]) -> Optional[str]:
#     if known_tones and word.endswith("y"):
#         base = word[:-1]
#         if base in known_tones:
#             return base
#     return None
#
#
# def _block_double_use_as_modifier(word: str, known_tones: Optional[Set[str]]) -> bool:
#     if known_tones and word.endswith("y"):
#         base = word[:-1]
#         return base in known_tones
#     return False
#
#
# def _match_exact_modifier(word: str, known_modifiers: Set[str]) -> Optional[str]:
#     return word if word in known_modifiers else None
#
#
# def _match_suffix_heuristic(word: str, known_modifiers: Set[str]) -> Optional[str]:
#     for mod in known_modifiers:
#         if word.startswith(mod) and word.endswith(("ish", "y")) and len(word) <= len(mod) + 3:
#             return mod
#     return None
#
#
# def _match_fuzzy_modifier(word: str, known_modifiers: Set[str], threshold: int = 90) -> Optional[str]:
#     from rapidfuzz import process, fuzz
#     match = process.extractOne(word, known_modifiers, scorer=fuzz.ratio)
#     if match and match[1] >= threshold:
#         return match[0]
#     return None
#
# def resolve_modifier_with_suffix_fallback(
#     word: str,
#     known_modifiers: Set[str],
#     known_tones: Optional[Set[str]] = None,
#     allow_fuzzy: bool = True,
#     is_tone: bool = False
# ) -> Optional[str]:
#     """
#     Resolves a modifier or tone variant by applying:
#     - tone override via suffix
#     - exact match
#     - heuristic suffix rules
#     - fuzzy fallback
#     """
#
#     # Tone override from suffix
#     override = _override_with_suffix_if_tone(word, known_tones)
#     if override and not is_tone:
#         return override
#
#     # Prevent double-use as modifier if it's a known tone
#     if _block_double_use_as_modifier(word, known_tones):
#         return None
#
#     # Exact match
#     exact = _match_exact_modifier(word, known_modifiers)
#     if exact:
#         return exact
#
#     # Heuristic suffix match
#     heuristic = _match_suffix_heuristic(word, known_modifiers)
#     if heuristic:
#         return heuristic
#
#     # Fuzzy (only if allowed and not tone-restricted)
#     if allow_fuzzy or not is_tone:
#         return _match_fuzzy_modifier(word, known_modifiers)
#
#     return None
#
#
# def should_suppress_compound(
#     raw_modifier: str,
#     resolved_modifier: Optional[str],
#     resolved_tone: Optional[str],
#     known_tones: Set[str]
# ) -> bool:
#     """
#     Decide whether to suppress a compound due to tone promotion.
#
#     Args:
#         raw_modifier: Original raw modifier token (e.g., 'peachy')
#         resolved_modifier: The resolved modifier (e.g., 'peach')
#         resolved_tone: The tone resolved from the second token
#         known_tones: All known tones
#
#     Returns:
#         bool: True if this compound should be skipped.
#     """
#     # If the raw modifier ended in 'y', got demoted to its base tone (e.g., peachy → peach)
#     # and the resolved tone is None or unknown → suppress this compound
#     if (
#         raw_modifier.endswith("y")
#         and resolved_modifier in known_tones
#         and resolved_tone is None
#     ):
#         return True
#     return False
#
# # ─────────────────────────────────────────────────────────────
# # Micro Helpers for Clean Pipelines
# # ─────────────────────────────────────────────────────────────
#
# def get_adjacent_token_pair(tokens, i) -> Tuple[str, str]:
#     t1 = tokens[i].text.lower()
#     t2 = singularize(tokens[i + 1].text.lower())
#     return t1, t2
# def resolve_modifier_and_tone(raw_t1, raw_t2, known_modifiers, known_tones, all_webcolor_names) -> Optional[Tuple[str, str]]:
#     mod = resolve_modifier_with_suffix_fallback(raw_t1, known_modifiers)
#     tone = resolve_modifier_with_suffix_fallback(raw_t2, known_modifiers, known_tones, allow_fuzzy=False, is_tone=True)
#     if mod and tone and (tone in known_tones or tone in all_webcolor_names):
#         return mod, tone
#     return None
# def register_compound_if_valid(mod, tone, raw_t1, known_tones, compounds, raw_compounds, debug):
#     if should_suppress_compound(raw_t1, mod, tone, known_tones):
#         if debug:
#             print(f"[⛔ SUPPRESSED] {mod} {tone}")
#         return
#     compound = f"{mod} {tone}"
#     compounds.add(compound)
#     raw_compounds.append(compound)
#     if debug:
#         print(f"[✅ WHOLE TOKEN COMPOUND DETECTED] → '{compound}'")
#
#
# def get_split_token_pair(tokens, i, known_color_tokens) -> Tuple[List[str], List[str]]:
#     raw_t1 = tokens[i].text.lower()
#     raw_t2 = singularize(tokens[i + 1].text.lower())
#     return split_glued_tokens(raw_t1, known_color_tokens), split_glued_tokens(raw_t2, known_color_tokens)
#
# def resolve_and_validate_split_combination(
#     mod_candidate: str,
#     tone_candidate: str,
#     known_modifiers: Set[str],
#     known_tones: Set[str],
#     all_webcolor_names: Set[str]
# ) -> Optional[Tuple[str, str]]:
#     mod = resolve_modifier_with_suffix_fallback(mod_candidate, known_modifiers)
#     if mod and (tone_candidate in known_tones or tone_candidate in all_webcolor_names):
#         return mod, tone_candidate
#     return None
#
# def register_fallback_compound_if_valid(
#     mod: str,
#     tone: str,
#     mod_candidate: str,
#     known_tones: Set[str],
#     compounds: Set[str],
#     raw_compounds: List[str],
#     debug: bool
# ):
#     if should_suppress_compound(mod_candidate, mod, tone, known_tones):
#         if debug:
#             print(f"[⛔ SUPPRESSED FALLBACK] {mod} {tone}")
#         return
#     compound = f"{mod} {tone}"
#     compounds.add(compound)
#     raw_compounds.append(compound)
#     if debug:
#         print(f"[✅ COMPOUND DETECTED] → '{compound}'")
#
#
#
#
#
#
#
#
#
#
#
