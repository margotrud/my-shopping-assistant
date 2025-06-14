"""
llm_api_client.py
=================
Handles the HTTP interaction with the LLM service to resolve descriptive color names into RGB values.

Responsibilities:
-----------------
- Format model-friendly prompts
- Build HTTP headers with secure API key usage
- Send requests to OpenRouter endpoint
- Parse and validate RGB results from JSON responses

This module supports color matching in fashion, cosmetics, and design
by turning vague phrases like "peachy beige" into actual RGB triplets.

Dependencies:
-------------
- Environment variable: OPENROUTER_API_KEY
- External: requests, regex (RGB pattern)
"""

import os
import json
import requests
import logging
from typing import Optional, Tuple

from Chatbot.extractors.color.utils.regex_patterns import RGB_REGEX

logger = logging.getLogger(__name__)


def build_llm_request_payload(color_phrase: str) -> dict:
    """
    Builds the prompt and payload for querying the LLM for an RGB value.

    Args:
        color_phrase (str): Descriptive color name (e.g., 'dusty pink').

    Returns:
        dict: LLM API request payload.
    """
    prompt = (
        f"You're a color matching assistant. Given the color name '{color_phrase}', "
        "estimate its most accurate RGB value based on design and fashion standards. "
        "Return only the result in this exact JSON format: {\"rgb\": [R, G, B]} "
        "with integers between 0 and 255. No explanation.\n\n"
        "Use examples like: 'dusty pink' → [213, 138, 148], 'peachy beige' → [243, 207, 183]"
    )

    return {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 20,
    }


def build_llm_headers(api_key: str) -> dict:
    """
    Builds the headers for the LLM API call.

    Args:
        api_key (str): Secret key from OpenRouter.

    Returns:
        dict: HTTP request headers.
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def query_llm_for_rgb(color_phrase: str) -> Optional[Tuple[int, int, int]]:
    """
    Queries the LLM to estimate an RGB tuple for a descriptive color phrase.

    Includes validation, fallback handling, and logging for bad responses.

    Args:
        color_phrase (str): Descriptive color phrase (e.g., 'soft coral').

    Returns:
        Optional[Tuple[int, int, int]]: RGB result if valid, else None.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    try:
        headers = build_llm_headers(api_key)
        payload = build_llm_request_payload(color_phrase)

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"[LLM REQUEST ERROR] {e}")
        return None

    try:
        raw_output = response.json()["choices"][0]["message"]["content"].strip()
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"[LLM RESPONSE PARSE ERROR] {e}")
        return None

    match = RGB_REGEX.search(raw_output)
    if match:
        try:
            r, g, b = map(int, match.groups())
            if all(0 <= val <= 255 for val in (r, g, b)):
                return (r, g, b)
            logger.warning(f"[⚠️ INVALID RANGE] RGB out of 0–255: {r}, {g}, {b}")
        except Exception as e:
            logger.error(f"[RGB PARSE ERROR] {e}")
    else:
        logger.warning(f"[⚠️ UNEXPECTED FORMAT] LLM Output: {raw_output}")

    return None
