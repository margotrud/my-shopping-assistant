import unittest
import webcolors
from matplotlib.colors import XKCD_COLORS
from Chatbot.extractors.color.llm.simplifier import is_valid_tone

def load_all_tones_from_web():
    css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
    xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS)
    return css_tones.union(xkcd_tones)

class TestIsValidTone(unittest.TestCase):

    def setUp(self):
        self.tones = load_all_tones_from_web()

    def test_case_01(self): self.assertEqual(True, is_valid_tone("peach", self.tones))
    def test_case_02(self): self.assertEqual(True, is_valid_tone("minty", self.tones))
    def test_case_03(self): self.assertEqual(True, is_valid_tone("greenish", self.tones))
    def test_case_04(self): self.assertEqual(True, is_valid_tone("rosy", self.tones))
    def test_case_05(self): self.assertEqual(False, is_valid_tone("glamorous", self.tones))
    def test_case_06(self): self.assertEqual(True, is_valid_tone("taupe", self.tones))
    def test_case_07(self): self.assertEqual(True, is_valid_tone("navyy", self.tones))
    def test_case_08(self): self.assertEqual(False, is_valid_tone("luxurious", self.tones))
    def test_case_09(self): self.assertEqual(True, is_valid_tone("beige", self.tones))
    def test_case_10(self): self.assertEqual(True, is_valid_tone("bronze", self.tones))
    def test_case_11(self): self.assertEqual(True, is_valid_tone("caramelly", self.tones))
    def test_case_12(self): self.assertEqual(False, is_valid_tone("metallic", self.tones))
    def test_case_13(self): self.assertEqual(False, is_valid_tone("glitter", self.tones))
    def test_case_14(self): self.assertEqual(True, is_valid_tone("peachish", self.tones))
    def test_case_15(self): self.assertEqual(False, is_valid_tone("complicatedtone", self.tones))
    def test_case_16(self): self.assertEqual(True, is_valid_tone("rose", self.tones))
    def test_case_17(self): self.assertEqual(False, is_valid_tone("nude", self.tones))
    def test_case_18(self): self.assertEqual(True, is_valid_tone("blushy", self.tones))
    def test_case_19(self): self.assertEqual(False, is_valid_tone("refined", self.tones))
    def test_case_20(self): self.assertEqual(False, is_valid_tone("electric", self.tones))
    def test_case_21(self): self.assertEqual(True, is_valid_tone("grayish", self.tones))
    def test_case_22(self): self.assertEqual(True, is_valid_tone("pinkish", self.tones))
    def test_case_23(self): self.assertEqual(True, is_valid_tone("bluish", self.tones))
    def test_case_24(self): self.assertEqual(True, is_valid_tone("redish", self.tones))
    def test_case_25(self): self.assertEqual(False, is_valid_tone("translucent", self.tones))
    def test_case_26(self): self.assertEqual(True, is_valid_tone("white", self.tones.union({"white"})))
    def test_case_27(self): self.assertEqual(True, is_valid_tone("bluey", self.tones))
    def test_case_28(self): self.assertEqual(True, is_valid_tone("shimmery", self.tones))
    def test_case_29(self): self.assertEqual(False, is_valid_tone("shimmer", self.tones))
    def test_case_30(self): self.assertEqual(False, is_valid_tone("sparkling", self.tones))
    def test_case_31(self): self.assertEqual(True, is_valid_tone("frosty", self.tones))
    def test_case_32(self): self.assertEqual(True, is_valid_tone("creamy", self.tones))
    def test_case_33(self): self.assertEqual(True, is_valid_tone("mossy", self.tones))
    def test_case_34(self): self.assertEqual(True, is_valid_tone("muddy", self.tones))
    def test_case_35(self): self.assertEqual(True, is_valid_tone("cloudy", self.tones))
    def test_case_36(self): self.assertEqual(True, is_valid_tone("inky", self.tones))
    def test_case_37(self): self.assertEqual(True, is_valid_tone("foggy", self.tones))
    def test_case_38(self): self.assertEqual(False, is_valid_tone("statement", self.tones))
    def test_case_39(self): self.assertEqual(False, is_valid_tone("vibrant", self.tones))
    def test_case_40(self): self.assertEqual(False, is_valid_tone("chic", self.tones))
    def test_case_41(self): self.assertEqual(True, is_valid_tone("dusty", self.tones))
    def test_case_42(self): self.assertEqual(True, is_valid_tone("pinky", self.tones))
    def test_case_43(self): self.assertEqual(True, is_valid_tone("plummy", self.tones))
    def test_case_44(self): self.assertEqual(True, is_valid_tone("ashy", self.tones))
    def test_case_45(self): self.assertEqual(True, is_valid_tone("fairy", self.tones))
    def test_case_46(self): self.assertEqual(False, is_valid_tone("glistening", self.tones))
    def test_case_47(self): self.assertEqual(True, is_valid_tone("daisy", self.tones))
    def test_case_48(self): self.assertEqual(True, is_valid_tone("buttery", self.tones))
    def test_case_49(self): self.assertEqual(True, is_valid_tone("grassy", self.tones))
    def test_case_50(self): self.assertEqual(True, is_valid_tone("rosy", self.tones))

if __name__ == "__main__":
    unittest.main()
