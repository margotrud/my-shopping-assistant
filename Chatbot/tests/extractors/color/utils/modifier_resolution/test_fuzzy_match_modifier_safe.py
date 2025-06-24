# Chatbot/tests/extractors/color/utils/test_fuzzy_match_modifier_safe.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.utils.modifier_resolution import fuzzy_match_modifier_safe

class TestFuzzyMatchModifierSafe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()

    def run_case(self, word, expected, threshold=83):
        result = fuzzy_match_modifier_safe(word, self.known_modifiers, threshold)
        self.assertEqual(expected, result, f"Input: '{word}' Threshold: {threshold} Expected: {expected} Got: {result}")


    # 25 positive cases with expected fuzzy matches (score >= threshold)
    def test_case_01(self): self.run_case("soft", "soft")
    def test_case_02(self): self.run_case("sofft", "soft")        # minor typo
    def test_case_03(self): self.run_case("muted", "muted")
    def test_case_04(self): self.run_case("mutd", "muted")
    def test_case_05(self): self.run_case("bright", "bright")
    def test_case_06(self): self.run_case("brigt", "bright")
    def test_case_07(self): self.run_case("dark", "dark")
    def test_case_08(self): self.run_case("dakr", "dark")
    def test_case_09(self): self.run_case("light", "light")
    def test_case_10(self): self.run_case("ligt", "light")
    def test_case_11(self): self.run_case("warm", "warm")
    def test_case_12(self): self.run_case("wram", None)
    def test_case_13(self): self.run_case("cool", "cool")
    def test_case_14(self): self.run_case("col", "cool")
    def test_case_15(self): self.run_case("dusty", "dust")
    def test_case_16(self): self.run_case("dusy", "dust")
    def test_case_17(self): self.run_case("rosy", "rose")
    def test_case_18(self): self.run_case("ros", "rose")
    def test_case_19(self): self.run_case("soft-focus", "soft-focus")
    def test_case_20(self): self.run_case("soft focu", "soft-focus")
    def test_case_21(self): self.run_case("matte", "matte")
    def test_case_22(self): self.run_case("mate", "matte")
    def test_case_23(self): self.run_case("velvet", "velvet")
    def test_case_24(self): self.run_case("velvet", "velvet")
    def test_case_25(self): self.run_case("glossy", "gloss")

    # 25 negative cases (expected None due to low similarity or unknown)
    def test_case_26(self): self.run_case("blurple", None)
    def test_case_27(self): self.run_case("invisible", None)
    def test_case_28(self): self.run_case("sparkly", "sparkly")
    def test_case_29(self): self.run_case("brightish", "bright")
    def test_case_30(self): self.run_case("softy", "soft")
    def test_case_31(self): self.run_case("softish", "soft")
    def test_case_32(self): self.run_case("darkish", "dark")
    def test_case_33(self): self.run_case("ghost", None)
    def test_case_34(self): self.run_case("none", None)
    def test_case_35(self): self.run_case("clear", "clean")
    def test_case_36(self): self.run_case("medium", "medium")
    def test_case_37(self): self.run_case("soft-focusx", "soft-focus")
    def test_case_38(self): self.run_case("deepish", "deep")
    def test_case_39(self): self.run_case("faint", "faint")  # maybe faint is modifier? adjust if needed
    def test_case_40(self): self.run_case("smoky", "smoke")
    def test_case_41(self): self.run_case("brighty", "bright")
    def test_case_42(self): self.run_case("warmth", "warm")
    def test_case_43(self): self.run_case("lighty", "light")
    def test_case_44(self): self.run_case("rosebud", "rose")
    def test_case_45(self): self.run_case("", None)
    def test_case_46(self): self.run_case(" ", None)
    def test_case_47(self): self.run_case("123", None)
    def test_case_48(self): self.run_case("pinkish", "pinkish")
    def test_case_49(self): self.run_case("reddish", "reddish")
    def test_case_50(self): self.run_case("soft-focus-", "soft-focus")

if __name__ == "__main__":
    unittest.main()

