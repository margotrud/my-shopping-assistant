# Chatbot/tests/extractors/color/utils/test_match_suffix_fallback.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.utils.modifier_resolution import match_suffix_fallback

class TestMatchSuffixFallback(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()

    def run_case(self, word, expected):
        result = match_suffix_fallback(word, self.known_modifiers)
        self.assertEqual(expected, result, f"Input: '{word}' Expected: {expected} Got: {result}")

    # 25 positive cases (should return base modifier)
    def test_case_01(self): self.run_case("dusty", "dust")
    def test_case_02(self): self.run_case("rosy", "rose")
    def test_case_03(self): self.run_case("smoky", "smoke")
    def test_case_04(self): self.run_case("softy", "soft")
    def test_case_05(self): self.run_case("mutedish", "muted")
    def test_case_06(self): self.run_case("brightish", "bright")
    def test_case_07(self): self.run_case("boldish", "bold")
    def test_case_08(self): self.run_case("cooly", "cool")
    def test_case_09(self): self.run_case("warmy", "warm")
    def test_case_10(self): self.run_case("faintish", "faint")
    def test_case_11(self): self.run_case("glossy", "gloss")
    def test_case_12(self): self.run_case("velvety", "velvet")
    def test_case_13(self): self.run_case("silky", "silk")
    def test_case_14(self): self.run_case("chalky", "chalk")
    def test_case_15(self): self.run_case("peachy", "peach")
    def test_case_16(self): self.run_case("earthy", None)
    def test_case_17(self): self.run_case("creamy", "cream")
    def test_case_18(self): self.run_case("rosy-", None)  # trailing hyphen stripped
    def test_case_19(self): self.run_case("dusty ", None)  # trailing space stripped
    def test_case_20(self): self.run_case("FOOishy", None)  # base not in modifiers
    def test_case_21(self): self.run_case("sandy", "sand")
    def test_case_22(self): self.run_case("rainy", None)
    def test_case_23(self): self.run_case("pasty", None)
    def test_case_24(self): self.run_case("shady", "shade")
    def test_case_25(self): self.run_case("spicy", None)

    # 25 negative cases (should return None)
    def test_case_26(self): self.run_case("dy", None)           # base too short
    def test_case_27(self): self.run_case("ish", None)          # base empty
    def test_case_28(self): self.run_case("y", None)            # only suffix
    def test_case_29(self): self.run_case("dyish", None)        # base too short "dy"
    def test_case_30(self): self.run_case("45ish", None)        # base non-alpha
    def test_case_31(self): self.run_case("softyy", None)       # endswith "y" but base "softy" not in modifiers
    def test_case_32(self): self.run_case("soft-ish", "soft")     # base "soft-" stripped hyphen but still not in modifiers (usually hyphen not allowed)
    def test_case_33(self): self.run_case("soft y", "soft")       # space breaks base alpha test
    def test_case_34(self): self.run_case("smokeyy", None)
    def test_case_35(self): self.run_case("brighty-", None)
    def test_case_36(self): self.run_case("mutedish", "muted")
    def test_case_37(self): self.run_case("light-", None)
    def test_case_38(self): self.run_case("", None)              # empty string
    def test_case_39(self): self.run_case(" ", None)             # space only
    def test_case_40(self): self.run_case("softishy", None)      # suffix inside word
    def test_case_41(self): self.run_case("coolish-", None)
    def test_case_42(self): self.run_case("coldy", None)         # base "cold" not in modifiers (assuming)
    def test_case_43(self): self.run_case("dustyy", None)
    def test_case_44(self): self.run_case("dustyishy", None)
    def test_case_45(self): self.run_case("dustyish-", None)
    def test_case_46(self): self.run_case("fasty", None)
    def test_case_47(self): self.run_case("dust", None)           # no suffix, should return None
    def test_case_48(self): self.run_case("pink", None)
    def test_case_49(self): self.run_case("redish", None)        # base "red" not in modifiers
    def test_case_50(self): self.run_case("softishish", None)

if __name__ == "__main__":
    unittest.main()
