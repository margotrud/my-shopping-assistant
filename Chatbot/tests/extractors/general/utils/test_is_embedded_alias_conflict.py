# tests/extractors/general/utils/test_is_embedded_alias_conflict.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import is_embedded_alias_conflict

class TestIsEmbeddedAliasConflict(unittest.TestCase):

    def run_case(self, longer, shorter, expected):
        result = is_embedded_alias_conflict(longer, shorter)
        self.assertEqual(result, expected)

    def test_case_01(self): self.run_case("glamorous", "glam", True)
    def test_case_02(self): self.run_case("glow", "glow", False)
    def test_case_03(self): self.run_case("romantic vibe", "romantic", True)
    def test_case_04(self): self.run_case("bare skin", "bare", True)
    def test_case_05(self): self.run_case("bare skin", "bare skin", False)
    def test_case_06(self): self.run_case("natural finish", "natural", True)
    def test_case_07(self): self.run_case("natural", "natural", False)
    def test_case_08(self): self.run_case("hollywood glam", "glam", True)
    def test_case_09(self): self.run_case("valentine", "val", True)
    def test_case_10(self): self.run_case("date night", "date", True)

    def test_case_11(self): self.run_case("night out", "night", True)
    def test_case_12(self): self.run_case("night", "night", False)
    def test_case_13(self): self.run_case("casual chic", "chic", True)
    def test_case_14(self): self.run_case("glitter glam", "glam", True)
    def test_case_15(self): self.run_case("glitter glam", "glitter", True)
    def test_case_16(self): self.run_case("daytime ready", "day", True)
    def test_case_17(self): self.run_case("fresh face", "fresh", True)
    def test_case_18(self): self.run_case("glam", "glamorous", False)
    def test_case_19(self): self.run_case("glamorous", "glamorous", False)
    def test_case_20(self): self.run_case("subtle glow", "subtle", True)

    def test_case_21(self): self.run_case("subtle glow", "glow", True)
    def test_case_22(self): self.run_case("glow up", "glow", True)
    def test_case_23(self): self.run_case("subtle", "subtle", False)
    def test_case_24(self): self.run_case("soft glam", "soft", True)
    def test_case_25(self): self.run_case("soft glam", "glam", True)
    def test_case_26(self): self.run_case("no makeup", "makeup", True)
    def test_case_27(self): self.run_case("no makeup", "no", True)
    def test_case_28(self): self.run_case("red carpet", "carpet", True)
    def test_case_29(self): self.run_case("red carpet", "red", True)
    def test_case_30(self): self.run_case("edgy vibe", "edgy", True)

    def test_case_31(self): self.run_case("sparkle glam", "sparkle", True)
    def test_case_32(self): self.run_case("sparkle glam", "spark", True)
    def test_case_33(self): self.run_case("elegant touch", "touch", True)
    def test_case_34(self): self.run_case("elegant touch", "elegant", True)
    def test_case_35(self): self.run_case("daily wear", "wear", True)
    def test_case_36(self): self.run_case("wear", "wear", False)
    def test_case_37(self): self.run_case("office ready", "office", True)
    def test_case_38(self): self.run_case("soft sparkle", "spark", True)
    def test_case_39(self): self.run_case("bold red", "bold", True)
    def test_case_40(self): self.run_case("bold red", "red", True)

    def test_case_41(self): self.run_case("clean glam", "clean", True)
    def test_case_42(self): self.run_case("glam clean", "clean", True)
    def test_case_43(self): self.run_case("glam clean", "glam", True)
    def test_case_44(self): self.run_case("glam clean", "am", True)
    def test_case_45(self): self.run_case("chic and glam", "chic", True)
    def test_case_46(self): self.run_case("chic and glam", "and", True)
    def test_case_47(self): self.run_case("chic and glam", "glam", True)
    def test_case_48(self): self.run_case("glam", "gla", True)
    def test_case_49(self): self.run_case("glam", "gl", True)
    def test_case_50(self): self.run_case("glam", "am", True)

if __name__ == "__main__":
    unittest.main()
