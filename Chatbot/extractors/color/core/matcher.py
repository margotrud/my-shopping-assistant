#Chatbot/extractors/color/matcher.py
"""
Modifier Matcher Module
-----------------------
Provides functions to load a known modifier vocabulary and perform fuzzy matching
to handle user input variations or typos in modifier names (e.g., matching 'brigt' to 'bright').

Features:
- Loads modifier vocabulary dynamically from JSON file in the project.
- Uses rapidfuzz for efficient fuzzy matching with a configurable threshold.
"""

from pathlib import Path
import json
from typing import Set, Optional
from rapidfuzz import process

from rapidfuzz import fuzz
from typing import Dict, List
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
    data_path = Path(__file__).resolve().parents[4] / "Data" / "known_modifiers.json"
    print(f"[DEBUG] Trying to load from: {data_path}")

    try:
        with data_path.open("r", encoding="utf-8") as f:
            modifiers = json.load(f)
        return set(modifiers)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Modifier vocab file not found at {data_path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in modifier vocab file at {data_path}") from e


def fuzzy_match_modifier(
    modifier: str,
    known_modifiers: Set[str],
    threshold: int = 80
) -> Optional[str]:
    """
    Performs fuzzy string matching to find the closest known modifier
    to the input string.

    Args:
        modifier (str): The input modifier string to match (e.g., 'brigt').
        known_modifiers (Set[str]): Set of known valid modifiers.
        threshold (int): Minimum similarity score (0–100) to consider a match.

    Returns:
        Optional[str]: The best matching known modifier if similarity
                       exceeds the threshold; otherwise None.
    """
    if not modifier:
        return None

    match = process.extractOne(modifier.lower(), known_modifiers, scorer=fuzz.ratio)
    return match[0] if match and match[1] >= threshold else None

def match_multiword_expressions(text: str, expression_map: Dict[str, List[str]], threshold: int = 85) -> List[str]:
    """
    Checks for approximate matches of multi-word expression triggers in the full text.

    Args:
        text (str): The user input text (e.g., "light glam, soft finish").
        expression_map (Dict[str, List[str]]): Mapping of expression → list of trigger phrases.
        threshold (int): Fuzzy match threshold (0-100).

    Returns:
        List[str]: List of expression categories matched (e.g., ["soft glam"]).
    """
    matched = set()
    lowered_text = text.lower()

    for expression, triggers in expression_map.items():
        for trigger in triggers:
            if " " in trigger:
                score = fuzz.token_sort_ratio(trigger.lower(), lowered_text)
                if score >= threshold:
                    matched.add(expression)
                    break  # One trigger is enough to match the expression

    return list(matched)


