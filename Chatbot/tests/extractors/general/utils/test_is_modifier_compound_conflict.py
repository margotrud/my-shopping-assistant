# tests/extractors/general/utils/test_is_modifier_compound_conflict.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import is_modifier_compound_conflict
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

class TestIsModifierCompoundConflict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()

    def run_case(self, expression, expected):
        result = is_modifier_compound_conflict(expression, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("natural", True)
    def test_case_02(self): self.run_case("romantic", False)
    def test_case_03(self): self.run_case("glamorous", False)
    def test_case_04(self): self.run_case("bare", True)
    def test_case_05(self): self.run_case("bronzed", True)
    def test_case_06(self): self.run_case("dewy", False)
    def test_case_07(self): self.run_case("sparkly", True)
    def test_case_08(self): self.run_case("glowy", True)
    def test_case_09(self): self.run_case("no makeup", False)
    def test_case_10(self): self.run_case("matte", True)

    def test_case_11(self): self.run_case("vibrant", True)
    def test_case_12(self): self.run_case("subtle", True)
    def test_case_13(self): self.run_case("deep", True)
    def test_case_14(self): self.run_case("dark", True)
    def test_case_15(self): self.run_case("daytime", False)
    def test_case_16(self): self.run_case("nude", False)
    def test_case_17(self): self.run_case("soft", True)
    def test_case_18(self): self.run_case("warm", True)
    def test_case_19(self): self.run_case("cool", True)
    def test_case_20(self): self.run_case("bold", True)

    def test_case_21(self): self.run_case("dramatic", False)
    def test_case_22(self): self.run_case("fresh", False)
    def test_case_23(self): self.run_case("office", False)
    def test_case_24(self): self.run_case("casual", False)
    def test_case_25(self): self.run_case("formal", False)
    def test_case_26(self): self.run_case("classic", True)
    def test_case_27(self): self.run_case("neutral", True)
    def test_case_28(self): self.run_case("clean", True)
    def test_case_29(self): self.run_case("satin", True)
    def test_case_30(self): self.run_case("shimmery", True)

    def test_case_31(self): self.run_case("peachy", True)
    def test_case_32(self): self.run_case("rosy", True)
    def test_case_33(self): self.run_case("taupe", False)
    def test_case_34(self): self.run_case("creamy", True)
    def test_case_35(self): self.run_case("barely-there", True)
    def test_case_36(self): self.run_case("elegant", False)
    def test_case_37(self): self.run_case("sparkle", False)
    def test_case_38(self): self.run_case("luminous", True)
    def test_case_39(self): self.run_case("moist", False)
    def test_case_40(self): self.run_case("ultra-deep", False)

    def test_case_41(self): self.run_case("intense", True)
    def test_case_42(self): self.run_case("milky", False)
    def test_case_43(self): self.run_case("rich", True)
    def test_case_44(self): self.run_case("sheer", True)
    def test_case_45(self): self.run_case("icy", True)
    def test_case_46(self): self.run_case("dusty", True)
    def test_case_47(self): self.run_case("creme", False)
    def test_case_48(self): self.run_case("tinted", False)
    def test_case_49(self): self.run_case("naked", False)
    def test_case_50(self): self.run_case("boldness", False)

if __name__ == "__main__":
    unittest.main()
