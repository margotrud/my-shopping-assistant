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
