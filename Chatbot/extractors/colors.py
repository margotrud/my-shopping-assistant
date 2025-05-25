from collections import defaultdict
import spacy
from typing import List, Set, Dict
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
import os
import json
import webcolors
all_webcolor_names = set(webcolors.CSS3_NAMES_TO_HEX.keys())

# Dynamically locate the known_modifiers.json regardless of where the script is run
this_dir = os.path.dirname(os.path.abspath(__file__))  # path to colors.py
data_path = os.path.abspath(os.path.join(this_dir, "..", "..", "Data", "known_modifiers.json"))

with open(data_path, "r", encoding="utf-8") as f:
    known_modifiers = set(json.load(f))

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
all_webcolor_names = set(name.lower() for name in webcolors.CSS3_NAMES_TO_HEX)


###################### I. Extract colors : Test checked and rewritten
def extract_all_descriptive_color_phrases(
    text: str,
    known_tones: Set[str],
    known_modifiers: Set[str],
    all_webcolor_names: Set[str],

        debug: bool = False,
) -> List[str]:
    """
    Extracts descriptive color phrases with detailed code-level debugging.
    """
    from collections import Counter

    def singularize(word: str) -> str:
        return word[:-1] if word.endswith("s") and not word.endswith("ss") else word

    doc = nlp(text.lower())
    tokens = list(doc)
    token_texts = [t.text for t in tokens]
    token_counts = Counter(token_texts)

    # 🚫 Only allowed hardcoded block (lipstick exists in webcolors but is not a tone)
    hardcoded_blocked_nouns = {"lipstick"}

    if debug:
        print(f"\n[DEBUG] Raw input: '{text}'")
        print(f"[DEBUG] Token list:")
        for i, t in enumerate(tokens):
            print(f"  - Index {i:02d} → '{t.text}' | POS={t.pos_} | DEP={t.dep_} | HEAD={t.head.text}")

    compounds = set()
    raw_compound_phrases = []  # used for accurate token counting
    singles = []

    for i in range(len(tokens) - 1):
        t1, t2 = tokens[i], tokens[i + 1]

        t1_is_valid = t1.text in known_modifiers
        t2_is_valid = singularize(t2.text) in known_tones

        if debug:
            print(f"\n[DEBUG] Checking pair: '{t1.text}' + '{t2.text}'")
            print(
                f"  → t1 = {t1.text}, is_modifier = {t1_is_valid}, is_tone/webcolor = {t1.text in known_tones or t1.text in all_webcolor_names}")
            print(
                f"  → t2 = {t2.text}, is_tone = {t2.text in known_tones}, is_webcolor = {t2.text in all_webcolor_names}, POS = {t2.pos_}")

        if not (t1_is_valid and t2_is_valid):
            if debug:
                print(f"[DEBUG] ❌ Skipping pair '{t1.text} {t2.text}' — t1_valid={t1_is_valid}, t2_valid={t2_is_valid}")
            continue

        t2_norm = singularize(t2.text).lower()

        if (
                t2.pos_ == "NOUN"
                and t2_norm not in known_tones
                and t2_norm not in all_webcolor_names
        ) or t2_norm in hardcoded_blocked_nouns:
            if debug:
                print(f"[DEBUG] 🚫 Rejected compound: '{t1.text} {t2.text}' — NOUN not in tone or webcolors")
            singles.append(t1.text)
            continue

        t1_is_tone = singularize(t1.text) in known_tones or t1.text in all_webcolor_names
        t2_is_tone = singularize(t2.text) in known_tones or t2.text in all_webcolor_names

        compound = f"{t1.text} {t2.text}"
        if t1_is_tone and t2_is_tone:
            compounds.add(compound)
            raw_compound_phrases.append(compound)
            if debug:
                print(f"[DEBUG] ✅ Added tone-tone compound: '{compound}'")

        compounds.add(compound)
        raw_compound_phrases.append(compound)
        if debug:
            print(f"[DEBUG] ✅ Added compound: '{compound}'")

    # Dedup compound list for later filtering
    compounds = set(compounds)
    if debug:
        print(f"[DEBUG] Unique compound phrases: {sorted(compounds)}")

    # Build token usage count from raw compound occurrences (not deduped)
    compound_token_counts = Counter(tok for comp in raw_compound_phrases for tok in comp.split())
    if debug:
        print(f"[DEBUG] Compound token usage count: {dict(compound_token_counts)}")

    # Build map from token → all compounds it's used in
    compound_token_to_phrases = {}
    for comp in compounds:
        for tok in comp.split():
            compound_token_to_phrases.setdefault(tok, set()).add(comp)
    if debug:
        print(f"[DEBUG] Token → Compound Map:")
        for token, phrases in compound_token_to_phrases.items():
            print(f"    - '{token}': {sorted(phrases)}")

    # Collect standalone tone/modifier tokens if not only used in compounds
    for i, t in enumerate(tokens):
        token_text = t.text
        normalized = singularize(token_text)

        if (token_text in known_modifiers or normalized in known_tones) and normalized not in hardcoded_blocked_nouns:
            total_occurrences = token_counts[token_text]
            compound_occurrences = compound_token_counts[token_text]

            if debug:
                print(f"[DEBUG] Token '{token_text}' appears {total_occurrences}x total, {compound_occurrences}x in compounds")

            if total_occurrences > compound_occurrences:
                singles.append(token_text)
                if debug:
                    print(f"[DEBUG] 🧷 Collected single: '{token_text}' (index {i}) — outside compound")
            else:
                if debug:
                    print(f"[DEBUG] ⛔ Skipped single '{token_text}' — only appears in compounds")

    # Filter singles
    filtered_singles = []
    for word in singles:
        count = token_counts[word]
        compound_uses = compound_token_to_phrases.get(word, set())
        compound_only_count = compound_token_counts.get(word, 0)

        if debug:
            print(f"\n[DEBUG] 🔍 Reviewing single: '{word}' — Occurs {count} time(s)")
            print(f"[DEBUG] Token '{word}' is used in {len(compound_uses)} unique compounds: {compound_uses}")

        # Suppress if word is used only in one compound and nowhere else
        if count == compound_only_count and len(compound_uses) == 1:
            if debug:
                print(f"[DEBUG] ❌ Skipped '{word}' — only appears in one compound")
            continue

        if count > 1:
            filtered_singles.append(word)
            if debug:
                print(f"[DEBUG] ✅ Kept: '{word}' — Appears multiple times")
            continue

        index = next((i for i, t in enumerate(tokens) if t.text == word), None)
        if index is None:
            if debug:
                print(f"[DEBUG] ⚠️ Could not locate '{word}' in tokens")
            continue

        prev = tokens[index - 1] if index > 0 else None
        next_ = tokens[index + 1] if index + 1 < len(tokens) else None
        prev_is_adj = prev and prev.pos_ == "ADJ"
        next_is_adj = next_ and next_.pos_ == "ADJ"

        if debug:
            print(f"[DEBUG] Neighbors for '{word}' → prev='{prev.text if prev else '∅'}', next='{next_.text if next_ else '∅'}'")
            print(f"[DEBUG] → prev_is_adj={prev_is_adj}, next_is_adj={next_is_adj}")

        if next_ and next_.pos_ == "NOUN":
            filtered_singles.append(word)
            if debug:
                print(f"[DEBUG] ✅ Kept: '{word}' — Followed by NOUN")
            continue

        if prev_is_adj or next_is_adj:
            if debug:
                print(f"[DEBUG] ❌ Rejected: '{word}' — Adjacent to another ADJ and not followed by NOUN")
            continue

        filtered_singles.append(word)
        if debug:
            print(f"[DEBUG] ✅ Kept strict single: '{word}' — Unique and not adjacent to ADJ")

    # Final filtering — reject compound/single phrases with invalid NOUN
    candidates = sorted(compounds.union(filtered_singles))
    final = []

    for phrase in candidates:
        parts = phrase.split()
        phrase_contains_noun = any(
            any(
                tok.text == part and
                tok.pos_ == "NOUN" and
                singularize(part) not in known_modifiers and
                singularize(part) not in known_tones
                for tok in tokens
            )
            for part in parts
        )
        if phrase_contains_noun:
            if debug:
                print(f"[DEBUG] 🚫 Removed '{phrase}' — Contains NOUN not in vocab")
            continue

        final.append(phrase)
        if debug:
            print(f"[DEBUG] ✅ Final accepted phrase: '{phrase}'")

    if debug:
        print(f"\n[DEBUG] ✨ Final result (before dedup): {final}")
    final = list(dict.fromkeys(final))
    if debug:
        print(f"[DEBUG] ✨ Deduplicated final result: {final}")

    return final



