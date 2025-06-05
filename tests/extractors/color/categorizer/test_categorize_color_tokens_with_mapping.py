# Chatbot/extractors/color/categorizer/test_categorize_color_tokens_with_mapping.py
import unittest
from Chatbot.extractors.color.extract.categorizer import categorize_color_tokens_with_mapping
from Chatbot.extractors.color import known_tones


class TestCategorizeColorTokensWithMapping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tones = known_tones  # uses the same one from __init__.py

        # Load modifiers (still JSON-based)
        import os, json
        current_dir = os.path.abspath(__file__)
        while not current_dir.endswith("pythonProject1"):
            current_dir = os.path.dirname(current_dir)
        data_path = os.path.join(current_dir, "Data", "known_modifiers.json")
        with open(data_path, "r", encoding="utf-8") as f:
            cls.modifiers = set(json.load(f))

    def test_case_01(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bold"],
            "modifier_to_tone": {"bold": ["red"]},
            "tone_to_modifier": {"red": ["bold"]}
        }
        result = categorize_color_tokens_with_mapping(["bold red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = {
            "tones": ["pink"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["pink"]},
            "tone_to_modifier": {"pink": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["soft pink"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = {
            "tones": ["coral"],
            "modifiers": ["light"],
            "modifier_to_tone": {"light": ["coral"]},
            "tone_to_modifier": {"coral": ["light"]}
        }
        result = categorize_color_tokens_with_mapping(["light coral"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = {
            "tones": ["peach"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["peach"]},
            "tone_to_modifier": {"peach": ["muted"]}
        }
        result = categorize_color_tokens_with_mapping(["muted peach"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = {
            "tones": ["beige", "brown"],
            "modifiers": ["cool", "warm"],
            "modifier_to_tone": {"cool": ["beige"], "warm": ["brown"]},
            "tone_to_modifier": {"beige": ["cool"], "brown": ["warm"]}
        }
        result = categorize_color_tokens_with_mapping(["cool beige", "warm brown"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = {
            "tones": ["pink", "red"],
            "modifiers": ["bold", "soft"],
            "modifier_to_tone": {"bold": ["red"], "soft": ["pink"]},
            "tone_to_modifier": {"red": ["bold"], "pink": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["soft pink", "bold red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = {
            "tones": ["pink"],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["pink"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = {
            "tones": [],
            "modifiers": ["dusty"],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["dusty"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = {
            "tones": ['purple'],
            "modifiers": ['luxurious'],
            "modifier_to_tone": {'luxurious': ['purple']},
            "tone_to_modifier": {'purple': ['luxurious']}
        }
        result = categorize_color_tokens_with_mapping(["luxurious purple"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["cool", "deep"],
            "modifier_to_tone": {"cool": ["red"], "deep": ["red"]},
            "tone_to_modifier": {"red": ["cool", "deep"]}
        }
        result = categorize_color_tokens_with_mapping(["cool deep red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["blue"]},
            "tone_to_modifier": {"blue": ["deep"]}
        }
        result = categorize_color_tokens_with_mapping(["deep blue"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["cool", "light"],
            "modifier_to_tone": {"cool": ["green"], "light": ["green"]},
            "tone_to_modifier": {"green": ["cool", "light"]}
        }
        result = categorize_color_tokens_with_mapping(["cool light green"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["orange"]},
            "tone_to_modifier": {"orange": ["bright"]}
        }
        result = categorize_color_tokens_with_mapping(["bright orange"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = {
            "tones": ["beige", "lavender"],
            "modifiers": ["cool", "soft"],
            "modifier_to_tone": {"cool": ["beige"], "soft": ["lavender"]},
            "tone_to_modifier": {"beige": ["cool"], "lavender": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["soft lavender", "cool beige"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = {
            "tones": ["pink"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["pink"]},
            "tone_to_modifier": {"pink": ["muted"]}
        }
        result = categorize_color_tokens_with_mapping(["muted pink"], self.tones, self.modifiers)
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
        result = categorize_color_tokens_with_mapping(
            ["bright red", "bright blue", "bright yellow"], self.tones, self.modifiers
        )
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = {
            "tones": ["peach"],
            "modifiers": ["dusty"],
            "modifier_to_tone": {"dusty": ["peach"]},
            "tone_to_modifier": {"peach": ["dusty"]}
        }
        result = categorize_color_tokens_with_mapping(["dusty peach"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = {
            "tones": ["brown"],
            "modifiers": ['rich'],
            "modifier_to_tone": {'rich': ['brown']},
            "tone_to_modifier": {'brown': ['rich']}
        }
        result = categorize_color_tokens_with_mapping(["rich brown"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = {
            "tones": ['nude'],
            "modifiers": ["soft", "warm"],
            "modifier_to_tone": {'soft': ['nude'], 'warm': ['nude']},
            "tone_to_modifier": {'nude': ['soft', 'warm']}
        }
        result = categorize_color_tokens_with_mapping(["soft warm nude"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = {
            "tones": ["pink"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["pink"]},
            "tone_to_modifier": {"pink": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["very soft pink"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = {
            "tones": ["peach", "pink"],
            "modifiers": ["muted", "warm"],
            "modifier_to_tone": {"muted": ["peach"], "warm": ["pink"]},
            "tone_to_modifier": {"peach": ["muted"], "pink": ["warm"]}
        }
        result = categorize_color_tokens_with_mapping(["warm pink", "muted peach"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = {
            "tones": ["gray"],
            "modifiers": ["cool"],
            "modifier_to_tone": {"cool": ["gray"]},
            "tone_to_modifier": {"gray": ["cool"]}
        }
        result = categorize_color_tokens_with_mapping(["cool gray"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = {
            "tones": ["blue"],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["deepest blue"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = {
            "tones": [],
            "modifiers": ['neutral'],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["neutral vibe"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = {
            "tones": ["blue", "gray"],
            "modifiers": ["dusty"],
            "modifier_to_tone": {"dusty": ["blue", "gray"]},
            "tone_to_modifier": {"blue": ["dusty"], "gray": ["dusty"]}
        }
        result = categorize_color_tokens_with_mapping(["dusty blue", "dusty gray"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = {
            "tones": ["rose"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["rose"]},
            "tone_to_modifier": {"rose": ["warm"]}
        }
        result = categorize_color_tokens_with_mapping(["warm rose"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["bold", "deep"],
            "modifier_to_tone": {"bold": ["orange"], "deep": ["orange"]},
            "tone_to_modifier": {"orange": ["bold", "deep"]}
        }
        result = categorize_color_tokens_with_mapping(["deep bold orange"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = {
            "tones": ["yellow"],
            "modifiers": ["cool", "light"],
            "modifier_to_tone": {"cool": ["yellow"], "light": ["yellow"]},
            "tone_to_modifier": {"yellow": ["cool", "light"]}
        }
        result = categorize_color_tokens_with_mapping(["cool light yellow"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = {
            "tones": ["coral", "pink"],
            "modifiers": ["bold"],
            "modifier_to_tone": {"bold": ["coral", "pink"]},
            "tone_to_modifier": {"coral": ["bold"], "pink": ["bold"]}
        }
        result = categorize_color_tokens_with_mapping(["bold pink", "bold coral"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bright"],
            "modifier_to_tone": {"bright": ["red"]},
            "tone_to_modifier": {"red": ["bright"]}
        }
        result = categorize_color_tokens_with_mapping(["bright red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["green"]},
            "tone_to_modifier": {"green": ["muted"]}
        }
        result = categorize_color_tokens_with_mapping(["muted green"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bold", "bright"],
            "modifier_to_tone": {"bold": ["red"], "bright": ["red"]},
            "tone_to_modifier": {"red": ["bold", "bright"]}
        }
        result = categorize_color_tokens_with_mapping(["bold bright red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = {
            "tones": ["beige"],
            "modifiers": ["cool", "soft"],
            "modifier_to_tone": {"cool": ["beige"], "soft": ["beige"]},
            "tone_to_modifier": {"beige": ["cool", "soft"]}
        }
        result = categorize_color_tokens_with_mapping(["cool soft beige"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = {
            "tones": ["brown"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["brown"]},
            "tone_to_modifier": {"brown": ["deep"]}
        }
        result = categorize_color_tokens_with_mapping(["deep brown"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = {
            "tones": [],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["random phrase"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = {
            "tones": ["beige", "pink"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["beige", "pink"]},
            "tone_to_modifier": {"beige": ["soft"], "pink": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["soft pink", "soft beige"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["blue"]},
            "tone_to_modifier": {"blue": ["warm"]}
        }
        result = categorize_color_tokens_with_mapping(["warm blue"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = {
            "tones": ["coral", "peach", "rose"],
            "modifiers": ["light"],
            "modifier_to_tone": {"light": ["coral", "peach", "rose"]},
            "tone_to_modifier": {"coral": ["light"], "peach": ["light"], "rose": ["light"]}
        }
        result = categorize_color_tokens_with_mapping(["light coral", "light peach", "light rose"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["red"]},
            "tone_to_modifier": {"red": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["soft red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = {
            "tones": ["beige", "nude"],
            "modifiers": ["warm"],
            "modifier_to_tone": {"warm": ["beige", "nude"]},
            "tone_to_modifier": {"beige": ["warm"], "nude": ["warm"]}
        }
        result = categorize_color_tokens_with_mapping(["warm nude", "warm beige"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = {
            "tones": ["pink", "red"],
            "modifiers": ["deep"],
            "modifier_to_tone": {"deep": ["pink", "red"]},
            "tone_to_modifier": {"pink": ["deep"], "red": ["deep"]}
        }
        result = categorize_color_tokens_with_mapping(["deep red", "deep pink"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = {
            "tones": ["red"],
            "modifiers": ["bright"],
            "modifier_to_tone": {'bright': ['red']},
            "tone_to_modifier": {'red': ['bright']}
        }
        result = categorize_color_tokens_with_mapping(["very bright red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = {
            "tones": ["blue", "green"],
            "modifiers": ["muted"],
            "modifier_to_tone": {"muted": ["blue", "green"]},
            "tone_to_modifier": {"blue": ["muted"], "green": ["muted"]}
        }
        result = categorize_color_tokens_with_mapping(["muted blue", "muted green"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = {
            "tones": ["orange"],
            "modifiers": ["soft"],
            "modifier_to_tone": {"soft": ["orange"]},
            "tone_to_modifier": {"orange": ["soft"]}
        }
        result = categorize_color_tokens_with_mapping(["orange soft"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = {
            "tones": ["green"],
            "modifiers": ["cool"],
            "modifier_to_tone": {"cool": ["green"]},
            "tone_to_modifier": {"green": ["cool"]}
        }
        result = categorize_color_tokens_with_mapping(["green cool"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ["bold", "deep"],
            "modifier_to_tone": {"bold": ["blue"], "deep": ["blue"]},
            "tone_to_modifier": {"blue": ["bold", "deep"]}
        }
        result = categorize_color_tokens_with_mapping(["bold deep blue"], self.tones, self.modifiers)
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
        result = categorize_color_tokens_with_mapping(["dusty red", "dusty pink", "dusty brown"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = {
            "tones": ["blue"],
            "modifiers": ['icy'],
            "modifier_to_tone": {'icy': ['blue']},
            "tone_to_modifier": {'blue': ['icy']}
        }
        result = categorize_color_tokens_with_mapping(["icy blue"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = {
            "tones": ["red"],
            "modifiers": ['deep', 'rich', 'vibrant'],
            "modifier_to_tone": {'deep': ['red'], 'rich': ['red'], 'vibrant': ['red']},
            "tone_to_modifier": {'red': ['deep', 'rich', 'vibrant']}
        }
        result = categorize_color_tokens_with_mapping(["rich deep vibrant red"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = {
            "tones": [],
            "modifiers": [],
            "modifier_to_tone": {},
            "tone_to_modifier": {}
        }
        result = categorize_color_tokens_with_mapping(["elegant timeless"], self.tones, self.modifiers)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
