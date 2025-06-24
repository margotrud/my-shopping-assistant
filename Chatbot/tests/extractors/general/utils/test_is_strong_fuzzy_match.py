# tests/extractors/general/utils/test_is_strong_fuzzy_match.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import is_strong_fuzzy_match, fuzzy_token_match

class TestIsStrongFuzzyMatch(unittest.TestCase):

    def run_case(self, a, b, expected):
        result = is_strong_fuzzy_match(a, b)
        print(f"Expected: {expected} | Actual: {result}")
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("blue", "blue", True)
    def test_case_02(self): self.run_case("Blue", "blue", True)
    def test_case_03(self): self.run_case(" blu", "blue", True)
    def test_case_04(self): self.run_case("blu", "blue", True)
    def test_case_05(self): self.run_case("bluu", "blue", True)

    def test_case_06(self): self.run_case("soft glam", "soft glam", True)
    def test_case_07(self): self.run_case("softglam", "soft glam", True)
    def test_case_08(self): self.run_case("soft glamm", "soft glam", True)
    def test_case_09(self): self.run_case("sof glam", "soft glam", True)
    def test_case_10(self): self.run_case("soft glam", "soft glow", False)

    def test_case_11(self): self.run_case("romantic", "romantic", True)
    def test_case_12(self): self.run_case("romantik", "romantic", True)
    def test_case_13(self): self.run_case("romntic", "romantic", True)
    def test_case_14(self): self.run_case("romantique", "romantic", True)
    def test_case_15(self): self.run_case("romantc", "romantic", True)

    def test_case_16(self): self.run_case("natural", "natural", True)
    def test_case_17(self): self.run_case("natrual", "natural", True)
    def test_case_18(self): self.run_case("natral", "natural", True)
    def test_case_19(self): self.run_case("naturel", "natural", True)
    def test_case_20(self): self.run_case("naturall", "natural", True)

    def test_case_21(self): self.run_case("glamorous", "glamorous", True)
    def test_case_22(self): self.run_case("glamourous", "glamorous", True)
    def test_case_23(self): self.run_case("glamoros", "glamorous", True)
    def test_case_24(self): self.run_case("glams", "glamorous", True)
    def test_case_25(self): self.run_case("glam", "glamorous", True)

    def test_case_26(self): self.run_case("bare skin", "bare skin", True)
    def test_case_27(self): self.run_case("bareskin", "bare skin", True)
    def test_case_28(self): self.run_case("bare skinn", "bare skin", True)
    def test_case_29(self): self.run_case("bare", "bare skin", True)
    def test_case_30(self): self.run_case("bare-skin", "bare skin", True)

    def test_case_31(self): self.run_case("red carpet", "red carpet", True)
    def test_case_32(self): self.run_case("redcarpet", "red carpet", True)
    def test_case_33(self): self.run_case("red carpt", "red carpet", True)
    def test_case_34(self): self.run_case("redd carpet", "red carpet", True)
    def test_case_35(self): self.run_case("red carpeted", "red carpet", True)

    def test_case_36(self): self.run_case("clean girl", "clean girl", True)
    def test_case_37(self): self.run_case("cleangirl", "clean girl", True)
    def test_case_38(self): self.run_case("clean grl", "clean girl", True)
    def test_case_39(self): self.run_case("clean gurl", "clean girl", True)
    def test_case_40(self): self.run_case("clean girll", "clean girl", True)

    def test_case_41(self): self.run_case("no makeup", "no makeup", True)
    def test_case_42(self): self.run_case("nomakeup", "no makeup", True)
    def test_case_43(self): self.run_case("no make up", "no makeup", True)
    def test_case_44(self): self.run_case("makeup", "no makeup", False)
    def test_case_45(self): self.run_case("no makep", "no makeup", True)

    def test_case_46(self): self.run_case("trendy", "trendii", True)
    def test_case_47(self): self.run_case("trendy", "trendyy", True)
    def test_case_48(self): self.run_case("trendy", "trrndy", True)
    def test_case_49(self): self.run_case("trendy", "trend", True)
    def test_case_50(self): self.run_case("trendy", "trendiest", True)
