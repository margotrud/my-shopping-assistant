# Chatbot/extractors/color/utils/token_utils.py

"""
token_utils.py
==============

Token-level normalization and recovery utilities.

Used By:
--------
- Compound extraction
- Glued token recovery
- Plural normalization of cosmetic nouns
"""
from typing import Set, List, Optional



def split_glued_tokens(
    token: str,
    known_tokens: Set[str],
    known_modifiers: Set[str],
    debug: bool = True
) -> List[str]:
    """
    Attempts to split a glued token (e.g. 'earthyrose') into known tokens/modifiers,
    respecting suffix variants and returning raw leftover prefix/suffix if needed.

    Args:
        token (str): The glued input string.
        known_tokens (Set[str]): Known tones and modifiers.
        known_modifiers (Set[str]): Base modifiers for suffix derivations.
        debug (bool): Whether to print debug information.

    Returns:
        List[str]: List of recognized token parts from the input.
    """

    token = normalize_token(token)


    # Combine bases for suffix generation
    bases_for_suffix = known_modifiers.union(known_tokens)

    augmented_vocab = set(known_tokens).union(known_modifiers)
    for mod in bases_for_suffix:
        if len(mod) >= 3:
            augmented_vocab.add(mod + "y")
            if not mod.endswith("e"):
                augmented_vocab.add(mod + "ed")
            if mod.endswith("e"):
                base = mod[:-1]
                augmented_vocab.add(base + "y")
                augmented_vocab.add(base + "ed")

    if debug:
        print(f"\n🔍 Starting split for: '{token}'")
        print(f"📦 Augmented vocab size: {len(augmented_vocab)}")

    def is_valid_token(t: str) -> bool:
        if t in augmented_vocab:
            return True
        if t.endswith("y") and t[:-1] in known_modifiers:
            return True
        if t.endswith("ed") and t[:-2] in known_modifiers:
            return True
        return False

    def recursive_split(t: str) -> Optional[List[str]]:
        if is_valid_token(t):
            if debug:
                print(f"✅ Recognized token: '{t}'")
            return [t]

        for i in range(3, len(t) - 2):
            left, right = t[:i], t[i:]
            if debug:
                print(f"↪️ Trying recursive split: '{left}' + '{right}'")

            left_split = recursive_split(left)
            right_split = recursive_split(right)

            if left_split is not None and right_split is not None:
                if debug:
                    print(f"✅ Recursive split success: {left_split + right_split}")
                return left_split + right_split

        if debug:
            print(f"❌ No recursive split found for: '{t}'")
        return None

    # First try recursive splitting
    parts = recursive_split(token)
    if parts:
        if debug:
            print(f"✅ Final recursive parts: {parts}")
        parts = [normalize_token(p) for p in parts]
        return parts

    # Improved fallback: find the longest known token anywhere in the glued token
    sorted_vocab = sorted(augmented_vocab, key=len, reverse=True)
    longest_word = ""
    longest_idx = -1
    for known_word in sorted_vocab:
        idx = token.find(known_word)
        if idx != -1 and len(known_word) > len(longest_word):
            longest_word = known_word
            longest_idx = idx

    if longest_word:
        prefix = token[:longest_idx]
        suffix = token[longest_idx + len(longest_word):]

        parts = []
        if prefix:
            parts.append(prefix)  # raw prefix, no recursion
        parts.append(longest_word)
        if suffix:
            parts.append(suffix)  # raw suffix, no recursion

        if debug:
            print(f"🪄 Fallback split at '{longest_word}': {parts}")

        return parts

    if debug:
        print(f"❌ Unable to split token: '{token}'")
    return []

def singularize(word: str) -> str:
    """
    Converts plural cosmetic nouns to singular form using simple heuristics.
    """
    word = word.lower()  # just lowercase, no normalize_token here
    if word.endswith("es") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word

def normalize_token(token: str) -> str:
    """
    Normalizes a token for comparison and matching.

    - Lowercases
    - Strips whitespace
    - Removes all hyphens (not just trailing)
    - Singularizes cosmetic plurals
    """
    token = token.lower().replace("-", "").strip()
    token = singularize(token)
    return token

