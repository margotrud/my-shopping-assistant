# Chatbot/extractors/color/extraction/standalone.py
"""
standalone.py
=============

Handles extraction of standalone tone/modifier terms,
including simplified and injected expressions.
"""
from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed
from Chatbot.extractors.color.shared.constants import COSMETIC_NOUNS
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token, match_expression_aliases


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

from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir

expression_map = load_json_from_data_dir("expression_definition.json")


import re
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases

expression_map = load_json_from_data_dir("expression_definition.json")


def normalize_expression_input(text: str) -> str:
    text = re.sub(r"\s*-\s*", "-", text.lower())
    return re.sub(r"\s+", " ", text).strip()

from nltk.corpus import wordnet
def _inject_expression_modifiers(tokens, known_modifiers, known_tones, expression_map, debug=False):
    def _synonym_candidates(word):
        syns = set()
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                lemma_name = lemma.name().replace("_", " ").lower()
                syns.add(lemma_name)
        return syns

    token_texts = [t.text for t in tokens]
    raw_text = normalize_expression_input(" ".join(token_texts))

    if debug:
        print("\n[🧪 TOKENS]")
        for idx, t in enumerate(tokens):
            print(f"  {idx:02d}: '{t.text}' (POS={t.pos_})")

        print(f"\n[🧼 RAW TEXT] → '{raw_text}'")
        print(f"[📚 EXPRESSION MAP SIZE] → {len(expression_map)}")

    matched_expressions = set()

    # ── Step 1: Forward match by alias or expression
    if debug:
        print("\n[🔍 DIRECT SPAN MATCHES]")
    for n in range(1, 4):
        for i in range(len(token_texts) - n + 1):
            span = " ".join(token_texts[i:i + n])
            norm_span = normalize_expression_input(span)
            matches = match_expression_aliases(norm_span, expression_map)

            if debug:
                print(f"  [SPAN] '{span}' → normalized: '{norm_span}'")
                if matches:
                    print(f"    ✅ Matched expressions: {matches}")
                else:
                    print("    ❌ No match")

            if matches:
                matched_expressions.update(matches)

    # ── Step 1B: Synonym fallback if no direct match
    if not matched_expressions:
        if debug:
            print("\n[🧠 SYNONYM FALLBACK]")
        for token in tokens:
            synonyms = _synonym_candidates(token.text)
            if debug:
                print(f"  [WORD] '{token.text}' → Synonyms: {sorted(synonyms)}")

            for syn in synonyms:
                norm_syn = normalize_expression_input(syn)
                matches = match_expression_aliases(norm_syn, expression_map)

                if matches:
                    matched_expressions.update(matches)
                    if debug:
                        print(f"    ✅ Matched via synonym '{syn}' → {matches}")

    # ── Step 2: Reverse modifier match (only if forward+synonym failed)
    if not matched_expressions:
        if debug:
            print("\n[🔁 REVERSE MODIFIER INJECTION]")
        for token in tokens:
            resolved = resolve_modifier_token(
                token.text,
                known_modifiers,
                known_tones,
                allow_fuzzy=True,
                is_tone=False
            )

            if resolved == token.text:
                if debug:
                    print(f"  ⛔ Skipping reverse match: '{token.text}' resolved to itself")
                continue

            if debug:
                print(f"  [TOKEN] '{token.text}' → Resolved: '{resolved}'")

            if resolved:
                for expr, conf in expression_map.items():
                    mod_set = conf.get("modifiers", [])
                    if resolved in mod_set:
                        matched_expressions.add(expr)
                        if debug:
                            print(f"    ✅ Modifier '{resolved}' found in expression '{expr}'")

    # ── Step 3: Inject modifiers from matched expressions
    injected_modifiers = set()
    if debug:
        print("\n[🧩 MODIFIER INJECTION]")
    for expr in matched_expressions:
        mod_candidates = expression_map.get(expr, {}).get("modifiers", [])
        if debug:
            print(f"  [EXPR] '{expr}' → Modifiers: {sorted(mod_candidates)}")

        for mod in mod_candidates:
            if mod in known_modifiers:
                injected_modifiers.add(mod)
                if debug:
                    print(f"    ✅ Injected modifier: '{mod}'")
            else:
                if debug:
                    print(f"    ⛔ Skipped unknown modifier: '{mod}'")

    if debug:
        print(f"\n[✅ FINAL INJECTED MODIFIERS] → {sorted(injected_modifiers)}\n")

    return injected_modifiers
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

        # ✅ First: try rule-based resolver
        resolved = resolve_modifier_token(raw, known_modifiers, known_tones)

        # 🔁 If nothing matched, fallback to LLM simplifier
        if not resolved:
            simplified = simplify_phrase_if_needed(raw, known_modifiers, known_tones)
            if simplified and simplified[0].strip():
                resolved_candidate = simplified[0].strip().split()[0]

                if resolved_candidate in known_modifiers or resolved_candidate in known_tones:
                    resolved = resolved_candidate
                    if debug:
                        print(f"[🔁 SIMPLIFIED FALLBACK] '{raw}' → '{resolved}'")

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
