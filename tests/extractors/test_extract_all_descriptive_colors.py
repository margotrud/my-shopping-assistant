from Chatbot.extractors.colors import extract_all_descriptive_color_phrases
import unittest
import webcolors
from matplotlib.colors import XKCD_COLORS
from pathlib import Path
import json

# Load known modifiers from Data/modifiers.json
BASE_DIR = Path(__file__).resolve().parents[2]
MODIFIERS_PATH = BASE_DIR / "Data" / "known_modifiers.json"

with open(MODIFIERS_PATH, "r", encoding="utf-8") as f:
    known_modifiers = set(json.load(f))

# Load known tones from webcolors
css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())
known_tones = css_tones.union(xkcd_tones)

# === TEST CASES ===
class TestColorPhraseExtraction(unittest.TestCase):

    def test_case_01(self):
        input_text = "pink"
        expected = ["pink"]
        actual = extract_all_descriptive_color_phrases(input_text, known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_02(self):
        input_text = "soft pink"
        expected = ["soft pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_03(self):
        input_text = "bold red lipstick"
        expected = ["bold red"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_04(self):
        input_text = "deep peach blush"
        expected = ["blush", "deep peach"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_05(self):
        input_text = "I like soft tones"
        expected = ["soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_06(self):
        input_text = "warm colors"
        expected = ["warm"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_07(self):
        input_text = "muted pink blush"
        expected = ["muted pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_08(self):
        input_text = "I prefer coral"
        expected = ["coral"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_09(self):
        input_text = "cool tones"
        expected = ["cool"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_10(self):
        input_text = "soft blush"
        expected = ["soft blush"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_11(self):
        input_text = "I want something bright"
        expected = ["bright"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_12(self):
        input_text = "bright pink options"
        expected = ["bright pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_13(self):
        input_text = "nude and warm tones"
        expected = ["nude", "warm"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_14(self):
        input_text = "deep red or soft pink"
        expected = ["deep red", "soft pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_15(self):
        input_text = "not too bright pink"
        expected = ["bright pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_16(self):
        input_text = "cool pink tones"
        expected = ["cool pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_17(self):
        input_text = "show me peach blush"
        expected = ["peach"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_18(self):
        input_text = "a soft pink lipstick"
        expected = ["soft pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_19(self):
        input_text = "warm beige foundation"
        expected = ["warm beige"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_20(self):
        input_text = "something deep and dark like brown"
        expected = ['brown', 'dark', 'deep']
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_21(self):
        input_text = "muted tones please"
        expected = ["muted"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_22(self):
        input_text = "I like brown but also soft pinks"
        expected = ["brown", "soft pinks"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_23(self):
        input_text = "not purple, just muted blush"
        expected = ["muted blush", "purple"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_24(self):
        input_text = "I'd love something like bright red or soft peach"
        expected = ["bright red", "soft peach"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_25(self):
        input_text = "Give me warm beige, muted pinks, and bold red options"
        expected = ["bold red", "muted pinks", "warm beige"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_26(self):
        input_text = "Avoid bold red and go for soft pink"
        expected = ["bold red", "soft pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_27(self):
        input_text = "I'm interested in muted lipstick or warm blush"
        expected = ["muted", "warm blush"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_28(self):
        input_text = "bright lipstick and bright pink"
        expected = ["bright", "bright pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_29(self):
        input_text = "She dislikes bold red but wears soft beige"
        expected = ["bold red", "soft beige"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_30(self):
        input_text = "no cool tones but yes to warm coral"
        expected = ["cool", "warm coral"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_31(self):
        input_text = "I want warm lipstick and muted colors"
        expected = ["muted", "warm"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_32(self):
        input_text = "deep brown and soft blush are my favorite"
        expected = ["deep brown", "soft blush"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_33(self):
        input_text = "pink is nice but bright pink is too much"
        expected = ["bright pink", "pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_34(self):
        input_text = "cool red or cool pink"
        expected = ["cool pink", "cool red"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_35(self):
        input_text = "coral lipstick, soft tones, and bright blush"
        expected = ["bright blush", "coral", "soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_36(self):
        input_text = "I’m between muted pink and muted blush"
        expected = ["muted blush", "muted pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_37(self):
        input_text = "Go for soft, cool, or warm shades"
        expected = ["cool", "soft", "warm"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_38(self):
        input_text = "deep foundation and bright lipstick"
        expected = ["bright", "deep"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_39(self):
        input_text = "peachy pink and bright coral lipsticks"
        expected = ["bright coral", "peachy pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_40(self):
        input_text = "cool lipstick and pink foundation"
        expected = ["cool", "pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_41(self):
        input_text = "only muted brown and bright red"
        expected = ["bright red", "muted brown"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_42(self):
        input_text = "no bold colors, just soft tones"
        expected = ["bold", "soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_43(self):
        input_text = "muted blush, soft lipstick, bright tones"
        expected = ["bright", "muted blush", "soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_44(self):
        input_text = "I enjoy soft pinks and deep reds"
        expected = ["deep reds", "soft pinks"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_45(self):
        input_text = "bright red lipstick, warm blush and cool tones"
        expected = ["bright red", "cool", "warm blush"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_46(self):
        input_text = "go for muted lipstick or foundation in soft tones"
        expected = ["muted", "soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_47(self):
        input_text = "I don’t like warm coral or bold red"
        expected = ["bold red", "warm coral"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_48(self):
        input_text = "avoid red but I want soft lipstick"
        expected = ["red", "soft"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_49(self):
        input_text = "she likes cool beige or warm pink blush"
        expected = ["cool beige", "warm pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_50(self):
        input_text = "muted pink lipstick and muted pink blush"
        expected = ["muted pink"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)

    def test_case_51(self):
        input_text = "looking for a nude base"
        expected = ["nude"]
        actual = extract_all_descriptive_color_phrases(input_text,  known_tones,
                                                       known_modifiers, debug=True)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

