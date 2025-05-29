#Tests/extractors/color/phrase_extractor/test_extract_phrases_from_segment.py
import unittest
import os
import json
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.phrase_extractor import extract_phrases_from_segment



class TestExtractPhrasesFromSegment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load known_modifiers from JSON
        current_dir = os.path.abspath(__file__)
        while not current_dir.endswith("pythonProject1"):
            current_dir = os.path.dirname(current_dir)
        modifiers_path = os.path.join(current_dir, "Data", "known_modifiers.json")
        with open(modifiers_path, "r", encoding="utf-8") as f:
            cls.known_modifiers = set(json.load(f))

        cls.known_tones = known_tones  # imported from color/__init__.py
    def test_case_01(self):
        expected = ["soft pink"]
        result = extract_phrases_from_segment("I like soft pink lipstick", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = ["bold red"]
        result = extract_phrases_from_segment("This bold red shade is stunning", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = ["warm peach"]
        result = extract_phrases_from_segment("Go for something warm peach", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = ["cool nude"]
        result = extract_phrases_from_segment("I prefer a cool nude tone", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = ["mauve"]
        result = extract_phrases_from_segment("mauve works well too", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = ["deep plum"]
        result = extract_phrases_from_segment("deep plum is elegant", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = ["luxurious", "matte"]
        result = extract_phrases_from_segment("luxurious matte finish", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = ["light beige"]
        result = extract_phrases_from_segment("maybe something light beige?", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = ["classic rose"]
        result = extract_phrases_from_segment("classic rose would be nice", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = ['rose', 'soft pink']
        result = extract_phrases_from_segment("soft pink or rose tones?", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = ["cool mauve"]
        result = extract_phrases_from_segment("cool mauve tones are trending", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = ["soft pink"]
        result = extract_phrases_from_segment("Soft pink is always flattering", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = []
        result = extract_phrases_from_segment("I'm unsure about the finish", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = ["coral"]
        result = extract_phrases_from_segment("Coral could work here", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = ["deep red"]
        result = extract_phrases_from_segment("A deep red hue, please", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = ["warm brown"]
        result = extract_phrases_from_segment("Give me something in warm brown", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = []
        result = extract_phrases_from_segment("clean aesthetic", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = ["light peach"]
        result = extract_phrases_from_segment("light peach shades are cute", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = ["plum"]
        result = extract_phrases_from_segment("Plum is pretty", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = ["nude"]
        result = extract_phrases_from_segment("a nude base would be great", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = ["bold coral"]
        result = extract_phrases_from_segment("bold coral pops nicely", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = ['nude', 'soft pink']
        result = extract_phrases_from_segment("something like soft pink or nude", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = ["light peach", "soft pink"]
        result = extract_phrases_from_segment("I like light peach and soft pink", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = ["cool pink"]
        result = extract_phrases_from_segment("cool pink vibes only", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = ["matte"]
        result = extract_phrases_from_segment("matte finish with shine", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = ["light pink"]
        result = extract_phrases_from_segment("My go-to is light pink", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = ["peach"]
        result = extract_phrases_from_segment("Go peach!", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = ['bright white', 'warm beige']
        result = extract_phrases_from_segment("I'd rather warm beige than bright white", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = ["deep brown"]
        result = extract_phrases_from_segment("deep brown works for contour", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = ["soft pink"]
        result = extract_phrases_from_segment("soft pink soft pink soft pink", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = ["cool beige"]
        result = extract_phrases_from_segment("cool beige always works for me", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = ["bold pink"]
        result = extract_phrases_from_segment("I want something bold pink", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = []
        result = extract_phrases_from_segment("smooth coverage with nice feel", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = ["soft mauve"]
        result = extract_phrases_from_segment("Go for a soft mauve blush", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = ["deep coral"]
        result = extract_phrases_from_segment("deep coral will look good", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = ["brown"]
        result = extract_phrases_from_segment("How about brown?", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = ['peach', 'red']
        result = extract_phrases_from_segment("Maybe red or peach", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = ["warm nude"]
        result = extract_phrases_from_segment("Choose a warm nude tone", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = ['bold', 'orange']
        result = extract_phrases_from_segment("Try orange if you're feeling bold", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = ["rose"]
        result = extract_phrases_from_segment("Rose looks elegant", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = ["cool pink", "mauve"]
        result = extract_phrases_from_segment("Between cool pink and mauve", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = ["nude"]
        result = extract_phrases_from_segment("Always nude for work", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = ["deep plum", "soft pink"]
        result = extract_phrases_from_segment("I’m hesitating between deep plum and soft pink", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = ["shiny"]
        result = extract_phrases_from_segment("Elegant packaging but too shiny", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = ["red"]
        result = extract_phrases_from_segment("A simple red should do", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = ['beige', 'peach']
        result = extract_phrases_from_segment("Try either peach or beige", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = ["deep peach"]
        result = extract_phrases_from_segment("deep peach lipstick goes with this", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = ['brown', 'plum']
        result = extract_phrases_from_segment("Plum and brown are my go-to", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = ["soft coral"]
        result = extract_phrases_from_segment("soft coral is so flattering", self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = ["bright pink"]
        result = extract_phrases_from_segment("bright pink is too much for me", self.known_modifiers)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
