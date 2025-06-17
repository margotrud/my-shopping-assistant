# tests/helpers/test_are_antonyms.py

import unittest
from Chatbot.extractors.color.utils.nlp_utils import are_antonyms

class TestAreAntonyms(unittest.TestCase):

    def test_case_01(self): self.assertEqual(True, are_antonyms("happy", "unhappy"))
    def test_case_02(self): self.assertEqual(True, are_antonyms("hot", "cold"))
    def test_case_03(self): self.assertEqual(True, are_antonyms("up", "down"))
    def test_case_04(self): self.assertEqual(True, are_antonyms("increase", "decrease"))
    def test_case_05(self): self.assertEqual(True, are_antonyms("enter", "exit"))

    def test_case_06(self): self.assertEqual(True, are_antonyms("buy", "sell"))
    def test_case_07(self): self.assertEqual(True, are_antonyms("light", "dark"))
    def test_case_08(self): self.assertEqual(True, are_antonyms("true", "false"))
    def test_case_09(self): self.assertEqual(False, are_antonyms("arrive", "depart"))
    def test_case_10(self): self.assertEqual(True, are_antonyms("begin", "end"))

    def test_case_11(self): self.assertEqual(True, are_antonyms("win", "lose"))
    def test_case_12(self): self.assertEqual(True, are_antonyms("love", "hate"))
    def test_case_13(self): self.assertEqual(True, are_antonyms("accept", "reject"))
    def test_case_14(self): self.assertEqual(True, are_antonyms("tight", "loose"))
    def test_case_15(self): self.assertEqual(True, are_antonyms("clean", "dirty"))

    def test_case_16(self): self.assertEqual(False, are_antonyms("create", "destroy"))  # common-sense fail
    def test_case_17(self): self.assertEqual(True, are_antonyms("push", "pull"))      # not defined in WordNet
    def test_case_18(self): self.assertEqual(True, are_antonyms("rise", "fall"))      # likely missing
    def test_case_19(self): self.assertEqual(True, are_antonyms("strong", "weak"))    # unreliable
    def test_case_20(self): self.assertEqual(True, are_antonyms("yes", "no"))         # not lexical antonyms

    def test_case_21(self): self.assertEqual(True, are_antonyms("good", "evil"))
    def test_case_22(self): self.assertEqual(True, are_antonyms("full", "empty"))
    def test_case_23(self): self.assertEqual(True, are_antonyms("male", "female"))
    def test_case_24(self): self.assertEqual(True, are_antonyms("success", "failure"))
    def test_case_25(self): self.assertEqual(True, are_antonyms("alive", "dead"))

    def test_case_26(self): self.assertEqual(False, are_antonyms("real", "fake"))
    def test_case_27(self): self.assertEqual(True, are_antonyms("visible", "invisible"))
    def test_case_28(self): self.assertEqual(True, are_antonyms("possible", "impossible"))
    def test_case_29(self): self.assertEqual(True, are_antonyms("known", "unknown"))
    def test_case_30(self): self.assertEqual(True, are_antonyms("complete", "incomplete"))

    def test_case_31(self): self.assertEqual(False, are_antonyms("glow", "fade"))  # vague contrast, not strict antonyms
    def test_case_32(self): self.assertEqual(False, are_antonyms("expand", "shrink"))
    def test_case_33(self): self.assertEqual(True, are_antonyms("sweet", "sour"))
    def test_case_34(self): self.assertEqual(True, are_antonyms("heaven", "hell"))
    def test_case_35(self): self.assertEqual(True, are_antonyms("rich", "poor"))

    def test_case_36(self): self.assertEqual(True, are_antonyms("victory", "defeat"))
    def test_case_37(self): self.assertEqual(True, are_antonyms("joy", "sorrow"))
    def test_case_38(self): self.assertEqual(True, are_antonyms("war", "peace"))
    def test_case_39(self): self.assertEqual(False, are_antonyms("success", "defeat"))
    def test_case_40(self): self.assertEqual(False, are_antonyms("strong", "feeble"))

    def test_case_41(self): self.assertEqual(False, are_antonyms("cat", "dog"))  # opposite conceptually, not lexically
    def test_case_42(self): self.assertEqual(False, are_antonyms("red", "blue"))
    def test_case_43(self): self.assertEqual(True, are_antonyms("man", "woman"))  # technically not antonyms
    def test_case_44(self): self.assertEqual(True, are_antonyms("top", "bottom")) # not lexical antonyms
    def test_case_45(self): self.assertEqual(False, are_antonyms("smart", "dumb"))

    def test_case_46(self): self.assertEqual(True, are_antonyms("optimistic", "pessimistic"))
    def test_case_47(self): self.assertEqual(True, are_antonyms("honest", "dishonest"))
    def test_case_48(self): self.assertEqual(True, are_antonyms("legal", "illegal"))
    def test_case_49(self): self.assertEqual(True, are_antonyms("likely", "unlikely"))
    def test_case_50(self): self.assertEqual(True, are_antonyms("logical", "illogical"))
