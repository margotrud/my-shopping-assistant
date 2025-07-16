# tests/extractors/general/utils/test_should_accept_multiword_alias.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import should_accept_multiword_alias

class TestShouldAcceptMultiwordAlias(unittest.TestCase):

    def run_case(self, alias, input_text, expected):
        result = should_accept_multiword_alias(alias, input_text)
        print(f"Expected: {expected} | Actual: {result}")
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("bare skin", "bare skin", True)
    def test_case_02(self): self.run_case("bare skin", "i like bare skin", True)
    def test_case_03(self): self.run_case("bare skin", "bare skin finish", True)
    def test_case_04(self): self.run_case("bare skin", "bare skinn", True)
    def test_case_05(self): self.run_case("bare skin", "i want that bare skin look", True)

    def test_case_06(self): self.run_case("red carpet", "red carpet", True)
    def test_case_07(self): self.run_case("red carpet", "like red carpet look", True)
    def test_case_08(self): self.run_case("red carpet", "red carpet vibe", True)
    def test_case_09(self): self.run_case("red carpet", "red carpets are cool", True)
    def test_case_10(self): self.run_case("red carpet", "red carpt look", True)

    def test_case_11(self): self.run_case("valentine date", "valentine date", True)
    def test_case_12(self): self.run_case("valentine date", "valentine date night", True)
    def test_case_13(self): self.run_case("valentine date", "on a valentine date", True)
    def test_case_14(self): self.run_case("valentine date", "valentin date", True)
    def test_case_15(self): self.run_case("valentine date", "valentime date night", True)

    def test_case_16(self): self.run_case("date night", "for a date night", True)
    def test_case_17(self): self.run_case("date night", "date night vibe", True)
    def test_case_18(self): self.run_case("date night", "soft date night glam", True)
    def test_case_19(self): self.run_case("date night", "d8 night look", False)
    def test_case_20(self): self.run_case("date night", "night date", True)

    def test_case_21(self): self.run_case("work appropriate", "work appropriate", True)
    def test_case_22(self): self.run_case("work appropriate", "something more work appropriate", True)
    def test_case_23(self): self.run_case("work appropriate", "maybe work approrpiate?", True)
    def test_case_24(self): self.run_case("work appropriate", "for work appropriateness", True)
    def test_case_25(self): self.run_case("work appropriate", "need office vibe", False)

    def test_case_26(self): self.run_case("soft glam", "soft glam", True)
    def test_case_27(self): self.run_case("soft glam", "i love soft glam", True)
    def test_case_28(self): self.run_case("soft glam", "sof glam", True)
    def test_case_29(self): self.run_case("soft glam", "softglam", True)
    def test_case_30(self): self.run_case("soft glam", "soft glamm", True)

    def test_case_31(self): self.run_case("glowy finish", "i want glowy finish", True)
    def test_case_32(self): self.run_case("glowy finish", "glowy finsih", True)
    def test_case_33(self): self.run_case("glowy finish", "something that gives a glowy finish", True)
    def test_case_34(self): self.run_case("glowy finish", "glowy end result", False)
    def test_case_35(self): self.run_case("glowy finish", "glowy glow", False)

    def test_case_36(self): self.run_case("clean girl", "clean girl", True)
    def test_case_37(self): self.run_case("clean girl", "clean girll look", True)
    def test_case_38(self): self.run_case("clean girl", "looking for a clean girl vibe", True)
    def test_case_39(self): self.run_case("clean girl", "girl clean aesthetic", True)
    def test_case_40(self): self.run_case("clean girl", "just clean", False)

    def test_case_41(self): self.run_case("natural glow", "natural glow", True)
    def test_case_42(self): self.run_case("natural glow", "looking for natural glow", True)
    def test_case_43(self): self.run_case("natural glow", "natrual glow", True)
    def test_case_44(self): self.run_case("natural glow", "natrl glow", True)
    def test_case_45(self): self.run_case("natural glow", "natural gloss", True)

    def test_case_46(self): self.run_case("even tone", "even tone", True)
    def test_case_47(self): self.run_case("even tone", "even tone coverage", True)
    def test_case_48(self): self.run_case("even tone", "even toned skin", True)
    def test_case_49(self): self.run_case("even tone", "evening tone", False)
    def test_case_50(self): self.run_case("even tone", "tone even", True)
