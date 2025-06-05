# tests/extractors/color/test_extract_compounds.py

import unittest
import spacy
import json
from pathlib import Path
from Chatbot.extractors.color.phrase_extractor import _extract_compounds, singularize
from Chatbot.extractors.color import known_tones, all_webcolor_names

class TestExtractCompounds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("TestSetup")

        try:
            cls.nlp = spacy.load("en_core_web_sm")
            from Chatbot.extractors.color import known_tones, all_webcolor_names
            from Chatbot.extractors.color.matcher import load_known_modifiers

            cls.known_tones = known_tones
            cls.webcolors = all_webcolor_names
            cls.known_modifiers = load_known_modifiers()

            logger.debug(f"✅ Setup successful. Loaded {len(cls.known_modifiers)} modifiers.")
        except Exception as e:
            logger.error(f"❌ Failed to set up class: {e}")
            raise

    def run_test(self, text, expected, debug=False):
        tokens = list(self.nlp(text))
        result, _ = _extract_compounds(
            tokens,
            self.known_tones,
            self.known_modifiers,
            self.webcolors,
            debug=debug
        )
        print(f"\n[🧪 DEBUG TEST] TEXT: {text}")
        print(f"[✅ EXPECTED COMPOUNDS] → {set(expected)}")
        print(f"[📦 RETURNED COMPOUNDS] → {result}")
        self.assertEqual(set(expected), result)

    def test_case_01(self): self.run_test("soft pink", ["soft pink"], debug = True)
    def test_case_02(self): self.run_test("bold red", ["bold red"], debug = True)
    def test_case_03(self): self.run_test("bright peach", ["bright peach"], debug = True)
    def test_case_04(self): self.run_test("deep green", ["deep green"], debug = True)
    def test_case_05(self): self.run_test("muted coral", ["muted coral"], debug = True)
    def test_case_06(self): self.run_test("soft lightblue", ["soft lightblue"], debug = True)
    def test_case_07(self): self.run_test("bright darkred", ["bright darkred"], debug = True)
    def test_case_08(self): self.run_test("muted lavender", ["muted lavender"], debug = True)
    def test_case_09(self): self.run_test("soft red soft pink", ["soft red", "soft pink"], debug = True)
    def test_case_10(self): self.run_test("bold red and soft pink", ["bold red", "soft pink"], debug = True)
    def test_case_11(self): self.run_test("I love soft pink and bold red.", ["soft pink", "bold red"], debug = True)
    def test_case_12(self): self.run_test("Try muted coral, soft green, and deep beige.", ['deep beige', 'soft green', 'muted coral'], debug = True)
    def test_case_13(self): self.run_test("soft apples and muted grapes", ['soft apple', 'muted grape'], debug = True)
    def test_case_14(self): self.run_test("softish pink and soft blue", ['soft pink', 'soft blue'], debug = True)
    def test_case_15(self): self.run_test("deepblue or brightred", ["deep blue", "bright red"], debug = True)
    def test_case_16(self): self.run_test("soft pinks", ["soft pink"], debug = True)
    def test_case_17(self): self.run_test("bright reds", ["bright red"], debug = True)
    def test_case_18(self): self.run_test("soft green, soft greens", ["soft green"], debug = True)
    def test_case_19(self): self.run_test("bold reds and bold red", ["bold red"], debug = True)
    def test_case_20(self): self.run_test("muted lavenders", ["muted lavender"], debug = True)
    def test_case_21(self): self.run_test("soft pink soft pink soft pink", ["soft pink"], debug = True)
    def test_case_22(self): self.run_test("muted lavender lavender muted", ["muted lavender"], debug = True)
    def test_case_23(self): self.run_test("soft pink blush", ["soft pink"], debug = True)
    def test_case_24(self): self.run_test("the bright green bag", ["bright green"], debug = True)
    def test_case_25(self): self.run_test("muted coral shoes", ["muted coral"], debug = True)
    def test_case_26(self): self.run_test("deep deep pink", ["deep pink"], debug = True)
    def test_case_27(self): self.run_test("deep soft green", ["soft green"], debug = True)
    def test_case_28(self): self.run_test("bright blue deep red soft peach", ['soft peach', 'bright blue', 'deep red'], debug = True)
    def test_case_29(self): self.run_test("muted coral pink", ["muted coral"], debug = True)
    def test_case_30(self): self.run_test("the bold and bright red", ["bright red"], debug = True)
    def test_case_31(self): self.run_test("muted coral coral muted", ["muted coral"], debug = True)
    def test_case_32(self): self.run_test("soft green, deep green, bright green", ['deep green', 'soft green', 'bright green'], debug = True)
    def test_case_33(self): self.run_test("deep-red soft-pink", ["deep red", "soft pink"], debug = True)
    def test_case_34(self): self.run_test("soft pinkish", ['soft pinkish'], debug = True)
    def test_case_35(self): self.run_test("bright pink, soft pink, bold pink", ["bright pink", "soft pink", "bold pink"], debug = True)
    def test_case_36(self): self.run_test("soft lightblue, muted lavender", ["soft lightblue", "muted lavender"], debug = True)
    def test_case_37(self): self.run_test("muted coral lipgloss", ["muted coral"], debug = True)
    def test_case_38(self): self.run_test("soft pink shoes muted lavender lips", ["soft pink", "muted lavender"], debug = True)
    def test_case_39(self): self.run_test("bright lightblue eyeshadow", ["bright lightblue"], debug = True)
    def test_case_40(self): self.run_test("nude soft pink", ["soft pink"], debug = True)
    def test_case_41(self): self.run_test("very soft pink", ['soft pink'], debug = True)
    def test_case_42(self): self.run_test("ultra deep red", ["deep red"], debug = True)
    def test_case_43(self): self.run_test("too bright pink", ["bright pink"], debug = True)
    def test_case_44(self): self.run_test("super muted coral", ["muted coral"], debug = True)
    def test_case_45(self): self.run_test("soft muted pink", ["muted pink"], debug = True)
    def test_case_46(self): self.run_test("deep peachy blush", ["deep peach"], debug = True)
    def test_case_47(self): self.run_test("bold lavender dress", ["bold lavender"], debug = True)
    def test_case_48(self): self.run_test("deep beige or soft peachy", ["deep beige","soft peachy"], debug = True)
    def test_case_49(self): self.run_test("soft darkred vs bright coral", ["soft darkred", "bright coral"], debug = True)
    def test_case_50(self): self.run_test("really like soft pink but not bright red", ["soft pink", "bright red"], debug = True)
