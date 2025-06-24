"""
llm_api_client.py
=================

Handles LLM requests for converting descriptive color phrases to RGB.
Uses OpenRouter API with configurable prompt and retry-safe logic.
"""

import os
import re
import json
import time
import logging
import requests
from typing import Optional, Tuple

# ------------------ LLM CONFIG ------------------ #

LLM_API_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "mistralai/mistral-7b-instruct"
LLM_MAX_TOKENS = 100
LLM_TEMPERATURE = 0.4

logger = logging.getLogger(__name__)

# ------------------ PROMPT BUILDER ------------------ #

def build_color_prompt(color_phrase: str) -> str:
    return (
        f"What is the RGB color code for the descriptive phrase: '{color_phrase}'?\n"
        "Respond ONLY with an RGB tuple in the form (R, G, B), without any explanation.\n"
        "Examples:\n"
        "- 'warm beige' → (245, 222, 179)\n"
        "- 'deep lavender' → (150, 123, 182)\n"
        "- 'rosy nude' → (231, 180, 188)\n"
        f"Now: '{color_phrase}' →"
    )

def build_llm_request_payload(color_phrase: str) -> dict:
    prompt = build_color_prompt(color_phrase)
    return {
        "model": LLM_MODEL,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }


def build_llm_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


# ------------------ RGB PARSER ------------------ #

def _parse_rgb_tuple(response: str, debug=False) -> Optional[Tuple[int, int, int]]:
    match = re.search(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", response)
    if not match:
        if debug:
            logger.warning(f"[❌ PARSE FAIL] Could not extract RGB from response: {response}")
        return None

    r, g, b = map(int, match.groups())
    if all(0 <= val <= 255 for val in (r, g, b)):
        return (r, g, b)

    if debug:
        logger.warning(f"[❌ OUT-OF-RANGE] RGB out of bounds: {r}, {g}, {b}")
    return None


# ------------------ MAIN REQUEST FUNCTION ------------------ #

def query_llm_for_rgb(
        color_phrase: str,
        llm_client=None,
        cache=None,
        retries: int = 2,
        debug: bool = False
) -> Optional[Tuple[int, int, int]]:
    """
    Queries the LLM and parses an RGB tuple response.
    Includes retry and logging.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("[⛔ NO API KEY] OPENROUTER_API_KEY not found in environment.")
        return None

    if cache:
        cached = cache.get_rgb(color_phrase)
        if cached:
            if debug:
                logger.info(f"[🗃️ CACHE HIT] '{color_phrase}' → {cached}")
            return cached

    payload = build_llm_request_payload(color_phrase)
    headers = build_llm_headers(api_key)

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                LLM_API_URL,
                headers=headers,
                json=payload,
                timeout=10
            )

            if debug:
                logger.info(f"[📡 LLM QUERY] Attempt {attempt + 1}: '{color_phrase}'")

            if response.status_code != 200:
                logger.warning(f"[⚠️ LLM FAILURE] Status {response.status_code}: {response.text}")
                time.sleep(1.5 * (attempt + 1))
                continue

            reply = response.json()["choices"][0]["message"]["content"]
            rgb = _parse_rgb_tuple(reply, debug=debug)

            if rgb and cache:
                cache.store_rgb(color_phrase, rgb)

            return rgb

        except Exception as e:
            logger.error(f"[💥 EXCEPTION] LLM request failed on attempt {attempt + 1}: {e}")
            time.sleep(1.5 * (attempt + 1))

    if debug:
        logger.warning(f"[🚫 TOTAL FAILURE] '{color_phrase}' → No valid RGB response.")
    return None
