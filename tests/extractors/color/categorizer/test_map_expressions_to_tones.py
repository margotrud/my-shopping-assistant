import unittest
import json
from pathlib import Path
from typing import List
from Chatbot.extractors.color.extract.categorizer import map_expressions_to_tones

class TestMapExpressionsToTones(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).resolve().parents[4] / "Data"
        with open(data_path / "expression_triggers.json", "r", encoding="utf-8") as f:
            cls.trigger_map = json.load(f)
        # known_tones should be all tones used in your products
        with open(data_path / "expression_aliases.json", "r", encoding="utf-8") as f:
            alias_map = json.load(f)
        cls.known_tones = set(tone for tones in alias_map.values() for tone in tones)

    def run_case(self, input_text: str, expected_expressions: List[str]):
        expected = {}
        for expr in expected_expressions:
            keywords = self.trigger_map[expr]
            expected[expr] = sorted([
                tone for tone in self.known_tones if any(k in tone for k in keywords)
            ])
        result = map_expressions_to_tones(input_text, self.trigger_map, self.known_tones)
        result = {k: sorted(v) for k, v in result.items()}
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("soft", ["natural"])
    def test_case_02(self): self.run_case("blush", ["romantic"])
    def test_case_03(self): self.run_case("vibrant tone", ["bold"])
    def test_case_04(self): self.run_case("subtle glow", ["fresh", "natural"])
    def test_case_05(self): self.run_case("natural and neutral", ["natural"])
    def test_case_06(self): self.run_case("rosy cheeks", ["romantic"])
    def test_case_07(self): self.run_case("bright and bold", ["bold"])
    def test_case_08(self): self.run_case("dewy and peachy", ["bronzed", "fresh"])
    def test_case_09(self): self.run_case("muted tones", ["natural"])
    def test_case_10(self): self.run_case("lovely finish", ["romantic"])
    def test_case_11(self): self.run_case("luminous look", ["soft glam"])
    def test_case_12(self): self.run_case("intense pop", ["bold"])
    def test_case_13(self): self.run_case("radiant shimmer", ["fresh"])
    def test_case_14(self): self.run_case("fresh face", ["fresh", "no makeup"])
    def test_case_15(self): self.run_case("warm undertones", ["bronzed", "fresh", "natural"])
    def test_case_16(self): self.run_case("bold vibrant", ["bold"])
    def test_case_17(self): self.run_case("natural glow", ["natural", "fresh"])
    def test_case_18(self): self.run_case("blush pink", ["romantic"])
    def test_case_19(self): self.run_case("minimal and soft", ["natural", "no makeup", ])
    def test_case_20(self): self.run_case("subtle elegance", ["elegant", "natural"])
    def test_case_21(self): self.run_case("romantic mood", ["romantic"])
    def test_case_22(self): self.run_case("subtle warm glow", ["bronzed", "fresh", "natural"])
    def test_case_23(self): self.run_case("peachy bronze", ["bronzed", "fresh"])
    def test_case_24(self): self.run_case("bold blush glam", ["bold", "glamorous", "romantic"])
    def test_case_25(self): self.run_case("understated fresh", ["fresh", "natural", "no makeup"])
    def test_case_26(self): self.run_case("soft glam look", ["natural", "soft glam"])
    def test_case_27(self): self.run_case("glow and blush", ["fresh", "romantic"])
    def test_case_28(self): self.run_case("natural subtle blush", ["natural", "romantic"])
    def test_case_29(self): self.run_case("dewy romantic", ["fresh", "romantic"])
    def test_case_30(self): self.run_case("bright intense glam", ["bold", "glamorous"])
    def test_case_31(self): self.run_case("fresh and radiant", ["fresh", "no makeup"])
    def test_case_32(self): self.run_case("soft glam and blush", ["natural", "romantic", "soft glam"])
    def test_case_33(self): self.run_case("bold bright romantic", ["bold", "romantic"])
    def test_case_34(self): self.run_case("subtle soft glow", ["fresh", "natural"])
    def test_case_35(self): self.run_case("peachy and lovely", ["bronzed", "fresh", "romantic"])
    def test_case_36(self): self.run_case("light warm tones", ["bronzed", "daytime", "fresh"])
    def test_case_37(self): self.run_case("natural romantic glam", ["natural", "romantic", "soft glam"])
    def test_case_38(self): self.run_case("blush and bronze", ["bronzed", "romantic"])
    def test_case_39(self): self.run_case("glow glam", ["fresh", "glamorous"])
    def test_case_40(self): self.run_case("bold soft neutral", ["bold", "natural"])
    def test_case_41(self): self.run_case("peachy subtle blush glow", ["bronzed", "fresh", "natural", "romantic"])
    def test_case_42(self): self.run_case("romantic warm radiant", ["bronzed", "fresh", "romantic"])
    def test_case_43(self): self.run_case("natural light glow", ["daytime", "fresh", "natural"])
    def test_case_44(self): self.run_case("dewy soft subtle", ["fresh", "natural"])
    def test_case_45(self): self.run_case("blush pink glam", ["glamorous", "romantic"])
    def test_case_46(self): self.run_case("intense glow blush", ["bold", "fresh", "romantic"])
    def test_case_47(self): self.run_case("muted subtle tones", ["natural"])
    def test_case_48(self): self.run_case("romantic minimal look", ["natural", "no makeup", "romantic"])
    def test_case_49(self): self.run_case("bold romantic glow", ["bold", "romantic", "fresh"])
    def test_case_50(self): self.run_case("natural soft dewy peachy warm radiant glow", ["bronzed", "fresh", "natural"])

if __name__ == "__main__":
    unittest.main()
