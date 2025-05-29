# Chatbot/extractors/color/simplifier.py
"""
Color Simplifier Module
-----------------------
Simplifies user-provided descriptive color phrases using an LLM via OpenRouter API.
Maps non-standard inputs (e.g., 'blush', 'peachy') to normalized cosmetic color tones
(e.g., 'soft pink', 'light peach').

Includes:
- Caching logic to avoid repeated LLM calls
- Clear prompt construction
- Validation of returned tones
"""

import os
import json
import requests
import webcolors
from typing import List

from matplotlib.colors import XKCD_COLORS

from dotenv import load_dotenv
load_dotenv()

def get_cached_simplified(phrase: str) -> List[str]:
    """
    Placeholder for cache retrieval logic.

    Args:
        phrase (str): The input phrase.

    Returns:
        List[str]: Cached simplified phrase if present, else empty list.
    """
    # Implement your cache retrieval here.
    return []


def store_simplified_to_cache(phrase: str, simplified: List[str]) -> None:
    """
    Placeholder for cache storage logic.

    Args:
        phrase (str): The original phrase.
        simplified (List[str]): The simplified phrase list.
    """
    # Implement your cache storage here.
    pass


def simplify_phrase_if_needed(phrase: str) -> List[str]:
    """
    Returns a simplified version of a color phrase if possible,
    using cache and fallback to an LLM simplification call.

    Args:
        phrase (str): The user input color phrase.

    Returns:
        List[str]: Simplified phrase list or the original phrase in a list.
    """
    cached = get_cached_simplified(phrase)
    if cached:
        return cached

    simplified = simplify_color_description_with_llm(phrase)
    if simplified:
        store_simplified_to_cache(phrase, simplified)
        return simplified

    return [phrase]


def build_prompt(color_phrase: str) -> str:
    """
    Builds the prompt string for the LLM given the input color phrase.

    Args:
        color_phrase (str): The color phrase to simplify.

    Returns:
        str: The formatted prompt.
    """
    return (
        f"You are a beauty product color simplifier.\n"
        f"Your task is to determine if the word '{color_phrase}' refers to an actual color or shade used in makeup, cosmetics, or fashion.\n"
        f"If it clearly refers to a color, return a simplified version using a tone and optional modifier (e.g., 'soft pink').\n"
        f"If it is not a color (e.g., 'elegant', 'luxurious', 'shiny', 'clean'), return an empty string.\n"
        f"⚠️ Only output a valid tone or modifier + tone. No explanations, no punctuation.\n\n"
        f"Examples:\n"
        f"- 'elegant' → ''\n"
        f"- 'success' → ''\n"
        f"- 'peachy' → 'light peach'\n"
        f"- 'blush' → 'soft pink'\n\n"
        f"Only return the simplified phrase."
    )


def is_valid_tone(token: str, tone_keywords: set) -> bool:
    """
    Determines if a token is a valid tone based on known tones and heuristics.

    Args:
        token (str): Token to check.
        tone_keywords (set): Set of known valid tone names.

    Returns:
        bool: True if token is valid tone, False otherwise.
    """
    return token in tone_keywords or token.endswith(("ish", "y")) or len(token) <= 10


def simplify_color_description_with_llm(color_phrase: str) -> List[str]:
    """
    Simplifies a descriptive color phrase into a normalized modifier + tone
    by querying an LLM through the OpenRouter API.

    Args:
        color_phrase (str): Raw user input color phrase.

    Returns:
        List[str]: List containing a simplified phrase or empty list if none.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    prompt = build_prompt(color_phrase)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 15,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data)
    )
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error {response.status_code}: {response.text}")

    raw_response = response.json()["choices"][0]["message"]["content"].strip().lower()
    if not raw_response:
        return []

    tokens = raw_response.split()

    css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
    xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS)
    tone_keywords = css_tones.union(xkcd_tones)

    # Look for modifier + tone pair first
    for i in range(len(tokens) - 1):
        mod, tone = tokens[i], tokens[i + 1]
        if is_valid_tone(tone, tone_keywords):
            return [f"{mod} {tone}"]

    # If no pair found, return single valid tone if any
    for token in tokens:
        if is_valid_tone(token, tone_keywords):
            return [token]

    return []
