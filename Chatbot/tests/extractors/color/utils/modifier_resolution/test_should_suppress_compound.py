# Chatbot/tests/extractors/color/utils/test_should_suppress_compound.py

import unittest
from Chatbot.extractors.color.utils.modifier_resolution import should_suppress_compound
from Chatbot.extractors.color.shared.vocab import known_tones

class TestShouldSuppressCompound(unittest.TestCase):

    def run_case(self, raw_modifier, resolved_modifier, resolved_tone, expected):
        result = should_suppress_compound(raw_modifier, resolved_modifier, resolved_tone, known_tones)
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("peachy", "peach", None, True)
    def test_case_02(self): self.run_case("rosy", "rose", None, True)
    def test_case_03(self): self.run_case("plummy", "plum", None, True)
    def test_case_04(self): self.run_case("berry", "berry", None, True)
    def test_case_05(self): self.run_case("minty", "mint", None, True)
    def test_case_06(self): self.run_case("ashy", "ash", None, True)
    def test_case_07(self): self.run_case("inky", "ink", None, True)
    def test_case_08(self): self.run_case("mochy", "mocha", None, True)
    def test_case_09(self): self.run_case("taupey", "taupe", None, True)
    def test_case_10(self): self.run_case("goldy", "gold", None, True)

    def test_case_11(self): self.run_case("peachy", "peach", "pink", False)
    def test_case_12(self): self.run_case("rosy", "rose", "mauve", False)
    def test_case_13(self): self.run_case("berry", "berry", "plum", False)
    def test_case_14(self): self.run_case("minty", "mint", "green", False)
    def test_case_15(self): self.run_case("inky", "ink", "black", False)

    def test_case_16(self): self.run_case("peach", "peach", None, False)
    def test_case_17(self): self.run_case("rose", "rose", None, False)
    def test_case_18(self): self.run_case("ink", "ink", None, False)
    def test_case_19(self): self.run_case("mint", "mint", None, False)
    def test_case_20(self): self.run_case("ash", "ash", None, False)

    def test_case_21(self): self.run_case("peachy", None, None, False)
    def test_case_22(self): self.run_case("peachy", "peach", "tone", False)
    def test_case_23(self): self.run_case("moody", "mood", None, False)
    def test_case_24(self): self.run_case("sunny", "sun", None, False)
    def test_case_25(self): self.run_case("glowy", "glow", None, False)

    def test_case_26(self): self.run_case("peachy", "peach", "", False)
    def test_case_27(self): self.run_case("rosy", "rose", "", False)
    def test_case_28(self): self.run_case("plummy", "plum", "", False)
    def test_case_29(self): self.run_case("berry", "berry", "", False)
    def test_case_30(self): self.run_case("minty", "mint", "", False)

    def test_case_31(self): self.run_case("ashy", "ash", "", False)
    def test_case_32(self): self.run_case("inky", "ink", "", False)
    def test_case_33(self): self.run_case("mochy", "mocha", "", False)
    def test_case_34(self): self.run_case("taupey", "taupe", "", False)
    def test_case_35(self): self.run_case("goldy", "gold", "", False)

    def test_case_36(self): self.run_case("peachy", "peach", "rose", False)
    def test_case_37(self): self.run_case("rosy", "rose", "plum", False)
    def test_case_38(self): self.run_case("plummy", "plum", "berry", False)
    def test_case_39(self): self.run_case("berry", "berry", "wine", False)
    def test_case_40(self): self.run_case("minty", "mint", "ice", False)

    def test_case_41(self): self.run_case("ashy", "ash", "gray", False)
    def test_case_42(self): self.run_case("inky", "ink", "navy", False)
    def test_case_43(self): self.run_case("mochy", "mocha", "brown", False)
    def test_case_44(self): self.run_case("taupey", "taupe", "beige", False)
    def test_case_45(self): self.run_case("goldy", "gold", "yellow", False)

    def test_case_46(self): self.run_case("sunny", "sun", None, False)
    def test_case_47(self): self.run_case("chalky", "chalk", None, False)
    def test_case_48(self): self.run_case("cloudy", "cloud", None, False)
    def test_case_49(self): self.run_case("muddy", "mud", None, True)
    def test_case_50(self): self.run_case("dusty", "dust", None, True)

if __name__ == "__main__":
    unittest.main()
