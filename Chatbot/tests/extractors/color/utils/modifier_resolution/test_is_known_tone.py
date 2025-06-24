# Chatbot/tests/extractors/color/shared/utils/test_is_known_tone.py

import unittest
from Chatbot.extractors.color.utils.modifier_resolution import is_known_tone

class TestIsKnownTone(unittest.TestCase):

    def run_case(self, word, expected):
        result = is_known_tone(word)
        self.assertEqual(expected, result, f"Word: '{word}' Expected: {expected} Got: {result}")

    # 25 positive cases (words in known_tones)
    def test_case_01(self): self.run_case("Pink", True)
    def test_case_02(self): self.run_case("beige", True)
    def test_case_03(self): self.run_case("OLIVE", True)
    def test_case_04(self): self.run_case("mint", True)
    def test_case_05(self): self.run_case("Peach", True)
    def test_case_06(self): self.run_case("coral", True)
    def test_case_07(self): self.run_case("lavender", True)
    def test_case_08(self): self.run_case("cyan", True)
    def test_case_09(self): self.run_case("turquoise", True)
    def test_case_10(self): self.run_case("crimson", True)
    def test_case_11(self): self.run_case("maroon", True)
    def test_case_12(self): self.run_case("teal", True)
    def test_case_13(self): self.run_case("navy", True)
    def test_case_14(self): self.run_case("gold", True)
    def test_case_15(self): self.run_case("silver", True)
    def test_case_16(self): self.run_case("bronze", True)
    def test_case_17(self): self.run_case("cream", True)
    def test_case_18(self): self.run_case("charcoal", True)
    def test_case_19(self): self.run_case("tan", True)
    def test_case_20(self): self.run_case("mustard", True)
    def test_case_21(self): self.run_case("rose", True)
    def test_case_22(self): self.run_case("ivory", True)
    def test_case_23(self): self.run_case("plum", True)
    def test_case_24(self): self.run_case("salmon", True)
    def test_case_25(self): self.run_case("fuchsia", True)

    def test_case_26(self): self.run_case("blurple", True)
    def test_case_27(self): self.run_case("invisible", False)
    def test_case_28(self): self.run_case("sparkly", False)
    def test_case_29(self): self.run_case("bluish", True)
    def test_case_30(self): self.run_case("soft", False)
    def test_case_31(self): self.run_case("brightish", False)
    def test_case_32(self): self.run_case("muted", False)
    def test_case_33(self): self.run_case("darkish", False)
    def test_case_34(self): self.run_case("ghost", False)
    def test_case_35(self): self.run_case("none", False)
    def test_case_36(self): self.run_case("clear", False)
    def test_case_37(self): self.run_case("medium", False)
    def test_case_38(self): self.run_case("soft-focus", False)
    def test_case_39(self): self.run_case("deepish", False)
    def test_case_40(self): self.run_case("faint", False)
    def test_case_41(self): self.run_case("smoky", False)
    def test_case_42(self): self.run_case("brighty", False)
    def test_case_43(self): self.run_case("warmth", False)
    def test_case_44(self): self.run_case("lighty", False)
    def test_case_45(self): self.run_case("rosebud", False)
    def test_case_46(self): self.run_case("", False)
    def test_case_47(self): self.run_case(" ", False)
    def test_case_48(self): self.run_case("123", False)
    def test_case_49(self): self.run_case("pinkish", True)
    def test_case_50(self): self.run_case("reddish", True)


if __name__ == "__main__":
    unittest.main()
