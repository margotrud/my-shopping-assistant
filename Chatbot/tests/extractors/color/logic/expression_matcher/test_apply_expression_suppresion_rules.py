# tests/extractors/color/logic/expression_matcher/test_apply_expression_suppression_rules.py

import unittest
from Chatbot.extractors.color.logic.expression_matcher import apply_expression_suppression_rules
from Chatbot.extractors.color.shared.constants import EXPRESSION_SUPPRESSION_RULES

class TestApplyExpressionSuppressionRules(unittest.TestCase):

    def run_test(self, matched, expected):
        result = apply_expression_suppression_rules(matched)
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_test(set(), set())
    def test_case_02(self): self.run_test({"natural"}, {"natural"})
    def test_case_03(self): self.run_test({"glamorous"}, {"glamorous"})
    def test_case_04(self): self.run_test({"daytime"}, {"daytime"})
    def test_case_05(self): self.run_test({"glamorous", "natural"}, {"glamorous"})
    def test_case_06(self): self.run_test({"glamorous", "daytime"}, {"glamorous"})
    def test_case_07(self): self.run_test({"glamorous", "daytime", "natural"}, {"glamorous"})
    def test_case_08(self): self.run_test({"romantic", "edgy"}, {"edgy"})
    def test_case_09(self): self.run_test({"soft glam", "edgy"}, {"edgy"})
    def test_case_10(self): self.run_test({"edgy", "romantic", "soft glam"}, {"edgy"})

    def test_case_11(self): self.run_test({"edgy", "romantic"}, {"edgy"})
    def test_case_12(self): self.run_test({"edgy", "soft glam"}, {"edgy"})
    def test_case_13(self): self.run_test({"romantic", "soft glam"}, {"romantic", "soft glam"})
    def test_case_14(self): self.run_test({"edgy", "glamorous"}, {"edgy", "glamorous"})
    def test_case_15(self): self.run_test({"glamorous", "natural", "bold"}, {"glamorous", "bold"})
    def test_case_16(self): self.run_test({"glamorous", "neutral", "daytime"}, {"neutral", "glamorous"})
    def test_case_17(self): self.run_test({"glamorous", "edgy", "daytime"}, {"glamorous", "edgy"})
    def test_case_18(self): self.run_test({"daytime", "neutral"}, {"daytime", "neutral"})
    def test_case_19(self): self.run_test({"bold", "subtle"}, {"bold"})
    def test_case_20(self): self.run_test({"subtle", "neutral"}, {"subtle", "neutral"})

    def test_case_21(self): self.run_test({"bold", "neutral"}, {"bold"})
    def test_case_22(self): self.run_test({"neutral", "natural"}, {"neutral", "natural"})
    def test_case_23(self): self.run_test({"neutral", "natural", "glamorous"}, {"glamorous", "neutral"})
    def test_case_24(self): self.run_test({"daytime", "bold", "natural"}, {"natural", "daytime", "bold"})
    def test_case_25(self): self.run_test({"daytime", "natural", "subtle"}, {"daytime", "subtle", "natural"})

    def test_case_26(self): self.run_test({"glamorous", "romantic"}, {"glamorous", "romantic"})
    def test_case_27(self): self.run_test({"glamorous", "soft glam", "daytime"}, {"glamorous", "soft glam"})
    def test_case_28(self): self.run_test({"glamorous", "neutral", "natural"}, {"glamorous", "neutral"})
    def test_case_29(self): self.run_test({"subtle", "bold", "daytime"}, {"daytime","bold"})
    def test_case_30(self): self.run_test({"neutral", "bold", "glamorous", "daytime"}, {"bold", "glamorous"})

    def test_case_31(self): self.run_test({"soft glam", "neutral"}, {"soft glam", "neutral"})
    def test_case_32(self): self.run_test({"natural", "neutral"}, {"natural", "neutral"})
    def test_case_33(self): self.run_test({"glamorous", "natural", "edgy"}, {"glamorous", "edgy"})
    def test_case_34(self): self.run_test({"subtle", "neutral", "romantic"}, {"subtle", "neutral", "romantic"})
    def test_case_35(self): self.run_test({"glamorous", "daytime", "natural", "neutral"}, {"glamorous", "neutral"})

    def test_case_36(self): self.run_test({"daytime", "natural", "bold", "neutral"}, {"daytime", "natural", "bold"})
    def test_case_37(self): self.run_test({"natural", "subtle", "romantic"}, {"natural", "subtle", "romantic"})
    def test_case_38(self): self.run_test({"bold", "neutral", "glamorous"}, {"bold", "glamorous"})
    def test_case_39(self): self.run_test({"neutral", "subtle", "glamorous"}, {"subtle","glamorous", "neutral"})
    def test_case_40(self): self.run_test({"natural", "daytime", "neutral", "subtle"}, {'daytime', 'subtle', 'natural', 'neutral'})

    def test_case_41(self): self.run_test({"natural", "neutral", "daytime", "romantic"}, {'daytime', 'neutral', 'natural', 'romantic'})
    def test_case_42(self): self.run_test({"neutral", "glamorous", "edgy", "daytime"}, {"neutral", "glamorous", "edgy"})
    def test_case_43(self): self.run_test({"daytime", "glamorous", "natural", "bold"}, {"glamorous", "bold"})
    def test_case_44(self): self.run_test({"bold", "glamorous", "subtle", "natural"}, {"bold", "glamorous"})
    def test_case_45(self): self.run_test({"glamorous", "subtle", "romantic"}, {"glamorous", "subtle", "romantic"})

    def test_case_46(self): self.run_test({"daytime", "glamorous", "romantic"}, {"glamorous", "romantic"})
    def test_case_47(self): self.run_test({"glamorous", "natural", "neutral", "romantic"}, {"glamorous", "neutral", "romantic"})
    def test_case_48(self): self.run_test({"bold", "subtle", "neutral"}, {"bold"})
    def test_case_49(self): self.run_test({"bold", "glamorous", "natural", "neutral", "daytime"}, {"bold", "glamorous"})
    def test_case_50(self): self.run_test({"glamorous", "natural", "daytime", "neutral", "romantic", "subtle"}, {"glamorous", "neutral", "romantic", "subtle"})
