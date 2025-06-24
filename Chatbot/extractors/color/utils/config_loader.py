# Chatbot/extractors/color/utils/config_loader.py

"""
config_loader.py
================

Loads configuration data from the /Data directory,
including modifiers, context rules, and suffix variants.

Used By:
--------
- Modifier/tone resolution
- Expression context mapping
- Color suffix detection

All functions assume the JSON files are UTF-8 encoded
and located under: Chatbot/Data/
"""

import json
from pathlib import Path
from typing import Set, Dict, List


def load_json_from_data_dir(filename: str) -> dict:
    """
    Loads a JSON file from the project's /Data directory.

    Args:
        filename (str): Name of the JSON file (e.g., 'known_modifiers.json').

    Returns:
        dict: Parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the content is not valid JSON.
    """
    path = Path(__file__).resolve().parents[3] / "Data" / filename
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"[❌ CONFIG LOAD FAILED] File: {filename} — {str(e)}")


def load_known_modifiers() -> Set[str]:
    """
    Loads the known modifier vocabulary from 'known_modifiers.json'.

    Returns:
        Set[str]: Modifier tokens (e.g., {'soft', 'bold', 'dusty'}).
    """
    data = load_json_from_data_dir("known_modifiers.json")
    return set(data)


def load_known_suffix_tokens() -> Set[str]:
    """
    Extracts suffix-style modifiers (ending in 'y' or 'ish').

    Returns:
        Set[str]: Subset of known modifiers like {'peachy', 'rosy', 'brownish'}.
    """
    data = load_json_from_data_dir("known_modifiers.json")
    return {m for m in data if m.endswith("y") or m.endswith("ish")}


def load_expression_context_rules() -> Dict[str, Dict[str, List[str]]]:
    """
    Loads and validates the expression context rule mappings.

    Each rule includes:
    - require_tokens: all must appear
    - context_clues: at least one must appear

    Returns:
        Dict[str, Dict]: Mapping from expression to its context clues.

    Example:
        {
            "romantic": {
                "require_tokens": ["soft"],
                "context_clues": ["flirt", "date"]
            }
        }
    """
    data = load_json_from_data_dir("expression_context_rules.json")
    if not isinstance(data, dict):
        raise ValueError("Context rules must be a dictionary mapping expressions to their rule objects.")
    return data