###################### II. Extract modifiers and tones : Test checked and rewritten
def categorize_color_tokens_with_mapping(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Dict[str, object]:
    """
    Analyzes a list of descriptive color phrases to identify tones and modifiers,
    and builds bidirectional mappings between them.

    Args:
        phrases: List of phrases (e.g., ['soft beige', 'bold red'])
        known_tones: Set of known base tones (e.g., {'beige', 'red'})
        known_modifiers: Set of known modifiers (e.g., {'soft', 'bold'})

    Returns:
        {
            "tones": List[str],
            "modifiers": List[str],
            "modifier_to_tone": Dict[str, List[str]],
            "tone_to_modifier": Dict[str, List[str]]
        }
    """
    tones = set()
    modifiers = set()
    modifier_to_tone = defaultdict(set)
    tone_to_modifier = defaultdict(set)

    for phrase in phrases:
        tokens = phrase.lower().split()
        matched_tones = [tok for tok in tokens if tok in known_tones]
        matched_modifiers = [tok for tok in tokens if tok in known_modifiers]

        tones.update(matched_tones)
        modifiers.update(matched_modifiers)

        for mod in matched_modifiers:
            for tone in matched_tones:
                modifier_to_tone[mod].add(tone)
                tone_to_modifier[tone].add(mod)

    return {
        "tones": sorted(tones),
        "modifiers": sorted(modifiers),
        "modifier_to_tone": {mod: sorted(tones) for mod, tones in modifier_to_tone.items()},
        "tone_to_modifier": {tone: sorted(mods) for tone, mods in tone_to_modifier.items()}
    }

###################### III. LLM Color Simplification: Test checked and rewritten

def simplify_color_description_with_llm(color_phrase: str) -> list[str]:
    """
    Uses an LLM via OpenRouter to simplify a descriptive color name (e.g. 'cherry')
    into a clean [modifier + tone] format (e.g. ['bright red']).

    Args:
        color_phrase (str): A non-standard color term (e.g. 'cherry')

    Returns:
        list[str]: A single-item list like ['bright red']
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env")

    prompt = (
        f"You are a beauty product color simplifier.\n"
        f"Your task is to determine if the word '{color_phrase}' refers to an actual color or shade used in makeup, cosmetics, or fashion.\n"
        f"If it **clearly refers to a color**, return a simplified version using a tone and optional modifier (e.g., 'soft pink', 'deep coral').\n"
        f"If it **is not a color** (e.g., 'elegant', 'flawless', 'luxurious', 'matte', 'shiny', 'clean'), return an empty string.\n"
        f"⚠️ Do NOT try to guess or interpret the word metaphorically. Do NOT return something close — only return color terms.\n"
        f"\nExamples:\n"
        f" - 'elegant' → ''\n"
        f" - 'success' → ''\n"
        f" - 'peachy' → 'light peach'\n"
        f" - 'blush' → 'soft pink'\n"
        f"\nReturn only the result. No explanations. No punctuation. No formatting."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 15,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error {response.status_code}: {response.text}")

    raw_output = response.json()["choices"][0]["message"]["content"].strip().lower()
    if raw_output == "":
        return []

    tokens = raw_output.split()

    from matplotlib.colors import XKCD_COLORS

    css_tones = set(map(str.lower, webcolors.CSS3_NAMES_TO_HEX.keys()))
    xkcd_tones = set(name.replace("xkcd:", "").lower() for name in XKCD_COLORS)
    tone_keywords = css_tones.union(xkcd_tones)

    def is_valid_tone(tone: str) -> bool:
        return tone in tone_keywords or tone.endswith(("ish", "y")) or len(tone) <= 10

    for i in range(len(tokens) - 1):
        mod, tone = tokens[i], tokens[i + 1]
        print(f"[DEBUG] Checking pair: {mod=} {tone=}")
        if mod in known_modifiers and is_valid_tone(tone):
            print(f"[DEBUG] ✅ Accepted simplified pair: {mod} {tone}")
            return [f"{mod} {tone}"]

    # Fallback: return first tone only if no modifier found
    for tok in tokens:
        if tok in tone_keywords:
            return [tok]

    return []  # Nothing matched


from rapidfuzz import process, fuzz

def fuzzy_match_modifier(
    modifier: str,
    known_modifiers: set[str],
    threshold: int = 80
) -> str | None:
    """
    Fuzzy match a modifier string to a known modifier vocabulary.

    Args:
        modifier (str): Input string (e.g. 'brigt')
        known_modifiers (set[str]): Known trusted modifiers
        threshold (int): Minimum similarity score (0-100)

    Returns:
        str or None: Closest matching known modifier or None if not found
    """
    if not modifier:
        return None

    match = process.extractOne(modifier.lower(), known_modifiers, scorer=fuzz.ratio)

    if match and match[1] >= threshold:
        return match[0]
    return None
