# Chatbot/tests/extractors/color/logic/test_get_all_trigger_tokens.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.color.utils.expression_helpers import get_all_trigger_tokens


# Load the expression JSON once at module level
expression_map = load_json_from_data_dir("expression_definition.json")
all_results = get_all_trigger_tokens()

# Limit to first 50 expressions or fewer if less exist
test_expressions = list(expression_map.keys())[:50]


class TestGetAllTriggerTokens(unittest.TestCase):
    def run_case(self, expression):
        expected_tokens = set(
            expression_map[expression].get("modifiers", []) +
            expression_map[expression].get("aliases", [])
        )
        actual_tokens = set(all_results.get(expression, []))
        self.assertEqual(
            expected_tokens,
            actual_tokens,
            f"Mismatch for '{expression}'\nExpected: {expected_tokens}\nActual:   {actual_tokens}"
        )

# Dynamically add 50 test methods to the class
def gen_test(expr):
    def test(self):
        self.run_case(expr)
    return test

for i, expr in enumerate(test_expressions, 1):
    test_name = f"test_case_{i:02d}"
    setattr(TestGetAllTriggerTokens, test_name, gen_test(expr))


if __name__ == "__main__":
    unittest.main()
