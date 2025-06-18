# utils/dev_generate_expected_map_tones.py

import json
from pathlib import Path
from Chatbot.extractors.color.logic.expression_matcher import map_expressions_to_tones
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.color import known_tones

TEST_PHRASES = [
    "I like soft glam",
    "Show me something edgy",
    "What about a natural style?",
    "Looking for daytime colors",
    "I want something romantic",
    "Show me bold makeup",
    "Do you have anything subtle?",
    "Elegant tones please",
    "I prefer something glamorous",
    "Evening looks are great",
    # Add more test cases here if needed
]

def generate_expected_results():
    expression_def = load_json_from_data_dir("expression_definition.json")
    results = {}

    for phrase in TEST_PHRASES:
        mapped = map_expressions_to_tones(phrase, expression_def, known_tones)
        results[phrase] = mapped

    output_path = Path(__file__).resolve().parents[3] / "tests" / "extractors" / "color" / "data" / "expected_map_expressions.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[✅ DONE] Expected tone mappings written to → {output_path}")

if __name__ == "__main__":
    generate_expected_results()
