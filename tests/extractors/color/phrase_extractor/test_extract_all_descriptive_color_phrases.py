#test/extractors/color/phrase_extractor/test_extract_all_descriptive_color_phrases.py

import unittest
import json
import os
from typing import Set

from Chatbot.extractors.color.phrase_extractor import extract_all_descriptive_color_phrases
from Chatbot.extractors.color import known_tones, all_webcolor_names



class TestExtractAllDescriptiveColorPhrases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load known_modifiers from JSON
        current_dir = os.path.abspath(__file__)
        while not current_dir.endswith("pythonProject1"):
            current_dir = os.path.dirname(current_dir)
        modifiers_path = os.path.join(current_dir, "Data", "known_modifiers.json")
        with open(modifiers_path, "r", encoding="utf-8") as f:
            cls.known_modifiers = set(json.load(f))
    def test_case_01(self):
        expected = ["pink"]
        result = extract_all_descriptive_color_phrases("pink", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = ["soft pink"]
        result = extract_all_descriptive_color_phrases("soft pink", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = ["red"]
        result = extract_all_descriptive_color_phrases("A simple red should work", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = ["soft pink", "rose"]
        result = extract_all_descriptive_color_phrases("something like soft pink or rose", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = ["mauve"]
        result = extract_all_descriptive_color_phrases("mauve works well too", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = []
        result = extract_all_descriptive_color_phrases("elegant packaging", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = ["cool pink", "mauve"]
        result = extract_all_descriptive_color_phrases("between cool pink and mauve", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = ["deep red"]
        result = extract_all_descriptive_color_phrases("a deep red hue", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = ["soft pink"]
        result = extract_all_descriptive_color_phrases("soft pink soft pink soft pink", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = ["bold coral"]
        result = extract_all_descriptive_color_phrases("bold coral pops nicely", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = ["peach"]
        result = extract_all_descriptive_color_phrases("peach is a safe choice", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = ["soft pink"]
        result = extract_all_descriptive_color_phrases("I’d go with soft pink blush", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = ["warm peach"]
        result = extract_all_descriptive_color_phrases("Go with a warm peach tone", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = ["red", "peach"]
        result = extract_all_descriptive_color_phrases("Maybe red or peach?", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = ["soft pink", "light peach"]
        result = extract_all_descriptive_color_phrases("I like soft pink and light peach", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = []
        result = extract_all_descriptive_color_phrases("clean skin tone", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = ["nude"]
        result = extract_all_descriptive_color_phrases("always nude for work", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = ["bright pink"]
        result = extract_all_descriptive_color_phrases("bright pink is too much for me", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = ["peachy"]
        result = extract_all_descriptive_color_phrases("It feels very peachy", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = ["reddish"]
        result = extract_all_descriptive_color_phrases("Maybe something reddish", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)


    def test_case_21(self):
        expected = ["dusty rose"]
        result = extract_all_descriptive_color_phrases("dusty rose feels elegant", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = ["muted peach"]
        result = extract_all_descriptive_color_phrases("muted peach is perfect", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = ["rosy"]
        result = extract_all_descriptive_color_phrases("rosy tones are flattering", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = ["orangey"]
        result = extract_all_descriptive_color_phrases("something a bit orangey", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = ["bronzy"]
        result = extract_all_descriptive_color_phrases("a soft bronzy shade", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = ["cool beige"]
        result = extract_all_descriptive_color_phrases("go for cool beige", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = ["plum"]
        result = extract_all_descriptive_color_phrases("plum is my go-to", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = ["burnt orange"]
        result = extract_all_descriptive_color_phrases("burnt orange tones work great", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = ["soft pink", "deep coral"]
        result = extract_all_descriptive_color_phrases("soft pink or deep coral maybe", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = ["coral"]
        result = extract_all_descriptive_color_phrases("try coral if you're feeling bold", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = ["brown"]
        result = extract_all_descriptive_color_phrases("how about brown?", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = ["cool mauve"]
        result = extract_all_descriptive_color_phrases("cool mauve tones are trending", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = []
        result = extract_all_descriptive_color_phrases("I like the packaging", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = ["light brown"]
        result = extract_all_descriptive_color_phrases("light brown works for autumn", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = ["peachy", "soft pink"]
        result = extract_all_descriptive_color_phrases("peachy or soft pink?", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = ["soft peach", "warm beige"]
        result = extract_all_descriptive_color_phrases("maybe soft peach or warm beige", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = []
        result = extract_all_descriptive_color_phrases("sleek modern look", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = ["bold red"]
        result = extract_all_descriptive_color_phrases("bold red makes a statement", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = ["barely-there pink"]
        result = extract_all_descriptive_color_phrases("barely-there pink is what I want", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = ["reddish", "coral"]
        result = extract_all_descriptive_color_phrases("a bit reddish, almost coral", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = ["ashy rose"]
        result = extract_all_descriptive_color_phrases("ashy rose please", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = ["peach", "soft pink"]
        result = extract_all_descriptive_color_phrases("between peach and soft pink", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = ["cool mauve", "deep plum"]
        result = extract_all_descriptive_color_phrases("cool mauve or deep plum?", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = ["warm pink"]
        result = extract_all_descriptive_color_phrases("warm pink blush sounds perfect", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = ["cherry"]
        result = extract_all_descriptive_color_phrases("cherry is bold but I like it", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = ["brownish"]
        result = extract_all_descriptive_color_phrases("a bit brownish is fine", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = ["pink"]
        result = extract_all_descriptive_color_phrases("something pink, nothing too bright", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = ["bronze"]
        result = extract_all_descriptive_color_phrases("bronze shimmer maybe?", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = ["beige"]
        result = extract_all_descriptive_color_phrases("I’d go for beige", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = ["nude", "soft peach", "reddish"]
        result = extract_all_descriptive_color_phrases("I want nude, soft peach, and something reddish", known_tones, self.known_modifiers, all_webcolor_names)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
