#Chatbot/tests/extractors/color/color_segment_logic/test_aggregate_results.py

import unittest
import os
import json
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.extract.color_segment_logic import aggregate_results

class TestAggregateResults(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.abspath(__file__)
        while not current_dir.endswith("pythonProject1"):
            current_dir = os.path.dirname(current_dir)
        path = os.path.join(current_dir, "Data", "known_modifiers.json")
        with open(path, "r", encoding="utf-8") as f:
            cls.known_modifiers = set(json.load(f))

        cls.rgb_map = {
            "red": (255, 0, 0),
            "pink": (255, 192, 203),
            "peach": (255, 218, 185),
            "beige": (245, 245, 220),
            "nude": (205, 180, 155),
            "coral": (255, 127, 80),
            "blue": (0, 0, 255),
            "green": (0, 128, 0)
        }

    def test_case_01(self):
        expected = ({"pink"}, ["soft pink"], {"soft pink": (255, 192, 203)})
        result = aggregate_results(["soft pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = ({"red"}, ["bright red"], {"bright red": (255, 0, 0)})
        result = aggregate_results(["bright red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = ({"peach"}, ["muted peach"], {"muted peach": (255, 218, 185)})
        result = aggregate_results(["muted peach"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = ({"beige"}, ["warm beige"], {"warm beige": (245, 245, 220)})
        result = aggregate_results(["warm beige"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = ({"nude"}, ["cool nude"], {"cool nude": (205, 180, 155)})
        result = aggregate_results(["cool nude"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = ({"coral"}, ["bold coral"], {"bold coral": (255, 127, 80)})
        result = aggregate_results(["bold coral"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = (
            {"pink"},
            ["light pink", "soft pink"],
            {"light pink": (255, 192, 203), "soft pink": (255, 192, 203)}
        )
        result = aggregate_results(["light pink", "soft pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = (
            {"red", "blue"},
            ["bright red", "cool blue"],
            {"bright red": (255, 0, 0), "cool blue": (0, 0, 255)}
        )
        result = aggregate_results(["bright red", "cool blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = ({"green"}, ["green"], {"green": (0, 128, 0)})
        result = aggregate_results(["green"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = (
            {"pink", "red", "nude"},
            ["soft pink", "bright red", "cool nude"],
            {
                "soft pink": (255, 192, 203),
                "bright red": (255, 0, 0),
                "cool nude": (205, 180, 155)
            }
        )
        result = aggregate_results(["soft pink", "bright red", "cool nude"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = (
            {"red"},
            ["deep red"],
            {"deep red": (255, 0, 0)}
        )
        result = aggregate_results(["deep red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = (
            {"green"},
            ["cool light green"],
            {"cool light green": (0, 128, 0)}
        )
        result = aggregate_results(["cool light green"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = (
            {"orange"},
            ["bright orange"],
            {"bright orange": self.rgb_map.get("orange", (255, 165, 0))}
        )
        result = aggregate_results(["bright orange"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("bright orange", result[1])
        self.assertIn("orange", result[0])

    def test_case_14(self):
        expected = (
            {"beige", "lavender"},
            ["soft lavender", "cool beige"],
            {
                "soft lavender": self.rgb_map.get("lavender", (230, 230, 250)),
                "cool beige": (245, 245, 220)
            }
        )
        result = aggregate_results(["soft lavender", "cool beige"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("soft lavender", result[1])
        self.assertIn("cool beige", result[1])

    def test_case_15(self):
        expected = (
            {"pink"},
            ["muted pink"],
            {"muted pink": (255, 192, 203)}
        )
        result = aggregate_results(["muted pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = (
            {"yellow", "red", "blue"},
            ["bright yellow", "bright red", "bright blue"],
            {
                "bright yellow": self.rgb_map.get("yellow", (255, 255, 0)),
                "bright red": (255, 0, 0),
                "bright blue": (0, 0, 255)
            }
        )
        result = aggregate_results(["bright yellow", "bright red", "bright blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("bright red", result[1])
        self.assertIn("bright blue", result[1])

    def test_case_17(self):
        expected = (
            {"peach"},
            ["dusty peach"],
            {"dusty peach": (255, 218, 185)}
        )
        result = aggregate_results(["dusty peach"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = (
            {"brown"},
            ["rich brown"],
            {"rich brown": self.rgb_map.get("brown", (165, 42, 42))}
        )
        result = aggregate_results(["rich brown"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("rich brown", result[1])
        self.assertIn("brown", result[0])

    def test_case_19(self):
        expected = (
            {"nude"},
            ["soft warm nude"],
            {"soft warm nude": (205, 180, 155)}
        )
        result = aggregate_results(["soft warm nude"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = (
            {"pink", "peach"},
            ["warm pink", "muted peach"],
            {
                "warm pink": (255, 192, 203),
                "muted peach": (255, 218, 185)
            }
        )
        result = aggregate_results(["warm pink", "muted peach"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = (
            {"gray"},
            ["cool gray"],
            {"cool gray": self.rgb_map.get("gray", (128, 128, 128))}
        )
        result = aggregate_results(["cool gray"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("cool gray", result[1])

    def test_case_22(self):
        expected = (
            {"blue"},
            ["deepest blue"],
            {"deepest blue": (0, 0, 255)}
        )
        result = aggregate_results(["deepest blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("deepest blue", result[1])

    def test_case_23(self):
        expected = (
            {"blue", "gray"},
            ["dusty blue", "dusty gray"],
            {
                "dusty blue": (0, 0, 255),
                "dusty gray": self.rgb_map.get("gray", (128, 128, 128))
            }
        )
        result = aggregate_results(["dusty blue", "dusty gray"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(set(result[0]), {"blue", "gray"})

    def test_case_24(self):
        expected = (
            {"rose"},
            ["warm rose"],
            {"warm rose": self.rgb_map.get("rose", (255, 102, 204))}
        )
        result = aggregate_results(["warm rose"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("warm rose", result[1])

    def test_case_25(self):
        expected = (
            {"orange"},
            ["deep bold orange"],
            {"deep bold orange": self.rgb_map.get("orange", (255, 165, 0))}
        )
        result = aggregate_results(["deep bold orange"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("deep bold orange", result[1])

    def test_case_26(self):
        expected = (
            {"yellow"},
            ["cool light yellow"],
            {"cool light yellow": self.rgb_map.get("yellow", (255, 255, 0))}
        )
        result = aggregate_results(["cool light yellow"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("cool light yellow", result[1])

    def test_case_27(self):
        expected = (
            {"pink", "coral"},
            ["bold pink", "bold coral"],
            {
                "bold pink": (255, 192, 203),
                "bold coral": (255, 127, 80)
            }
        )
        result = aggregate_results(["bold pink", "bold coral"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(set(result[0]), {"pink", "coral"})

    def test_case_28(self):
        expected = (
            {"red"},
            ["brightest red"],
            {"brightest red": (255, 0, 0)}
        )
        result = aggregate_results(["brightest red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("brightest red", result[1])

    def test_case_29(self):
        expected = (
            {"blue"},
            ["bold deep blue"],
            {"bold deep blue": (0, 0, 255)}
        )
        result = aggregate_results(["bold deep blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("bold deep blue", result[1])

    def test_case_30(self):
        expected = (
            {"pink", "brown", "red"},
            ["dusty pink", "dusty brown", "dusty red"],
            {
                "dusty pink": (255, 192, 203),
                "dusty brown": self.rgb_map.get("brown", (165, 42, 42)),
                "dusty red": (255, 0, 0)
            }
        )
        result = aggregate_results(["dusty pink", "dusty brown", "dusty red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(set(result[0]), {"pink", "brown", "red"})

    def test_case_31(self):
        expected = (
            {"orange"},
            ["orange soft"],
            {"orange soft": self.rgb_map.get("orange", (255, 165, 0))}
        )
        result = aggregate_results(["orange soft"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("orange soft", result[1])

    def test_case_32(self):
        expected = (
            {"green"},
            ["green cool"],
            {"green cool": (0, 128, 0)}
        )
        result = aggregate_results(["green cool"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("green cool", result[1])

    def test_case_33(self):
        expected = (
            {"blue"},
            ["cool deep blue"],
            {"cool deep blue": (0, 0, 255)}
        )
        result = aggregate_results(["cool deep blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("cool deep blue", result[1])

    def test_case_34(self):
        expected = (
            {"pink"},
            ["pink"],
            {"pink": (255, 192, 203)}
        )
        result = aggregate_results(["pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = (
            set(),
            ["elegant timeless"],
            {}
        )
        result = aggregate_results(["elegant timeless"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = (
            {"gray"},
            ["dusty gray"],
            {"dusty gray": self.rgb_map.get("gray", (128, 128, 128))}
        )
        result = aggregate_results(["dusty gray"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("gray", result[0])

    def test_case_37(self):
        expected = (
            {"green"},
            ["icy green"],
            {"icy green": (0, 128, 0)}
        )
        result = aggregate_results(["icy green"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("icy green", result[1])

    def test_case_38(self):
        expected = (
            {"red"},
            ["rich deep vibrant red"],
            {"rich deep vibrant red": (255, 0, 0)}
        )
        result = aggregate_results(["rich deep vibrant red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("rich deep vibrant red", result[1])

    def test_case_39(self):
        expected = (
            {"nude"},
            ["nude"],
            {"nude": (205, 180, 155)}
        )
        result = aggregate_results(["nude"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = (
            {"beige"},
            ["beige"],
            {"beige": (245, 245, 220)}
        )
        result = aggregate_results(["beige"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = (
            {"red"},
            ["red", "deep red"],
            {"red": (255, 0, 0), "deep red": (255, 0, 0)}
        )
        result = aggregate_results(["red", "deep red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("red", result[0])

    def test_case_42(self):
        expected = (
            {"blue"},
            ["blue"],
            {"blue": (0, 0, 255)}
        )
        result = aggregate_results(["blue"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = (
            {"brown"},
            ["brown"],
            {"brown": self.rgb_map.get("brown", (165, 42, 42))}
        )
        result = aggregate_results(["brown"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = (
            {"green", "pink"},
            ["green", "pink"],
            {"green": (0, 128, 0), "pink": (255, 192, 203)}
        )
        result = aggregate_results(["green", "pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = (
            {"coral"},
            ["coral"],
            {"coral": (255, 127, 80)}
        )
        result = aggregate_results(["coral"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = (
            {"red", "pink"},
            ["bold red", "soft pink"],
            {"bold red": (255, 0, 0), "soft pink": (255, 192, 203)}
        )
        result = aggregate_results(["bold red", "soft pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = (
            {"peach", "pink", "brown"},
            ["peach", "pink", "brown"],
            {
                "peach": (255, 218, 185),
                "pink": (255, 192, 203),
                "brown": self.rgb_map.get("brown", (165, 42, 42))
            }
        )
        result = aggregate_results(["peach", "pink", "brown"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(set(result[0]), {"peach", "pink", "brown"})

    def test_case_48(self):
        expected = (
            {"red"},
            ["very bright red"],
            {"very bright red": (255, 0, 0)}
        )
        result = aggregate_results(["very bright red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertIn("very bright red", result[1])

    def test_case_49(self):
        expected = (
            {"red", "pink"},
            ["red", "pink"],
            {"red": (255, 0, 0), "pink": (255, 192, 203)}
        )
        result = aggregate_results(["red", "pink"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = (
            {"pink", "coral", "peach", "red"},
            ["soft pink", "bold coral", "light peach", "bright red"],
            {
                "soft pink": (255, 192, 203),
                "bold coral": (255, 127, 80),
                "light peach": (255, 218, 185),
                "bright red": (255, 0, 0)
            }
        )
        result = aggregate_results(["soft pink", "bold coral", "light peach", "bright red"], known_tones, self.known_modifiers, self.rgb_map)
        self.assertEqual(set(result[0]), {"pink", "coral", "peach", "red"})

if __name__ == "__main__":
    unittest.main()
