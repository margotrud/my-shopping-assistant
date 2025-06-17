# tests/helpers/test_fuzzy_match_modifier.py

import unittest
from Chatbot.extractors.color.utils.modifier_resolution import fuzzy_match_modifier

class TestFuzzyMatchModifier(unittest.TestCase):

    def test_case_01(self): self.assertEqual(True, fuzzy_match_modifier("soft", "soft"))
    def test_case_02(self): self.assertEqual(True, fuzzy_match_modifier("bold", "bold"))
    def test_case_03(self): self.assertEqual(True, fuzzy_match_modifier("bare", "bare"))
    def test_case_04(self): self.assertEqual(True, fuzzy_match_modifier("nude", "nude"))
    def test_case_05(self): self.assertEqual(False, fuzzy_match_modifier("soft", "bold"))
    def test_case_06(self): self.assertEqual(True, fuzzy_match_modifier("sof", "soft"))
    def test_case_07(self): self.assertEqual(True, fuzzy_match_modifier("sooft", "soft"))
    def test_case_08(self): self.assertEqual(True, fuzzy_match_modifier("natral", "natural"))
    def test_case_09(self): self.assertEqual(True, fuzzy_match_modifier("glosy", "glossy"))
    def test_case_10(self): self.assertEqual(False, fuzzy_match_modifier("wrong", "bare"))

    def test_case_11(self): self.assertEqual(True, fuzzy_match_modifier("cooly", "cool"))
    def test_case_12(self): self.assertEqual(True, fuzzy_match_modifier("naturly", "natural"))
    def test_case_13(self): self.assertEqual(True, fuzzy_match_modifier("glosse", "glossy"))
    def test_case_14(self): self.assertEqual(False, fuzzy_match_modifier("fire", "bare"))
    def test_case_15(self): self.assertEqual(True, fuzzy_match_modifier("cleany", "clean"))
    def test_case_16(self): self.assertEqual(True, fuzzy_match_modifier("softy", "soft"))
    def test_case_17(self): self.assertEqual(True, fuzzy_match_modifier("brght", "bright"))
    def test_case_18(self): self.assertEqual(False, fuzzy_match_modifier("barely", "bare", threshold=90))
    def test_case_19(self): self.assertEqual(True, fuzzy_match_modifier("barely", "bare", threshold=70))
    def test_case_20(self): self.assertEqual(True, fuzzy_match_modifier("cold", "cool"))

    def test_case_21(self): self.assertEqual(True, fuzzy_match_modifier("glssy", "glossy", threshold=75))
    def test_case_22(self): self.assertEqual(True, fuzzy_match_modifier("cleen", "clean"))
    def test_case_23(self): self.assertEqual(False, fuzzy_match_modifier("glow", "glossy"))
    def test_case_24(self): self.assertEqual(True, fuzzy_match_modifier("sofft", "soft"))
    def test_case_25(self): self.assertEqual(True, fuzzy_match_modifier("smoth", "smooth"))
    def test_case_26(self): self.assertEqual(False, fuzzy_match_modifier("neon", "natural"))
    def test_case_27(self): self.assertEqual(True, fuzzy_match_modifier("blod", "bold"))
    def test_case_28(self): self.assertEqual(False, fuzzy_match_modifier("bald", "bold", threshold=90))
    def test_case_29(self): self.assertEqual(True, fuzzy_match_modifier("bald", "bold", threshold=70))
    def test_case_30(self): self.assertEqual(False, fuzzy_match_modifier("red", "bold"))

    def test_case_31(self): self.assertEqual(False, fuzzy_match_modifier("breezy", "bare"))
    def test_case_32(self): self.assertEqual(False, fuzzy_match_modifier("bar", "bare", threshold=90))
    def test_case_33(self): self.assertEqual(True, fuzzy_match_modifier("bar", "bare", threshold=70))
    def test_case_34(self): self.assertEqual(True, fuzzy_match_modifier("gliss", "gloss"))
    def test_case_35(self): self.assertEqual(True, fuzzy_match_modifier("glosse", "glossy", threshold=80))
    def test_case_36(self): self.assertEqual(False, fuzzy_match_modifier("green", "clean"))
    def test_case_37(self): self.assertEqual(True, fuzzy_match_modifier("nud", "nude"))
    def test_case_38(self): self.assertEqual(False, fuzzy_match_modifier("newd", "nude", threshold=90))
    def test_case_39(self): self.assertEqual(False, fuzzy_match_modifier("newd", "nude", threshold=70))
    def test_case_40(self): self.assertEqual(False, fuzzy_match_modifier("milk", "bare"))

    def test_case_41(self): self.assertEqual(True, fuzzy_match_modifier("wram", "warm"))
    def test_case_42(self): self.assertEqual(True, fuzzy_match_modifier("col", "cool"))
    def test_case_43(self): self.assertEqual(False, fuzzy_match_modifier("deep", "soft"))
    def test_case_44(self): self.assertEqual(True, fuzzy_match_modifier("naturl", "natural"))
    def test_case_45(self): self.assertEqual(False, fuzzy_match_modifier("gold", "bold", threshold=90))
    def test_case_46(self): self.assertEqual(True, fuzzy_match_modifier("gold", "bold", threshold=70))
    def test_case_47(self): self.assertEqual(False, fuzzy_match_modifier("shine", "soft"))
    def test_case_48(self): self.assertEqual(True, fuzzy_match_modifier("soofty", "soft"))
    def test_case_49(self): self.assertEqual(False, fuzzy_match_modifier("xxx", "bare"))
    def test_case_50(self): self.assertEqual(False, fuzzy_match_modifier("nat", "natural", threshold=65))


if __name__ == "__main__":
    unittest.main()
