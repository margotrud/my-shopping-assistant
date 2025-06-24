# tests/test_is_blocked_modifier_tone_pair.py

import unittest
from Chatbot.extractors.color.logic.compound_rule import is_blocked_modifier_tone_pair
from Chatbot.extractors.color.shared.constants import BLOCKED_TOKENS


class TestIsBlockedModifierTonePair(unittest.TestCase):

    def run_case(self, mod, tone, expected_result):
        result = is_blocked_modifier_tone_pair(mod, tone, BLOCKED_TOKENS)
        self.assertEqual(expected_result, result, f"Expected: {expected_result}\nActual: {result}")

    def test_case_01(self): self.run_case("light", "night", True)
    def test_case_02(self): self.run_case("night", "light", True)
    def test_case_03(self): self.run_case("romantic", "dramatic", True)
    def test_case_04(self): self.run_case("dramatic", "romantic", True)
    def test_case_05(self): self.run_case("bold", "neutral", False)
    def test_case_06(self): self.run_case("neutral", "bold", False)
    def test_case_07(self): self.run_case("glamorous", "daytime", False)
    def test_case_08(self): self.run_case("daytime", "glamorous", False)
    def test_case_09(self): self.run_case("edgy", "romantic", False)
    def test_case_10(self): self.run_case("soft glam", "edgy", False)

    def test_case_11(self): self.run_case("soft", "pink", False)
    def test_case_12(self): self.run_case("light", "pink", False)
    def test_case_13(self): self.run_case("deep", "rose", False)
    def test_case_14(self): self.run_case("muted", "nude", False)
    def test_case_15(self): self.run_case("romantic", "rose", False)

    def test_case_16(self): self.run_case("daytime", "natural", False)
    def test_case_17(self): self.run_case("subtle", "nude", False)
    def test_case_18(self): self.run_case("intense", "red", False)
    def test_case_19(self): self.run_case("dramatic", "night", False)
    def test_case_20(self): self.run_case("light", "beige", False)


if __name__ == "__main__":
    unittest.main()
