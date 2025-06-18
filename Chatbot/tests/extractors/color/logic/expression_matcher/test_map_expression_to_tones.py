import unittest
import json
from Chatbot.extractors.color.logic.expression_matcher import map_expressions_to_tones
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from pathlib import Path


class TestMapExpressionsToTones(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expression_def = load_json_from_data_dir("expression_definition.json")
        data_path = Path(__file__).resolve().parents[0] / "data" / "expected_map_expressions.json"
        with open(data_path, "r", encoding="utf-8") as f:
            cls.expected_map = json.load(f)

    def run_test(self, text: str):
        expected = self.expected_map[text]
        actual = map_expressions_to_tones(text, self.expression_def, known_tones)
        self.assertEqual(expected, actual)

    def test_case_01(self): self.run_test("I like soft glam")

    def test_case_02(self): self.run_test("Show me something edgy")

    def test_case_03(self): self.run_test("What about a natural style?")

    def test_case_04(self): self.run_test("Looking for daytime colors")

    def test_case_05(self): self.run_test("I want something romantic")

    def test_case_06(self): self.run_test("Show me bold makeup")

    def test_case_07(self): self.run_test("Do you have anything subtle?")

    def test_case_08(self): self.run_test("Elegant tones please")

    def test_case_09(self): self.run_test("I prefer something glamorous")

    def test_case_10(self): self.run_test("Evening looks are great")
    def test_case_11(self): self.run_test("Matte glam only")

    def test_case_12(self): self.run_test("Nothing too flashy")

    def test_case_13(self): self.run_test("Give me high fashion looks")

    def test_case_14(self): self.run_test("Work appropriate tones")

    def test_case_15(self): self.run_test("Soft peach shades")

    def test_case_16(self): self.run_test("Subtle and elegant shades")

    def test_case_17(self): self.run_test("Romantic or dramatic options?")

    def test_case_18(self): self.run_test("Neutral evening tone")

    def test_case_19(self): self.run_test("Deep neutral glam")

    def test_case_20(self): self.run_test("Casual everyday tones")

    def test_case_21(self): self.run_test("Bold and edgy mix")

    def test_case_22(self): self.run_test("Dramatic deep look")

    def test_case_23(self): self.run_test("Dark glam look")

    def test_case_24(self): self.run_test("I like refined options")

    def test_case_25(self): self.run_test("Show me something dewy")

    def test_case_26(self): self.run_test("Cool soft tones")

    def test_case_27(self): self.run_test("Warm bold finish")

    def test_case_28(self): self.run_test("Muted glam styles")

    def test_case_29(self): self.run_test("Vibrant glam shades")

    def test_case_30(self): self.run_test("Work-appropriate makeup")

    def test_case_31(self): self.run_test("Party time options")

    def test_case_32(self): self.run_test("A very natural peach")

    def test_case_33(self): self.run_test("Fancy dramatic lipstick")

    def test_case_34(self): self.run_test("Something neutral")

    def test_case_35(self): self.run_test("Heavy glam only")

    def test_case_36(self): self.run_test("I want classy red")

    def test_case_37(self): self.run_test("Soft focus foundation")

    def test_case_38(self): self.run_test("Evening glow")

    def test_case_39(self): self.run_test("Matte and subtle")

    def test_case_40(self): self.run_test("Elegant bold style")

    def test_case_41(self): self.run_test("Nothing at all")

    def test_case_42(self): self.run_test("Just looking")

    def test_case_43(self): self.run_test("Classic everyday glam")

    def test_case_44(self): self.run_test("I want rich glam")

    def test_case_45(self): self.run_test("Formal romantic red")

    def test_case_46(self): self.run_test("Toned down subtle base")

    def test_case_47(self): self.run_test("Neutral base with elegant finish")

    def test_case_48(self): self.run_test("Soft bold pink")

    def test_case_49(self): self.run_test("Minimalist glam")

    def test_case_50(self): self.run_test("Luminous but subtle")
