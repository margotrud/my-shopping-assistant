# Chatbot/extractors/color/utils/config_loader.py

"""
config_loader.py
----------------

Generic loader for configuration and vocabulary files stored in the project's /Data directory.

This utility is used throughout the color extraction pipeline to load known modifiers,
expression triggers, tone mappings, and more.

By centralizing the file access logic, the project avoids redundant loader functions like:
    - load_known_modifiers()
    - load_expression_triggers()
    - load_expression_context_rules()

Instead, all these are replaced with:

    from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
    known_modifiers = set(load_json_from_data_dir("known_modifiers.json"))

Expected JSON directory structure:
    /Data/
    ├── known_modifiers.json
    ├── expression_triggers.json
    ├── expression_context_rules.json

Raises:
    - FileNotFoundError: If the file is missing.
    - json.JSONDecodeError: If the file is not valid JSON.

This script contributes to making the codebase DRY, modular, and professional.
"""

import json
from pathlib import Path
from typing import Set, Dict


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
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_known_modifiers() -> Set[str]:
    """
    Loads the known modifier vocabulary from 'Data/known_modifiers.json'.

    The JSON file should contain a list of modifier strings.

    Returns:
        Set[str]: Set of modifier strings (e.g., {'soft', 'bold'}).

    Raises:
        FileNotFoundError: If the JSON file is not found at expected path.
        ValueError: If the JSON content is invalid or malformed.
    """
    data_path = Path(__file__).resolve().parents[3] / "Data" / "known_modifiers.json"
    print(f"[DEBUG] Trying to load from: {data_path}")

    try:
        with data_path.open("r", encoding="utf-8") as f:
            modifiers = json.load(f)
        return set(modifiers)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Modifier vocab file not found at {data_path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in modifier vocab file at {data_path}") from e

def load_known_suffix_tokens() -> Set[str]:
    """
    Loads known suffix tokens used for NLP-aware phrase splitting (e.g., 'tone', 'shade').

    Returns:
        Set[str]: A set of valid suffix tokens.
    """
    return set(load_json_from_data_dir("known_suffix_tokens.json"))

def load_expression_context_rules() -> Dict[str, Dict[str, list]]:
    """
    Loads contextual promotion rules used for expression inference from tokens.

    Expects a JSON file named `expression_context_rules.json` in the /Data directory
    structured as:
        {
            "expression_name": {
                "require_tokens": [...],
                "context_clues": [...]
            },
            ...
        }

    Returns:
        Dict[str, Dict[str, List[str]]]: Context rules for expression tagging.
    """
    data_dir = Path(__file__).resolve().parents[3] / "Data"
    file_path = data_dir / "expression_context_rules.json"

    if not file_path.exists():
        raise FileNotFoundError(f"[❌ MISSING FILE] Could not find: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)