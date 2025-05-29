#Chatbot/scripts/helpers.py
from typing import Dict, List, Set

from rapidfuzz import fuzz
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet

def are_antonyms(word1: str, word2: str) -> bool:
    for syn in wordnet.synsets(word1):
        for lemma in syn.lemmas():
            for ant in lemma.antonyms():
                if ant.name().lower() == word2.lower():
                    return True
    return False

def split_glued_tokens(token: str, known_tokens: set[str]) -> list[str]:
    """
    Attempt to split a glued token into a sequence of known tone tokens.
    For example, "greige" → ["grey", "beige"] if both are in known_tones.

    Args:
        token (str): The glued token (e.g. "greige", "rosewood")
        known_tokens (set[str]): Set of known base tone tokens (e.g. {"grey", "beige"})

    Returns:
        list[str]: Sequence of known tokens if split found, else []
    """
    token = token.lower()
    n = len(token)
    results = []

    def backtrack(start, path):
        if start == n:
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            piece = token[start:end]
            if piece in known_tokens:
                path.append(piece)
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    # Return first valid split (greedy match)
    return results[0] if results else []


BLOCKED_TOKENS = {
    ("light", "night"),
    ("romantic", "dramatic")
}

def fuzzy_token_match(token: str, target: str, threshold: int = 75) -> bool:
    """
    Secure fuzzy matcher with:
    - Semantic blocklist
    - Exact match
    - Safe prefix (only when both are 1-word)
    - Full fuzzy match (only when both are 1-word)
    - Multi-word triggers require all words to be in token
    """
    print(f"[🧪 FUZZY CHECK] token='{token}' vs target='{target}'")

    token = token.lower()
    target = target.lower()
    pair = (token, target)
    reversed_pair = (target, token)

    # 1. Blocklist check
    if pair in BLOCKED_TOKENS or reversed_pair in BLOCKED_TOKENS:
        print("   ⛔ BLOCKED (explicit)")
        return False

    # 2. Exact match
    if token == target:
        print("   ✅ EXACT")
        return True

    # 3. Safe prefix match: only allow if both are single words
    if " " not in token and " " not in target and target.startswith(token):
        print("   ✅ SAFE PREFIX")
        return True

    # 4. Multi-word match: require full phrase match
    if " " in target:
        parts = target.split()
        if all(part in token for part in parts):
            print("   ✅ FULL MULTI-WORD MATCH")
            return True
        print("   🚫 SKIPPED (multi-word not fully matched)")
        return False

    # 5. Fuzzy match (only if both are single-word)
    if " " not in token and " " not in target:
        score = fuzz.ratio(token, target)
        print(f"   🤏 FUZZY SCORE = {score}")
        return score >= threshold

    print("   🚫 SKIPPED (fallback)")
    return False


def get_all_trigger_tokens(trigger_map: Dict[str, List[str]]) -> Set[str]:
    """
    Extract individual lowercase tokens from all trigger phrases.
    Used to dynamically allow fuzzy matches (even verbs like 'glow').

    Args:
        trigger_map (Dict[str, List[str]]): Expression → phrases

    Returns:
        Set[str]: All unique lowercase words from trigger phrases
    """
    tokens = set()
    for phrases in trigger_map.values():
        for phrase in phrases:
            tokens.update(phrase.lower().split())
    return tokens
