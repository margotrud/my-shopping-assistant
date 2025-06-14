#Chatbot/extractors/general/helpers.py
from typing import Dict, List, Set

from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.old.core import load_known_modifiers

from rapidfuzz import fuzz
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet

def are_antonyms(word1: str, word2: str) -> bool:
    """
       Determines whether two words are antonyms based on WordNet definitions.

       This function checks all synsets (word senses) of the first word,
       and inspects each lemma (canonical form) for listed antonyms.
       If the second word appears as an antonym of any lemma, it returns True.

       ⚠️ Note:
           - This function strictly uses the antonym relationships defined in NLTK's WordNet.
           - It does NOT infer antonyms using logic, embeddings, or semantic similarity.
           - Common-sense or intuitive opposites like ("create", "destroy") may return False
             if WordNet lacks an explicit antonym relation.

       Args:
           word1 (str): The first word to compare.
           word2 (str): The second word to check as a possible antonym of the first.

       Returns:
           bool: True if word2 is a WordNet-defined antonym of word1; otherwise False.
       """

    for syn in wordnet.synsets(word1):
        for lemma in syn.lemmas():
            for ant in lemma.antonyms():
                if ant.name().lower() == word2.lower():
                    return True
    return False

def split_glued_tokens(token: str, known_tokens: set[str]) -> list[str]:
    """
    Attempt to split a glued token into a sequence of known tone tokens,
    even if the full token itself is a known tone.

    Args:
        token (str): The glued token (e.g., "greige", "rosewood")
        known_tokens (set[str]): Set of known base tone tokens (e.g. {"grey", "beige"})

    Returns:
        list[str]: Sequence of known tokens if split found;
                   [token] if token is in known_tokens;
                   [] if nothing matched.
    """
    token = token.lower()
    n = len(token)
    results = []

    print(f"\n[🧪 DEBUG] Input token: '{token}'")
    print(f"[🔍] Known tokens include: {', '.join(sorted(list(known_tokens)[:10]))}...")

    def backtrack(start, path):
        if start == n:
            print(f"[✅] Complete split found: {path}")
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            piece = token[start:end]
            if piece in known_tokens:
                print(f"  [➡️] Match '{piece}' from {start}:{end}")
                path.append(piece)
                backtrack(end, path)
                path.pop()
            else:
                print(f"  [❌] Reject '{piece}' from {start}:{end}")

    backtrack(0, [])

    if results and len(results[0]) > 1:
        print(f"[🏁 RETURN] Split result: {results[0]}")
        return results[0]
    elif token in known_tokens:
        print(f"[🏁 RETURN] Fallback to full token: [{token}] (exists in known)")
        return [token]
    else:
        print(f"[🏁 RETURN] No valid split found. Returning []")
        return []


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
        return False

    # 5. Fuzzy match (only if both are single-word)
    if " " not in token and " " not in target:
        score = fuzz.ratio(token, target)
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


def get_glued_token_vocabulary() -> set[str]:
    """
    Returns the unified set of single-word color tokens for token splitting.
    Combines known tones and modifiers.
    """
    return {t for t in known_tones.union(load_known_modifiers()) if " " not in t}

