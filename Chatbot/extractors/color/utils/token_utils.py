# Chatbot/extractors/color/utils/token_utils.py
"""
token_utils.py
==============
Token-level text utilities used throughout the color extraction pipeline.

This module provides low-level, language-agnostic functions that manipulate
and analyze individual tokens — especially useful for cosmetic and fashion-related
text parsing where user inputs often include creative or informal structures.

Key Features:
-------------
- Glued token decomposition: Handles cases like "deepblue" → ["deep", "blue"]
- Designed for integration into higher-level phrase extraction modules
- Lightweight and fully standalone — no dependencies beyond the standard library

Why This Module Exists:
-----------------------
In user-generated input, it's common to encounter color descriptions without
spaces or in non-standard formats (e.g., "lightpeach", "softpink", "rosybrown").
These are not picked up by standard NLP tokenizers. This utility enables
recognizing and extracting valid color components from such inputs.

Example Use Cases:
------------------
Used by:
- compound phrase extractor to parse adjacent or glued modifiers + tones
- fallback extractors to recognize embedded tokens in unknown compounds

Example:
--------
>>> known = {"soft", "pink", "light", "blue", "nude"}
>>> split_glued_tokens("lightblue", known)
['light', 'blue']

>>> split_glued_tokens("softpink", known)
['soft', 'pink']

>>> split_glued_tokens("nude", known)
['nude']

>>> split_glued_tokens("shinyglam", known)
[]
"""
from typing import Set, Optional, Callable, List


def split_glued_tokens(
    token: str,
    known_tokens: Set[str],
    fallback_token_resolver: Optional[Callable[[str], Optional[str]]] = None,
    debug: bool = False
) -> List[str]:
    """
    Splits a glued token into known sub-tokens using backtracking,
    preferring the longest valid decomposition. If no valid split is found,
    optionally applies a fallback resolver, and finally applies substring-based
    longest-known-token decomposition.

    Args:
        token (str): The glued token (e.g., 'deepblue', 'cooltone')
        known_tokens (Set[str]): Set of known base or compound tokens
        fallback_token_resolver (Callable[[str], Optional[str]], optional):
            Function to resolve unknown suffixes (e.g., known tone matcher)
        debug (bool): If True, prints detailed debug information

    Returns:
        List[str]: List of split tokens if found, otherwise [].
    """
    token = token.lower()
    n = len(token)
    results = []

    if debug:
        print(f"\n[🔍 GLUED TOKEN SPLIT] Input: '{token}'")
        print(f"[📚 KNOWN TOKENS SAMPLE] → {sorted(list(known_tokens))[:10]} ...")

    def backtrack(start: int, path: List[str]):
        if start == n:
            if debug:
                print(f"   ✅ COMPLETE SPLIT → {path}")
            results.append(path[:])
            return
        for end in range(start + 1, n + 1):
            piece = token[start:end]
            if piece in known_tokens:
                if debug:
                    print(f"   🔹 MATCHED: '{piece}' at [{start}:{end}] → path so far = {path + [piece]}")
                path.append(piece)
                backtrack(end, path)
                path.pop()
            else:
                if debug:
                    print(f"   ⛔ REJECTED: '{piece}' at [{start}:{end}]")

    backtrack(0, [])

    if results:
        best = max(results, key=len)
        if debug:
            print(f"[🏁 FINAL CHOICE] Longest valid split → {best}")
        return best

    # 🔁 Fallback: try prefix + resolvable suffix
    if fallback_token_resolver:
        if debug:
            print("[🛟 FALLBACK MODE] No valid full split found, trying prefix + suffix resolution...")
        for i in range(1, len(token)):
            prefix, suffix = token[:i], token[i:]
            if prefix in known_tokens:
                resolved_suffix = fallback_token_resolver(suffix)
                if resolved_suffix:
                    if debug:
                        print(f"   ✅ FALLBACK SPLIT → prefix: '{prefix}' + resolved suffix: '{resolved_suffix}'")
                    return [prefix, resolved_suffix]
                else:
                    if debug:
                        print(f"   ⛔ Fallback failed: '{suffix}' not resolvable after prefix '{prefix}'")

    if token in known_tokens:
        if debug:
            print(f"[✔️ WHOLE TOKEN MATCH] Full token '{token}' is directly known")
        return [token]

    if debug:
        print("[❌ FULL SPLIT FAILED] No valid split or resolver result found.")

    # 🧠 FINAL LAYER FALLBACK: Try longest known substring match
    longest_known = ""
    start_idx = -1

    for known in known_tokens:
        idx = token.find(known)
        if idx != -1 and len(known) > len(longest_known):
            longest_known = known
            start_idx = idx

    if longest_known:
        prefix = token[:start_idx]
        suffix = token[start_idx + len(longest_known):]
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(longest_known)
        if suffix:
            parts.append(suffix)

        if debug:
            print(f"[🧪 FINAL FALLBACK] Longest known inside token: '{longest_known}'")
            print(f" → Decomposed as: {parts}")
        return parts

    return []


def singularize(word: str) -> str:
    """
    Heuristically converts simple plural forms to singular
    by stripping trailing 's' (unless ending in 'ss').

    Args:
        word (str): Input word (e.g., 'pinks', 'dresses').

    Returns:
        str: Singular form if applicable, else original.
    """
    if len(word) >= 4 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

