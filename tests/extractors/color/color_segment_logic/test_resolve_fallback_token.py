#Chatbot/tests/extractors/color/color_segment_logic/test_resolve_fallback_token.py

import unittest
from unittest.mock import patch
from Chatbot.extractors.color.color_segment_logic import resolve_fallback_tokens

rgb_map = {
    "soft pink": (255, 192, 203),
    "bright red": (255, 0, 0),
    "peach": (255, 218, 185),
    "coral": (255, 127, 80),
    "dusty rose": (188, 143, 143),
    "nude": (205, 180, 145),
    "cherry red": (222, 49, 99),
    "light beige": (245, 245, 220),
    "warm peach": (243, 207, 183),
    "deep cherry": (136, 8, 8),
    "rose": (188, 143, 143),
    "beige": (245, 245, 220),
}

mock_rgb = {
    "pink": (255, 192, 203),
    "red": (255, 0, 0),
    "peach": (255, 218, 185),
    "coral": (255, 127, 80),
    "rose": (188, 143, 143),
    "nude": (205, 180, 145),
    "cherry": (222, 49, 99),
    "beige": (245, 245, 220),
    "warm": (243, 207, 183),
    "deep": (136, 8, 8),
}

def mock_rgb_func(token):
    return mock_rgb.get(token.split()[-1], None)

def mock_similar_func(rgb, _):
    return [name for name, val in rgb_map.items() if val == rgb]

class TestResolveFallbackTokens(unittest.TestCase):

    @patch("Chatbot.extractors.color.color_segment_logic.get_rgb_from_descriptive_color_llm_first", side_effect=mock_rgb_func)
    @patch("Chatbot.extractors.color.color_segment_logic.find_similar_color_names", side_effect=mock_similar_func)
    def test_case_01(self, *_):
        expected = ["soft pink"]
        result = resolve_fallback_tokens("pink", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = ["bright red"]
        result = resolve_fallback_tokens("red", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = ["peach"]
        result = resolve_fallback_tokens("peach", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = ["coral"]
        result = resolve_fallback_tokens("coral shade", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = ["dusty rose"]
        result = resolve_fallback_tokens("dusty rose finish", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = ["nude"]
        result = resolve_fallback_tokens("nude tone", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = []
        result = resolve_fallback_tokens("pink", {"pink"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = []
        result = resolve_fallback_tokens("123 pink!", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = []
        result = resolve_fallback_tokens("💖 pinky 💖", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = ["cherry red"]
        result = resolve_fallback_tokens("deep cherry red lipstick", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = ["light beige"]
        result = resolve_fallback_tokens("beige and light beige are elegant", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = ["warm peach"]
        result = resolve_fallback_tokens("warm peach glow", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = ["deep cherry"]
        result = resolve_fallback_tokens("deep cherry gloss", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = ["soft pink"]
        result = resolve_fallback_tokens("soft pink pink pink", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = ["bright red"]
        result = resolve_fallback_tokens("BRIGHT RED", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = ["coral"]
        result = resolve_fallback_tokens("…coral; nude, red.", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = []
        result = resolve_fallback_tokens("blargh", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = []
        result = resolve_fallback_tokens("superfantasticpurple", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = ["nude"]
        result = resolve_fallback_tokens("nude", {"soft pink"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = ["rose"]
        result = resolve_fallback_tokens("rose powder", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = ["beige"]
        result = resolve_fallback_tokens("beige cover", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = []
        result = resolve_fallback_tokens("softly boldly pink", {"pink"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = []
        result = resolve_fallback_tokens("elegance", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = ["bright red"]
        result = resolve_fallback_tokens("red red", {"red"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = ["peach"]
        result = resolve_fallback_tokens("peach something", {"nude"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = []
        result = resolve_fallback_tokens("glowy", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = ["warm peach"]
        result = resolve_fallback_tokens("warm peach tones are beautiful", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = ["dusty rose"]
        result = resolve_fallback_tokens("dusty rose look", {"dusty"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = []
        result = resolve_fallback_tokens("very very pink", {"pink"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = ["soft pink"]
        result = resolve_fallback_tokens("soft pinky shade", {"pink"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = ["cherry red"]
        result = resolve_fallback_tokens("cherry red", {"cherry"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = []
        result = resolve_fallback_tokens("matte", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = []
        result = resolve_fallback_tokens("sparkly", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = []
        result = resolve_fallback_tokens("silver", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = []
        result = resolve_fallback_tokens("gold", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = []
        result = resolve_fallback_tokens("clear", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = []
        result = resolve_fallback_tokens("transparent", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = []
        result = resolve_fallback_tokens("non-color", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = ["soft pink"]
        result = resolve_fallback_tokens("they said soft pink", {"nude"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = ["peach"]
        result = resolve_fallback_tokens("the color peach", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = []
        result = resolve_fallback_tokens("they love matte looks", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = ["deep cherry"]
        result = resolve_fallback_tokens("deep cherry feels", {"cherry"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = ["cherry red"]
        result = resolve_fallback_tokens("not cherry but cherry red", {"red"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = ["warm peach"]
        result = resolve_fallback_tokens("nope, just warm peach", {"warm"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = ["light beige"]
        result = resolve_fallback_tokens("light beige is the base", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = ["bright red"]
        result = resolve_fallback_tokens("like bright red", set(), set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = []
        result = resolve_fallback_tokens("none of these: pink, red, beige", {"pink", "red", "beige"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = ["nude"]
        result = resolve_fallback_tokens("only nude", {"soft"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = ["peach"]
        result = resolve_fallback_tokens("still peach", {"red"}, set(), rgb_map)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = ["peach"]
        result = resolve_fallback_tokens("really love peach blush", {"blush"}, set(), rgb_map)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()

