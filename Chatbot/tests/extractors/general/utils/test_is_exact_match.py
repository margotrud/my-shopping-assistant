# tests/extractors/general/utils/test_is_exact_match.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import is_exact_match
from Chatbot.extractors.general.utils.fuzzy_match import normalize_token  # used internally

class TestIsExactMatch(unittest.TestCase):

    def run_case(self, a, b, expected):
        result = is_exact_match(a, b)
        print(f"Expected: {expected} | Actual: {result}")
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("blue", "blue", True)
    def test_case_02(self): self.run_case(" Blue", "blue", True)
    def test_case_03(self): self.run_case("blue ", "blue", True)
    def test_case_04(self): self.run_case("  blue  ", "blue", True)
    def test_case_05(self): self.run_case("BLUE", "blue", True)
    def test_case_06(self): self.run_case("BlUe", "blue", True)
    def test_case_07(self): self.run_case("\tbluE", "blue", True)
    def test_case_08(self): self.run_case("blue\n", "blue", True)
    def test_case_09(self): self.run_case(" blue\t\n", "blue", True)
    def test_case_10(self): self.run_case("soft glam", "soft glam", True)

    def test_case_11(self): self.run_case(" Soft Glam", "soft glam", True)
    def test_case_12(self): self.run_case("Soft Glam  ", "soft glam", True)
    def test_case_13(self): self.run_case("  Soft Glam  ", "soft glam", True)
    def test_case_14(self): self.run_case("SoftGlam", "softglam", True)
    def test_case_15(self): self.run_case("rose_gold", "rose_gold", True)

    def test_case_16(self): self.run_case("rose gold ", "rose gold", True)
    def test_case_17(self): self.run_case("   rose   gold   ", "rose   gold", True)
    def test_case_18(self): self.run_case("nude", "nude", True)
    def test_case_19(self): self.run_case(" Nude", "nude", True)
    def test_case_20(self): self.run_case("nUdE", "nude", True)

    def test_case_21(self): self.run_case("lavender-blush", "lavender-blush", True)
    def test_case_22(self): self.run_case("lavender blush", "lavender-blush", False)
    def test_case_23(self): self.run_case("lavender", "lavender blush", False)
    def test_case_24(self): self.run_case("glowy", "glowy", True)
    def test_case_25(self): self.run_case("glowy✨", "glowy", False)

    def test_case_26(self): self.run_case("off white", "offwhite", False)
    def test_case_27(self): self.run_case("offwhite", "off white", False)
    def test_case_28(self): self.run_case("bare skin", "bareskin", False)
    def test_case_29(self): self.run_case("bareskin", "bare skin", False)
    def test_case_30(self): self.run_case("bold look", "bold look", True)

    def test_case_31(self): self.run_case("bold look", "boldlook", False)
    def test_case_32(self): self.run_case("soft glam", "softglam", False)
    def test_case_33(self): self.run_case(" glam", "glam", True)
    def test_case_34(self): self.run_case("Glam", "glam", True)
    def test_case_35(self): self.run_case("Glam!", "glam", False)

    def test_case_36(self): self.run_case("red carpet", "redcarpet", False)
    def test_case_37(self): self.run_case("red carpet", "red carpet ", True)
    def test_case_38(self): self.run_case("natural", "natural", True)
    def test_case_39(self): self.run_case("Natural", "natural", True)
    def test_case_40(self): self.run_case("glamorous", "glamorous", True)

    def test_case_41(self): self.run_case("glamourous", "glamorous", False)
    def test_case_42(self): self.run_case("no makeup", "nomakeup", False)
    def test_case_43(self): self.run_case("nomakeup", "no makeup", False)
    def test_case_44(self): self.run_case("clean girl", "clean girl", True)
    def test_case_45(self): self.run_case("clean girl", "cleangirl", False)

    def test_case_46(self): self.run_case("  valentine ", "valentine", True)
    def test_case_47(self): self.run_case("valentine", "valentine", True)
    def test_case_48(self): self.run_case("valentines", "valentine", False)
    def test_case_49(self): self.run_case("red carpet", "red carpets", False)
    def test_case_50(self): self.run_case("nude", "nud", False)
