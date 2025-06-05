# tests/extractors/color/test_find_matching_expressions.py

import unittest
from pathlib import Path
import json

from Chatbot.extractors.color.extract.categorizer import find_matching_expressions

class TestFindMatchingExpressions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).resolve().parents[4]/ "Data" / "expression_triggers.json"
        with open(data_path, "r", encoding="utf-8") as f:
            cls.trigger_map = json.load(f)

    def test_case_01(self):
        self.assertEqual(["natural"], find_matching_expressions("I love neutral tones", self.trigger_map))

    def test_case_02(self):
        self.assertEqual(["bold"], find_matching_expressions("Go for something bold", self.trigger_map))

    def test_case_03(self):
        self.assertEqual(["romantic"], find_matching_expressions("A romantic vibe maybe", self.trigger_map))

    def test_case_04(self):
        self.assertEqual(["fresh", "no makeup"], find_matching_expressions("Give me a fresh look", self.trigger_map))

    def test_case_05(self):
        self.assertEqual(["daytime", "fresh"], find_matching_expressions("light shades", self.trigger_map))

    def test_case_06(self):
        self.assertEqual(["bold"], find_matching_expressions("intense colors", self.trigger_map))

    def test_case_07(self):
        self.assertEqual(["romantic"], find_matching_expressions("rosy cheeks", self.trigger_map))

    def test_case_08(self):
        self.assertEqual(["bronzed", "fresh"], find_matching_expressions("peachy glow", self.trigger_map))

    def test_case_09(self):
        self.assertEqual(['bold', 'daytime', 'fresh'], find_matching_expressions("light but bold makeup", self.trigger_map))

    def test_case_10(self):
        self.assertEqual(["natural", "romantic"], find_matching_expressions("soft and rosy tones", self.trigger_map))

    def test_case_11(self):
        self.assertEqual(["bold", "romantic"], find_matching_expressions("blush with a bold touch", self.trigger_map))

    def test_case_12(self):
        self.assertEqual(["natural"], find_matching_expressions("natural shades please", self.trigger_map))

    def test_case_13(self):
        self.assertEqual(["romantic"], find_matching_expressions("something lovely and delicate", self.trigger_map))

    def test_case_14(self):
        self.assertEqual(["bold"], find_matching_expressions("something really vibrant and strong", self.trigger_map))

    def test_case_15(self):
        self.assertEqual(["natural", "romantic"], find_matching_expressions("soft blush tones", self.trigger_map))

    def test_case_16(self):
        self.assertEqual(["bold", "fresh"], find_matching_expressions("vibrant peach combo", self.trigger_map))

    def test_case_17(self):
        self.assertEqual(["fresh"], find_matching_expressions("dewy peach", self.trigger_map))

    def test_case_18(self):
        self.assertEqual(["natural", "no makeup"], find_matching_expressions("muted colors are best", self.trigger_map))

    def test_case_19(self):
        self.assertEqual(["bold", "romantic"], find_matching_expressions("bright and rosy lips", self.trigger_map))

    def test_case_20(self):
        self.assertEqual(['bold', 'natural', 'romantic'],
                         find_matching_expressions("soft bright blush", self.trigger_map))

    def test_case_21(self):
        self.assertEqual(["bold"], find_matching_expressions("go for brightness", self.trigger_map))

    def test_case_22(self):
        self.assertEqual(['daytime', 'fresh', 'natural', 'no makeup'], find_matching_expressions("minimal and light", self.trigger_map))

    def test_case_23(self):
        self.assertEqual(["romantic"], find_matching_expressions("blushy tones", self.trigger_map))

    def test_case_24(self):
        self.assertEqual(["bronzed", "fresh"], find_matching_expressions("a warm sunny look", self.trigger_map))

    def test_case_25(self):
        self.assertEqual(['evening', 'romantic'], find_matching_expressions("a lovely date night look", self.trigger_map))

    def test_case_26(self):
        self.assertEqual(['bronzed', 'fresh', 'natural'] , find_matching_expressions("natural and warm shades", self.trigger_map))

    def test_case_27(self):
        self.assertEqual(['bold', 'natural'], find_matching_expressions("soft and vibrant look", self.trigger_map))

    def test_case_28(self):
        self.assertEqual(["bronzed", "fresh"], find_matching_expressions("peachy sun tones", self.trigger_map))

    def test_case_29(self):
        self.assertEqual(["bold", "natural"], find_matching_expressions("bright but muted", self.trigger_map))

    def test_case_30(self):
        self.assertEqual(["romantic"], find_matching_expressions("blush and more blush", self.trigger_map))

    def test_case_31(self):
        self.assertEqual(["natural"], find_matching_expressions("subtle and soft", self.trigger_map))

    def test_case_32(self):
        self.assertEqual(["bronzed", "fresh", "romantic"], find_matching_expressions("peachy blush", self.trigger_map))

    def test_case_33(self):
        self.assertEqual(["bold", "glamorous"], find_matching_expressions("intensity and drama", self.trigger_map))

    def test_case_34(self):
        self.assertEqual(["natural"], find_matching_expressions("something understated", self.trigger_map))

    def test_case_35(self):
        self.assertEqual(["elegant", "romantic"], find_matching_expressions("rosy elegance", self.trigger_map))

    def test_case_36(self):
        self.assertEqual(['bronzed', 'fresh'], find_matching_expressions("sun-kissed glow", self.trigger_map))

    def test_case_37(self):
        self.assertEqual(["bold"], find_matching_expressions("a bit of vibrance", self.trigger_map))

    def test_case_38(self):
        self.assertEqual(['bronzed', 'fresh', 'romantic'], find_matching_expressions("rosy warm tone", self.trigger_map))

    def test_case_39(self):
        self.assertEqual(['daytime', 'fresh'], find_matching_expressions("light and easygoing", self.trigger_map))

    def test_case_40(self):
        self.assertEqual(["bold"], find_matching_expressions("bright and proud", self.trigger_map))

    def test_case_41(self):
        self.assertEqual(["fresh", "no makeup"], find_matching_expressions("fresh vibe please", self.trigger_map))

    def test_case_42(self):
        self.assertEqual(["romantic"], find_matching_expressions("romantic hues", self.trigger_map))

    def test_case_43(self):
        self.assertEqual(["natural", "romantic"], find_matching_expressions("natural blush", self.trigger_map))

    def test_case_44(self):
        self.assertEqual(["daytime","fresh"], find_matching_expressions("dewy light makeup", self.trigger_map))

    def test_case_45(self):
        self.assertEqual(["bold", "romantic"], find_matching_expressions("rosy and bright lips", self.trigger_map))

    def test_case_46(self):
        self.assertEqual(['daytime', 'fresh', 'natural', 'soft glam'], find_matching_expressions("light glam, soft finish", self.trigger_map))

    def test_case_47(self):
        self.assertEqual(["bold"], find_matching_expressions("intense coral pop", self.trigger_map))

    def test_case_48(self):
        self.assertEqual(["romantic"], find_matching_expressions("lovely charming tones", self.trigger_map))

    def test_case_49(self):
        self.assertEqual(['bold', 'bronzed', 'fresh'], find_matching_expressions("warm vibrant energy", self.trigger_map))

    def test_case_50(self):
        self.assertEqual(['bold', 'fresh', 'natural', 'romantic'],
                         find_matching_expressions("soft rosy bright glow", self.trigger_map))

    if __name__ == "__main__":
        unittest.main()

if __name__ == "__main__":
    unittest.main()
