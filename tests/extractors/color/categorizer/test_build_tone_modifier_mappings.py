# Chatbot/tests/extractors/color/categorizer/test_build_tone_modifier_mappings.py

import unittest
import os
import json
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.categorizer import build_tone_modifier_mappings

class TestBuildToneModifierMappings(unittest.TestCase):

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
        expected = (
            {"red"},
            {"bold"},
            {"bold": {"red"}},
            {"red": {"bold"}}
        )
        result = build_tone_modifier_mappings(["bold red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = (
            {"pink"},
            {"soft"},
            {"soft": {"pink"}},
            {"pink": {"soft"}}
        )
        result = build_tone_modifier_mappings(["soft pink"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = (
            {"red", "pink"},
            {"soft", "bold"},
            {"soft": {"pink"}, "bold": {"red"}},
            {"pink": {"soft"}, "red": {"bold"}}
        )
        result = build_tone_modifier_mappings(["soft pink", "bold red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = (
            {"beige", "brown"},
            {"muted", "warm"},
            {"muted": {"beige"}, "warm": {"brown"}},
            {"beige": {"muted"}, "brown": {"warm"}}
        )
        result = build_tone_modifier_mappings(["muted beige", "warm brown"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = (
            {"coral", "peach"},
            {"bright", "light"},
            {"bright": {"coral"}, "light": {"peach"}},
            {"coral": {"bright"}, "peach": {"light"}}
        )
        result = build_tone_modifier_mappings(["bright coral", "light peach"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = (
            {"pink", "red"},
            {"bold", "soft"},
            {"bold": {"red"}, "soft": {"pink"}},
            {"red": {"bold"}, "pink": {"soft"}}
        )
        result = build_tone_modifier_mappings(["soft pink", "bold red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = (
            {"pink"},
            set(),
            {},
            {}
        )
        result = build_tone_modifier_mappings(["pink"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = (
            set(),
            {"dusty"},
            {},
            {}
        )
        result = build_tone_modifier_mappings(["dusty"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = (
            {'purple'},
            {'luxurious'},
            {'luxurious': {'purple'}},
            {'purple': {'luxurious'}}
        )
        result = build_tone_modifier_mappings(["luxurious purple"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = (
            {"red"},
            {"deep", "cool"},
            {"deep": {"red"}, "cool": {"red"}},
            {"red": {"deep", "cool"}}
        )
        result = build_tone_modifier_mappings(["cool deep red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = (
            {"blue"},
            {"deep"},
            {"deep": {"blue"}},
            {"blue": {"deep"}}
        )
        result = build_tone_modifier_mappings(["deep blue"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = (
            {"green"},
            {"light", "cool"},
            {"light": {"green"}, "cool": {"green"}},
            {"green": {"light", "cool"}}
        )
        result = build_tone_modifier_mappings(["cool light green"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = (
            {"orange"},
            {"bright"},
            {"bright": {"orange"}},
            {"orange": {"bright"}}
        )
        result = build_tone_modifier_mappings(["bright orange"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = (
            {"lavender", "beige"},
            {"soft", "cool"},
            {"soft": {"lavender"}, "cool": {"beige"}},
            {"lavender": {"soft"}, "beige": {"cool"}}
        )
        result = build_tone_modifier_mappings(["soft lavender", "cool beige"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = (
            {"pink"},
            {"muted"},
            {"muted": {"pink"}},
            {"pink": {"muted"}}
        )
        result = build_tone_modifier_mappings(["muted pink"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = (
            {"red", "blue", "yellow"},
            {"bright"},
            {"bright": {"red", "blue", "yellow"}},
            {"red": {"bright"}, "blue": {"bright"}, "yellow": {"bright"}}
        )
        result = build_tone_modifier_mappings(
            ["bright red", "bright blue", "bright yellow"], self.known_tones, self.known_modifiers
        )
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = (
            {"peach"},
            {"dusty"},
            {"dusty": {"peach"}},
            {"peach": {"dusty"}}
        )
        result = build_tone_modifier_mappings(["dusty peach"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = (
            {"brown"},
            {"rich"},
            {"rich": {"brown"}},
            {"brown": {"rich"}}
        )
        result = build_tone_modifier_mappings(["rich brown"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = (
            {"nude"},
            {"soft", "warm"},
            {"soft": {"nude"}, "warm": {"nude"}},
            {"nude": {"soft", "warm"}}
        )
        result = build_tone_modifier_mappings(["soft warm nude"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = (
            {"red"},
            {"bright"},
            {"bright": {"red"}},
            {"red": {"bright"}}
        )
        result = build_tone_modifier_mappings(["bright red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = (
            {"pink", "peach"},
            {"warm", "muted"},
            {"warm": {"pink"}, "muted": {"peach"}},
            {"pink": {"warm"}, "peach": {"muted"}}
        )
        result = build_tone_modifier_mappings(["warm pink", "muted peach"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = (
            {"gray"},
            {"cool"},
            {"cool": {"gray"}},
            {"gray": {"cool"}}
        )
        result = build_tone_modifier_mappings(["cool gray"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = (
            {"blue"},
            set(),
            {},
            {}
        )
        result = build_tone_modifier_mappings(["deepest blue"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = (
            set(),
            {"neutral"},
            {},
            {}
        )
        result = build_tone_modifier_mappings(["neutral vibe"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = (
            {"blue", "gray"},
            {"dusty"},
            {"dusty": {"blue", "gray"}},
            {"blue": {"dusty"}, "gray": {"dusty"}}
        )
        result = build_tone_modifier_mappings(["dusty blue", "dusty gray"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = (
            {"rose"},
            {"warm"},
            {"warm": {"rose"}},
            {"rose": {"warm"}}
        )
        result = build_tone_modifier_mappings(["warm rose"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = (
            {"orange"},
            {"bold", "deep"},
            {"bold": {"orange"}, "deep": {"orange"}},
            {"orange": {"bold", "deep"}}
        )
        result = build_tone_modifier_mappings(["deep bold orange"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = (
            {"yellow"},
            {"light", "cool"},
            {"light": {"yellow"}, "cool": {"yellow"}},
            {"yellow": {"light", "cool"}}
        )
        result = build_tone_modifier_mappings(["cool light yellow"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = (
            {"pink", "coral"},
            {"bold"},
            {"bold": {"pink", "coral"}},
            {"pink": {"bold"}, "coral": {"bold"}}
        )
        result = build_tone_modifier_mappings(["bold pink", "bold coral"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = (
            {"red"},
            {"bright"},
            {"bright": {"red"}},
            {"red": {"bright"}}
        )
        result = build_tone_modifier_mappings(["bright red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)


    def test_case_31(self):
        expected = (
            {"green"},
            {"muted"},
            {"muted": {"green"}},
            {"green": {"muted"}}
        )
        result = build_tone_modifier_mappings(["muted green"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = (
            {"red"},
            {"bold", "bright"},
            {"bold": {"red"}, "bright": {"red"}},
            {"red": {"bold", "bright"}}
        )
        result = build_tone_modifier_mappings(["bold bright red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = (
            {"beige"},
            {"soft", "cool"},
            {"soft": {"beige"}, "cool": {"beige"}},
            {"beige": {"soft", "cool"}}
        )
        result = build_tone_modifier_mappings(["cool soft beige"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = (
            {"brown"},
            {"deep"},
            {"deep": {"brown"}},
            {"brown": {"deep"}}
        )
        result = build_tone_modifier_mappings(["deep brown"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = (
            set(),
            set(),
            {},
            {}
        )
        result = build_tone_modifier_mappings(["random phrase"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = (
            {"pink", "beige"},
            {"soft"},
            {"soft": {"pink", "beige"}},
            {"pink": {"soft"}, "beige": {"soft"}}
        )
        result = build_tone_modifier_mappings(["soft pink", "soft beige"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = (
            {"blue"},
            {"warm"},
            {"warm": {"blue"}},
            {"blue": {"warm"}}
        )
        result = build_tone_modifier_mappings(["warm blue"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = (
            {"coral", "peach", "rose"},
            {"light"},
            {"light": {"coral", "peach", "rose"}},
            {"coral": {"light"}, "peach": {"light"}, "rose": {"light"}}
        )
        result = build_tone_modifier_mappings(["light coral", "light peach", "light rose"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = (
            {"red"},
            {"soft"},
            {"soft": {"red"}},
            {"red": {"soft"}}
        )
        result = build_tone_modifier_mappings(["soft red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = (
            {"nude", "beige"},
            {"warm"},
            {"warm": {"nude", "beige"}},
            {"nude": {"warm"}, "beige": {"warm"}}
        )
        result = build_tone_modifier_mappings(["warm nude", "warm beige"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = (
            {"red", "pink"},
            {"deep"},
            {"deep": {"red", "pink"}},
            {"red": {"deep"}, "pink": {"deep"}}
        )
        result = build_tone_modifier_mappings(["deep red", "deep pink"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = (
            {"red"},
            {"bright"},
            {"bright": {"red"}},
            {"red": {"bright"}}
        )
        result = build_tone_modifier_mappings(["very bright red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = (
            {"blue", "green"},
            {"muted"},
            {"muted": {"blue", "green"}},
            {"blue": {"muted"}, "green": {"muted"}}
        )
        result = build_tone_modifier_mappings(["muted blue", "muted green"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = (
            {"orange"},
            {"soft"},
            {"soft": {"orange"}},
            {"orange": {"soft"}}
        )
        result = build_tone_modifier_mappings(["orange soft"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = (
            {"green"},
            {"cool"},
            {"cool": {"green"}},
            {"green": {"cool"}}
        )
        result = build_tone_modifier_mappings(["green cool"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = (
            {"blue"},
            {"bold", "deep"},
            {"bold": {"blue"}, "deep": {"blue"}},
            {"blue": {"bold", "deep"}}
        )
        result = build_tone_modifier_mappings(["bold deep blue"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = (
            {"red", "pink", "brown"},
            {"dusty"},
            {"dusty": {"red", "pink", "brown"}},
            {"red": {"dusty"}, "pink": {"dusty"}, "brown": {"dusty"}}
        )
        result = build_tone_modifier_mappings(["dusty red", "dusty pink", "dusty brown"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = (
            {"blue"},
            {'icy'},
            {'icy': {'blue'}},
            {'blue': {'icy'}}
        )
        result = build_tone_modifier_mappings(["icy blue"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = (
            {"red"},
            {'deep', 'rich', 'vibrant'},
            {'deep': {'red'},
             'rich': {'red'},
             'vibrant': {'red'}}
            ,
            {'red': {'deep', 'rich', 'vibrant'}}
        )
        result = build_tone_modifier_mappings(["rich deep vibrant red"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = (
            set(),
            set(),
            {},
            {}
        )
        result = build_tone_modifier_mappings(["elegant timeless"], self.known_tones, self.known_modifiers)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
