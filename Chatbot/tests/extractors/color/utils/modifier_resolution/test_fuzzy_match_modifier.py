# Chatbot/tests/extractors/color/utils/test_fuzzy_match_modifier.py

import unittest
from Chatbot.extractors.color.utils.modifier_resolution import _fuzzy_match_modifier
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

class TestFuzzyMatchModifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()

    def run_case(self, raw, expected_match, min_expected_score=70):
        result = _fuzzy_match_modifier(raw, self.known_modifiers)
        if expected_match is None:
            self.assertIsNone(result, f"Expected None for input '{raw}' but got {result}")
        else:
            self.assertIsNotNone(result, f"Expected match for '{raw}' but got None")
            match, score = result
            self.assertEqual(expected_match, match, f"Expected match '{expected_match}', got '{match}' for input '{raw}'")
            self.assertGreaterEqual(score, min_expected_score, f"Score {score} below threshold {min_expected_score} for input '{raw}'")

    # 25 positive cases (expected best match returned with decent score)
    def test_case_01(self): self.run_case("soft", "soft")
    def test_case_02(self): self.run_case("sofft", "soft")
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
    def test_case_24(self): self.run_case("glossy", "gloss")
    def test_case_25(self): self.run_case("smooth", "smooth")

    # 25 negative cases (expected None for no decent match)
    def test_case_26(self): self.run_case("blurple", "blur")
    def test_case_27(self): self.run_case("invisible", None)
    def test_case_28(self): self.run_case("sparkly", "sparkly")
    def test_case_29(self): self.run_case("brightish", "bright")
    def test_case_30(self): self.run_case("softy", "soft")
    def test_case_31(self): self.run_case("softish", "soft")
    def test_case_32(self): self.run_case("darkish", "dark")
    def test_case_33(self): self.run_case("ghost", None)
    def test_case_34(self): self.run_case("none", None)
    def test_case_35(self): self.run_case("clear", "clear")
    def test_case_36(self): self.run_case("medium", "medium")
    def test_case_37(self): self.run_case("soft-focusx", "soft-focus")
    def test_case_38(self): self.run_case("deepish", "deep")
    def test_case_39(self): self.run_case("faint", "faint")  # adjust if faint is modifier
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
