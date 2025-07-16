# Chatbot/tests/extractors/color/utils/test_match_direct_modifier.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.utils.modifier_resolution import match_direct_modifier

class TestMatchDirectModifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()

    def run_case(self, word, expected):
        result = match_direct_modifier(word, self.known_modifiers)
        self.assertEqual(expected, result, f"Input: '{word}' Expected: {expected} Got: {result}")

    # 25 positive tests (words that should match)
    def test_case_01(self): self.run_case("soft", "soft")
    def test_case_02(self): self.run_case("Muted", "muted")
    def test_case_03(self): self.run_case("BRIGHT", "bright")
    def test_case_04(self): self.run_case("dark", "dark")
    def test_case_05(self): self.run_case("light", "light")
    def test_case_06(self): self.run_case("warm", "warm")
    def test_case_07(self): self.run_case("cool", "cool")
    def test_case_08(self): self.run_case("dusty", "dust")
    def test_case_09(self): self.run_case("rosy", "rose")
    def test_case_10(self): self.run_case("pale", "pale")
    def test_case_11(self): self.run_case("deep", "deep")
    def test_case_12(self): self.run_case("faint", "faint")
    def test_case_13(self): self.run_case("rich", "rich")
    def test_case_14(self): self.run_case("vibrant", "vibrant")
    def test_case_15(self): self.run_case("soft-focus", "soft")
    def test_case_16(self): self.run_case("matte", "matte")
    def test_case_17(self): self.run_case("velvet", "velvet")
    def test_case_18(self): self.run_case("glossy", "gloss")
    def test_case_19(self): self.run_case("smooth", "smooth")
    def test_case_20(self): self.run_case("silky", "silk")
    def test_case_21(self): self.run_case("lightweight", None)   # edge case - likely not modifier
    def test_case_22(self): self.run_case("bold", "bold")
    def test_case_23(self): self.run_case("neutral", "neutral")
    def test_case_24(self): self.run_case("brighten", "bright")
    def test_case_25(self): self.run_case("subtle", "subtle")

    # 25 negative tests (words not in known_modifiers)
    def test_case_26(self): self.run_case("softy", "soft")
    def test_case_27(self): self.run_case("brightish", "bright")
    def test_case_28(self): self.run_case("mutedness", "muted")
    def test_case_29(self): self.run_case("darkish", "dark")
    def test_case_30(self): self.run_case("lighty", "light")
    def test_case_31(self): self.run_case("warmer", "warm")
    def test_case_32(self): self.run_case("cooler", "cool")
    def test_case_33(self): self.run_case("dustier", "dust")
    def test_case_34(self): self.run_case("rosier", "rose")
    def test_case_35(self): self.run_case("palely", "pale")
    def test_case_36(self): self.run_case("deeply", "deep")
    def test_case_37(self): self.run_case("faintly", "faint")
    def test_case_38(self): self.run_case("richly", "rich")
    def test_case_39(self): self.run_case("vibrantly", "vibrant")
    def test_case_40(self): self.run_case("matting", "matte")
    def test_case_41(self): self.run_case("velvety", "velvet")
    def test_case_42(self): self.run_case("glossiness", "gloss")
    def test_case_43(self): self.run_case("smoothly", "smooth")
    def test_case_44(self): self.run_case("silken", "silk")
    def test_case_45(self): self.run_case("boldness", "bold")
    def test_case_46(self): self.run_case("", None)
    def test_case_47(self): self.run_case(" ", None)
    def test_case_48(self): self.run_case("123", None)
    def test_case_49(self): self.run_case("!!", None)
    def test_case_50(self): self.run_case("soft-focus ", "soft")  # trailing space

if __name__ == "__main__":
    unittest.main()
