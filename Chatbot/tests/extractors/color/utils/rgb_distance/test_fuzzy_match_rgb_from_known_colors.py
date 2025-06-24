# Chatbot/tests/extractors/color/utils/test_fuzzy_match_rgb_from_known_colors.py

import unittest
import webcolors
from Chatbot.extractors.color.utils.rgb_distance import fuzzy_match_rgb_from_known_colors
from Chatbot.extractors.color.shared.vocab import all_webcolor_names

known_rgb_map = {name: webcolors.name_to_rgb(name) for name in all_webcolor_names}

class TestFuzzyMatchRgbFromKnownColors(unittest.TestCase):

    def run_case(self, phrase, expected_rgb):
        result_name = fuzzy_match_rgb_from_known_colors(phrase)
        result_rgb = webcolors.name_to_rgb(result_name) if result_name else None
        self.assertEqual(expected_rgb, result_rgb, msg=f"\nExpected : {expected_rgb}\nActual   : {result_rgb}")

    def test_case_01(self): self.run_case("white", (255, 255, 255))
    def test_case_02(self): self.run_case("black", (0, 0, 0))
    def test_case_03(self): self.run_case("red", (255, 0, 0))
    def test_case_04(self): self.run_case("blue", (0, 0, 255))
    def test_case_05(self): self.run_case("green", (0, 128, 0))

    def test_case_06(self): self.run_case("yellow", (255, 255, 0))
    def test_case_07(self): self.run_case("orange", (255, 165, 0))
    def test_case_08(self): self.run_case("purple", (128, 0, 128))
    def test_case_09(self): self.run_case("pink", (255, 192, 203))
    def test_case_10(self): self.run_case("gray", (128, 128, 128))

    def test_case_11(self): self.run_case("brown", (165, 42, 42))
    def test_case_12(self): self.run_case("sky blue", (135, 206, 235))
    def test_case_13(self): self.run_case("salmon", (250, 128, 114))
    def test_case_14(self): self.run_case("misty rose", (255, 228, 225))
    def test_case_15(self): self.run_case("beige", (245, 245, 220))

    def test_case_16(self): self.run_case("steel blue", (70, 130, 180))
    def test_case_17(self): self.run_case("tomato", (255, 99, 71))
    def test_case_18(self): self.run_case("powder blue", (176, 224, 230))
    def test_case_19(self): self.run_case("alice blue", (240, 248, 255))
    def test_case_20(self): self.run_case("antique white", (250, 235, 215))

    def test_case_21(self): self.run_case("pale green", (152, 251, 152))
    def test_case_22(self): self.run_case("violet", (238, 130, 238))
    def test_case_23(self): self.run_case("medium orchid", (186, 85, 211))
    def test_case_24(self): self.run_case("light salmon", (255, 160, 122))
    def test_case_25(self): self.run_case("hot pink", (255, 105, 180))

    def test_case_26(self): self.run_case("light blue", (173, 216, 230))
    def test_case_27(self): self.run_case("dark turquoise", (0, 206, 209))
    def test_case_28(self): self.run_case("yellow green", (154, 205, 50))
    def test_case_29(self): self.run_case("deep pink", (255, 20, 147))
    def test_case_30(self): self.run_case("sea green", (46, 139, 87))

    def test_case_31(self): self.run_case("gold", (255, 215, 0))
    def test_case_32(self): self.run_case("light pink", (255, 182, 193))
    def test_case_33(self): self.run_case("dark slate blue", (72, 61, 139))
    def test_case_34(self): self.run_case("dim gray", (105, 105, 105))
    def test_case_35(self): self.run_case("cornsilk", (255, 248, 220))

    def test_case_36(self): self.run_case("olive drab", (107, 142, 35))
    def test_case_37(self): self.run_case("dark salmon", (233, 150, 122))
    def test_case_38(self): self.run_case("dark khaki", (189, 183, 107))
    def test_case_39(self): self.run_case("dark slate gray", (47, 79, 79))
    def test_case_40(self): self.run_case("seashell", (255, 245, 238))

    def test_case_41(self): self.run_case("snow", (255, 250, 250))
    def test_case_42(self): self.run_case("deep sky blue", (0, 191, 255))
    def test_case_43(self): self.run_case("cyan", (0, 255, 255))
    def test_case_44(self): self.run_case("plum", (221, 160, 221))
    def test_case_45(self): self.run_case("coral", (255, 127, 80))

    def test_case_46(self): self.run_case("orchid", (218, 112, 214))
    def test_case_47(self): self.run_case("light goldenrod yellow", (250, 250, 210))
    def test_case_48(self): self.run_case("cornflower blue", (100, 149, 237))
    def test_case_49(self): self.run_case("khaki", (240, 230, 140))
    def test_case_50(self): self.run_case("maroon", (128, 0, 0))

if __name__ == "__main__":
    unittest.main()
