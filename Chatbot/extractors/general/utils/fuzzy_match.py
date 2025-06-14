#Chatbot/extractors/general/utils/fuzzy_match.py
"""
fuzzy_match.py
==============
Generic fuzzy token matcher with blocklist, prefix, and multi-word logic.

Designed for reuse across multiple domains (e.g., colors, brands, products).
Wraps common secure fuzzy matching behaviors into a single configurable function.

Features:
---------
- Exact match
- Safe prefix match (single-word only)
- Multi-word trigger matching
- Fuzzy string ratio fallback
- Optional semantic blocklist filtering
"""

from typing import Set, Tuple, Optional, Dict
from rapidfuzz import fuzz
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
import spacy
# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

def normalize_token(token: str) -> str:
    original = token
    token = token.lower().strip()

    # 1. Manual suffix strip
    for suffix in ["ness"]:
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            stripped = token[:-len(suffix)]
            print(f"   🔁 Stripped suffix '{suffix}': '{original}' → '{stripped}'")
            return stripped

    # 2. WordNet
    lemma_adj = wnl.lemmatize(token, pos='a')
    if lemma_adj != token:
        print(f"   ✅ WordNet(ADJ): '{original}' → '{lemma_adj}'")
        return lemma_adj

    lemma_noun = wnl.lemmatize(token, pos='n')
    if lemma_noun != token:
        print(f"   ✅ WordNet(NOUN): '{original}' → '{lemma_noun}'")
        return lemma_noun

    # 3. spaCy — only for single words
    if " " not in token:
        doc = nlp(token)
        if doc and doc[0].lemma_ != token:
            lemma_spacy = doc[0].lemma_.lower()
            print(f"   ✅ spaCy lemma: '{original}' → '{lemma_spacy}'")
            return lemma_spacy

    print(f"   ❌ No normalization match: keeping '{original}'")
    return token


def fuzzy_token_match(
        token: str,
        target: str,
        *,
        blocklist: Optional[Set[Tuple[str, str]]] = None,
        threshold: int = 75,
        allow_prefix: bool = True,
        allow_multiword: bool = True
) -> bool:
    print(f"\n[🧪 FUZZY CHECK] token='{token}' target='{target}' threshold={threshold}")
    print(f"[🔧 NORMALIZED INPUTS] token='{token}', target='{target}'")

    # 1. Normalize inputs
    token = normalize_token(token)
    target = normalize_token(target)

    pair = (token, target)
    reverse = (target, token)

    # 2. Blocklist check
    if blocklist and (pair in blocklist or reverse in blocklist):
        print("   ⛔ BLOCKED (blocklist)")
        return False

    # 3. Exact match
    if token == target:
        print("   ✅ EXACT MATCH")
        return True

    # 4. Prefix match (single-word only)
    if allow_prefix and " " not in token and " " not in target:
        if target.startswith(token):
            print("   ✅ PREFIX MATCH")
            return True

    # 5. Multi-word logic
    if " " in target:
        if allow_multiword:
            if token == target:
                print("   ✅ EXACT MULTI-WORD")
                return True

            token_parts = token.split()
            target_parts = target.split()

            if len(token_parts) != len(target_parts):
                print("   🚫 MISMATCH LENGTH (multi-word)")
                return False

            for t_tok, t_tgt in zip(token_parts, target_parts):
                score = fuzz.ratio(t_tok, t_tgt)
                print(f"   🤏 PARTWISE FUZZY: '{t_tok}' vs '{t_tgt}' → {score}")
                if score < threshold:
                    print("   🚫 PARTWISE FAIL")
                    return False
            print("   ✅ PARTWISE FUZZY MATCH")
            return True
        else:
            print("   🚫 MULTI-WORD MATCH DISALLOWED")
            return False

    # 6. Fuzzy match fallback (only if both are single-word)
    if " " not in token and " " not in target:
        score = fuzz.ratio(token, target)
        print(f"   🤏 SINGLE WORD FUZZY: '{token}' vs '{target}' → {score}")
        return score >= threshold

    # 7. No other logic path
    print("   🚫 FALLBACK CASE — no match strategy applicable")
    return False

def match_expression_aliases(
    text: str,
    expression_definition: Dict[str, Dict[str, list]],
    threshold: int = 85
) -> Set[str]:
    """
    Matches user input against expression aliases using fuzzy and exact matching.

    Args:
        text (str): Raw user input (e.g., "I'm going for a soft glam wedding look").
        expression_definition (Dict): Expression config with 'aliases' per expression.
        threshold (int): Minimum fuzzy match score to consider a match.

    Returns:
        Set[str]: Set of matched expression names (e.g., {"soft glam", "romantic"})
    """
    matches = set()
    lowered = text.lower()

    for expression, definition in expression_definition.items():
        aliases = definition.get("aliases", [])
        for alias in aliases:
            alias = alias.lower()
            if alias in lowered:
                matches.add(expression)
                break
            elif fuzz.partial_ratio(alias, lowered) >= threshold:
                matches.add(expression)
                break

    return matches

