# tests/extractors/color/logic/expression_matcher/test_apply_expression_context_rules.py

import unittest
from Chatbot.extractors.color.logic.expression_matcher import apply_expression_context_rules
from Chatbot.extractors.color.utils.config_loader import load_expression_context_rules


class TestApplyExpressionContextRules(unittest.TestCase):

    def setUp(self):
        self.context_map = load_expression_context_rules()

    def run_test(self, tokens, matched, expected):
        result = apply_expression_context_rules(tokens, matched, self.context_map)
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_test(["soft", "glowy"], set(), set())
    def test_case_02(self): self.run_test(["bold", "dark"], set(), set())
    def test_case_03(self): self.run_test(["romantic", "rosy"], set(), set())
    def test_case_04(self): self.run_test(["natural", "bare"], set(), set())
    def test_case_05(self): self.run_test(["evening", "plum"], set(), set())

    def test_case_06(self): self.run_test(["bold", "liner"], set(), set())
    def test_case_07(self): self.run_test(["soft", "subtle"], set(), set())
    def test_case_08(self): self.run_test(["natural", "peach"], set(), set())
    def test_case_09(self): self.run_test(["romantic", "pink"], set(), set())
    def test_case_10(self): self.run_test(["evening", "bold"], set(), set())

    def test_case_11(self): self.run_test(["soft", "glowy"], {"soft glam"}, set())
    def test_case_12(self): self.run_test(["bold", "dark"], {"edgy"}, set())
    def test_case_13(self): self.run_test(["romantic", "rosy"], {"romantic"}, set())
    def test_case_14(self): self.run_test(["natural", "bare"], {"natural"}, set())
    def test_case_15(self): self.run_test(["evening", "plum"], {"evening"}, set())

    def test_case_16(self): self.run_test(["soft"], set(), set())
    def test_case_17(self): self.run_test(["glowy"], set(), set())
    def test_case_18(self): self.run_test(["dark"], set(), set())
    def test_case_19(self): self.run_test(["bold"], set(), set())
    def test_case_20(self): self.run_test(["liner"], set(), set())

    def test_case_21(self): self.run_test(["soft", "intense"], set(), set())
    def test_case_22(self): self.run_test(["dramatic", "glowy"], set(), set())
    def test_case_23(self): self.run_test(["romantic", "intense"], set(), set())
    def test_case_24(self): self.run_test(["natural", "clean"], set(), set())
    def test_case_25(self): self.run_test(["evening", "shine"], set(), set())

    def test_case_26(self): self.run_test(["romantic", "rosy", "pink"], set(), set())
    def test_case_27(self): self.run_test(["soft", "peachy", "glowy"], set(), set())
    def test_case_28(self): self.run_test(["bold", "dark", "liner"], set(), set())
    def test_case_29(self): self.run_test(["evening", "plum", "bold"], set(), set())
    def test_case_30(self): self.run_test(["natural", "peach", "bare"], set(), set())

    def test_case_31(self): self.run_test(["bold", "liner"], {"edgy"}, set())
    def test_case_32(self): self.run_test(["soft", "glowy"], {"soft glam"}, set())
    def test_case_33(self): self.run_test(["natural", "peach"], {"natural"}, set())
    def test_case_34(self): self.run_test(["romantic", "rosy"], {"romantic"}, set())
    def test_case_35(self): self.run_test(["evening", "plum"], {"evening"}, set())

    def test_case_36(self): self.run_test([], set(), set())
    def test_case_37(self): self.run_test(["subtle"], set(), set())
    def test_case_38(self): self.run_test(["bare"], set(), set())
    def test_case_39(self): self.run_test(["rosy"], set(), set())
    def test_case_40(self): self.run_test(["peach"], set(), set())

    def test_case_41(self): self.run_test(["intense", "smokey"], set(), set())
    def test_case_42(self): self.run_test(["elegant", "fierce"], set(), set())
    def test_case_43(self): self.run_test(["natural", "rosy", "pink"], set(), set())
    def test_case_44(self): self.run_test(["evening", "dark", "liner"], set(), set())
    def test_case_45(self): self.run_test(["soft", "powdery"], set(), set())

    def test_case_46(self): self.run_test(["glowy", "glamorous", "light"], set(), set())
    def test_case_47(self): self.run_test(["soft", "glowy", "rosy"], {"soft glam"}, set())
    def test_case_48(self): self.run_test(["bold", "liner", "dark"], {"edgy"}, set())
    def test_case_49(self): self.run_test(["natural", "bare", "clean"], {"natural"}, set())
    def test_case_50(self): self.run_test(["evening", "plum", "rosy"], {"evening"}, set())
