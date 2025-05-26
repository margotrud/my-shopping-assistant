#Chatbot/tests/extractors/color/categorizer/test_clean_and_categorize.py

import unittest
import os
import json
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.categorizer import clean_and_categorize

class TestCleanAndCategorize(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.abspath(__file__)
        while not current_dir.endswith("pythonProject1"):
            current_dir = os.path.dirname(current_dir)
        modifiers_path = os.path.join(current_dir, "Data", "known_modifiers.json")
        with open(modifiers_path, "r", encoding="utf-8") as f:
            cls.known_modifiers = set(json.load(f))

    def test_case_01(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bold"],
            "modifier_to_tone": {"bold": ["red"]},
            "tone_to_modifier": {"red": ["bold"]}
        }
        result = clean_and_categorize(["bold red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = {
            "tones": ["pink"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["pink"]},
            "tone_to_modifier": {"pink": ["soft"]}
        }
        result = clean_and_categorize(["soft pink"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = {
            "tones": ["pink", "red"],
            "modifiers": ["bold", "soft"],
            "modifier_to_tone": {"bold": ["red"], "soft": ["pink"]},
            "tone_to_modifier": {"pink": ["soft"], "red": ["bold"]}
        }
        result = clean_and_categorize(["soft pink", "bold red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = {
            "tones": ["beige", "brown"],
            "modifiers": ["muted", "warm"],
            "modifier_to_tone": {"muted": ["beige"], "warm": ["brown"]},
            "tone_to_modifier": {"beige": ["muted"], "brown": ["warm"]}
        }
        result = clean_and_categorize(["muted beige", "warm brown"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = {
            "tones": ["coral", "peach"],
            "modifiers": ["bright", "light"],
            "modifier_to_tone": {"bright": ["coral"], "light": ["peach"]},
            "tone_to_modifier": {"coral": ["bright"], "peach": ["light"]}
        }
        result = clean_and_categorize(["bright coral", "light peach"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = {
            "tones": ["pink"],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["pink"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = {
            "tones": [],
            "modifiers": ["dusty"],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["dusty"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = {
            "tones": ['purple'],
            "modifiers": ['luxurious'],
            "modifier_to_tone": {'luxurious': ['purple']},
            "tone_to_modifier": {'purple': ['luxurious']}
        }
        result = clean_and_categorize(["luxurious purple"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["cool", "deep"],
            "modifier_to_tone": {"cool": ["red"], "deep": ["red"]},
            "tone_to_modifier": {"red": ["cool", "deep"]}
        }
        result = clean_and_categorize(["cool deep red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = {
            "tones": ["nude"],
            "modifiers": ["soft", "warm"],
            "modifier_to_tone": {"soft": ["nude"], "warm": ["nude"]},
            "tone_to_modifier": {"nude": ["soft", "warm"]}
        }
        result = clean_and_categorize(["soft warm nude"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["blue"]},
            "tone_to_modifier": {"blue": ["deep"]}
        }
        result = clean_and_categorize(["deep blue"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["cool", "light"],
            "modifier_to_tone": {"cool": ["green"], "light": ["green"]},
            "tone_to_modifier": {"green": ["cool", "light"]}
        }
        result = clean_and_categorize(["cool light green"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["orange"]},
            "tone_to_modifier": {"orange": ["bright"]}
        }
        result = clean_and_categorize(["bright orange"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = {
            "tones": ["beige", "lavender"],
            "modifiers": ["cool", "soft"],
            "modifier_to_tone": {"cool": ["beige"], "soft": ["lavender"]},
            "tone_to_modifier": {"beige": ["cool"], "lavender": ["soft"]}
        }
        result = clean_and_categorize(["soft lavender", "cool beige"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = {
            "tones": ["pink"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["pink"]},
            "tone_to_modifier": {"pink": ["muted"]}
        }
        result = clean_and_categorize(["muted pink"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = {
            "tones": ["blue", "red", "yellow"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["blue", "red", "yellow"]},
            "tone_to_modifier": {
                "blue": ["bright"],
                "red": ["bright"],
                "yellow": ["bright"]
            }
        }
        result = clean_and_categorize(["bright red", "bright blue", "bright yellow"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = {
            "tones": ["peach"],
            "modifiers": ["dusty"],
            "modifier_to_tone": {"dusty": ["peach"]},
            "tone_to_modifier": {"peach": ["dusty"]}
        }
        result = clean_and_categorize(["dusty peach"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = {
            "tones": ["brown"],
            "modifiers": ["rich"],
            "modifier_to_tone": {"rich": ["brown"]},
            "tone_to_modifier": {"brown": ["rich"]}
        }
        result = clean_and_categorize(["rich brown"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = {
            "tones": ["nude"],
            "modifiers": ["soft", "warm"],
            "modifier_to_tone": {"soft": ["nude"], "warm": ["nude"]},
            "tone_to_modifier": {"nude": ["soft", "warm"]}
        }
        result = clean_and_categorize(["soft warm nude"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["red"]},
            "tone_to_modifier": {"red": ["bright"]}
        }
        result = clean_and_categorize(["bright red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = {
            "tones": ["peach", "pink"],
            "modifiers": ["muted", "warm"],
            "modifier_to_tone": {"muted": ["peach"], "warm": ["pink"]},
            "tone_to_modifier": {"peach": ["muted"], "pink": ["warm"]}
        }
        result = clean_and_categorize(["warm pink", "muted peach"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = {
            "tones": ["gray"],
            "modifiers": ["cool"],
            "modifier_to_tone": {"cool": ["gray"]},
            "tone_to_modifier": {"gray": ["cool"]}
        }
        result = clean_and_categorize(["cool gray"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = {
            "tones": ["blue"],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["deepest blue"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = {
            "tones": [],
            "modifiers": ["neutral"],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["neutral vibe"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = {
            "tones": ["blue", "gray"],
            "modifiers": ["dusty"],
            "modifier_to_tone": {"dusty": ["blue", "gray"]},
            "tone_to_modifier": {"blue": ["dusty"], "gray": ["dusty"]}
        }
        result = clean_and_categorize(["dusty blue", "dusty gray"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = {
            "tones": ["rose"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["rose"]},
            "tone_to_modifier": {"rose": ["warm"]}
        }
        result = clean_and_categorize(["warm rose"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["bold", "deep"],
            "modifier_to_tone": {"bold": ["orange"], "deep": ["orange"]},
            "tone_to_modifier": {"orange": ["bold", "deep"]}
        }
        result = clean_and_categorize(["deep bold orange"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = {
            "tones": ["yellow"],
            "modifiers": ["cool", "light"],
            "modifier_to_tone": {"cool": ["yellow"], "light": ["yellow"]},
            "tone_to_modifier": {"yellow": ["cool", "light"]}
        }
        result = clean_and_categorize(["cool light yellow"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = {
            "tones": ["coral", "pink"],
            "modifiers": ["bold"],
            "modifier_to_tone": {"bold": ["coral", "pink"]},
            "tone_to_modifier": {"coral": ["bold"], "pink": ["bold"]}
        }
        result = clean_and_categorize(["bold pink", "bold coral"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["red"]},
            "tone_to_modifier": {"red": ["bright"]}
        }
        result = clean_and_categorize(["bright red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["green"]},
            "tone_to_modifier": {"green": ["muted"]}
        }
        result = clean_and_categorize(["muted green"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bold", "bright"],
            "modifier_to_tone": {"bold": ["red"], "bright": ["red"]},
            "tone_to_modifier": {"red": ["bold", "bright"]}
        }
        result = clean_and_categorize(["bold bright red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = {
            "tones": ["beige"],
            "modifiers": ["cool", "soft"],
            "modifier_to_tone": {"cool": ["beige"], "soft": ["beige"]},
            "tone_to_modifier": {"beige": ["cool", "soft"]}
        }
        result = clean_and_categorize(["cool soft beige"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = {
            "tones": ["brown"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["brown"]},
            "tone_to_modifier": {"brown": ["deep"]}
        }
        result = clean_and_categorize(["deep brown"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = {
            "tones": [],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["random phrase"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = {
            "tones": ["beige", "pink"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["beige", "pink"]},
            "tone_to_modifier": {"beige": ["soft"], "pink": ["soft"]}
        }
        result = clean_and_categorize(["soft pink", "soft beige"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["blue"]},
            "tone_to_modifier": {"blue": ["warm"]}
        }
        result = clean_and_categorize(["warm blue"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = {
            "tones": ["coral", "peach", "rose"],
            "modifiers": ["light"],
            "modifier_to_tone": {"light": ["coral", "peach", "rose"]},
            "tone_to_modifier": {
                "coral": ["light"],
                "peach": ["light"],
                "rose": ["light"]
            }
        }
        result = clean_and_categorize(["light coral", "light peach", "light rose"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["red"]},
            "tone_to_modifier": {"red": ["soft"]}
        }
        result = clean_and_categorize(["soft red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = {
            "tones": ["beige", "nude"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["beige", "nude"]},
            "tone_to_modifier": {"beige": ["warm"], "nude": ["warm"]}
        }
        result = clean_and_categorize(["warm nude", "warm beige"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = {
            "tones": ["pink", "red"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["pink", "red"]},
            "tone_to_modifier": {"pink": ["deep"], "red": ["deep"]}
        }
        result = clean_and_categorize(["deep red", "deep pink"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["red"]},
            "tone_to_modifier": {"red": ["bright"]}
        }
        result = clean_and_categorize(["very bright red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = {
            "tones": ["blue", "green"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["blue", "green"]},
            "tone_to_modifier": {"blue": ["muted"], "green": ["muted"]}
        }
        result = clean_and_categorize(["muted blue", "muted green"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["orange"]},
            "tone_to_modifier": {"orange": ["soft"]}
        }
        result = clean_and_categorize(["orange soft"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["cool"],
            "modifier_to_tone": {"cool": ["green"]},
            "tone_to_modifier": {"green": ["cool"]}
        }
        result = clean_and_categorize(["green cool"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["bold", "deep"],
            "modifier_to_tone": {"bold": ["blue"], "deep": ["blue"]},
            "tone_to_modifier": {"blue": ["bold", "deep"]}
        }
        result = clean_and_categorize(["bold deep blue"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = {
            "tones": ["brown", "pink", "red"],
            "modifiers": ["dusty"],
            "modifier_to_tone": {"dusty": ["brown", "pink", "red"]},
            "tone_to_modifier": {
                "brown": ["dusty"],
                "pink": ["dusty"],
                "red": ["dusty"]
            }
        }
        result = clean_and_categorize(["dusty red", "dusty pink", "dusty brown"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ['icy'],
            "modifier_to_tone": {'icy': ['blue']},
            "tone_to_modifier": {'blue': ['icy']}
        }
        result = clean_and_categorize(["icy blue"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = {
            "tones": ["red"],
            "modifiers": ['deep', 'rich','vibrant'],
            "modifier_to_tone": {'deep': ['red'], 'rich': ['red'], 'vibrant': ['red']},
            "tone_to_modifier": {'red': ['deep', 'rich', 'vibrant']},
        }
        result = clean_and_categorize(["rich deep vibrant red"], self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = {
            "tones": [],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = clean_and_categorize(["elegant timeless"], self.known_modifiers)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()