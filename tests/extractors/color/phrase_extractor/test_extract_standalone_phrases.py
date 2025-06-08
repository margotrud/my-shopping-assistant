# tests/extractors/color/phrase_extractor/test_extract_standalone.py

import unittest
import spacy
from collections import Counter
from Chatbot.extractors.color.extract.standalone_extraction import extract_standalone_phrases
from Chatbot.extractors.color import known_tones, all_webcolor_names
from Chatbot.extractors.color.core.matcher import load_known_modifiers
import Chatbot.extractors.color.extract.standalone_extraction as target_module
print("[🧪 TEST LOADED MODULE] →", target_module.__file__)
from Chatbot.extractors.color.extract.categorizer import load_expression_definitions


class TestExtractStandalonePhrases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()
        cls.known_tones = known_tones
        cls.webcolors = all_webcolor_names
        cls.hardcoded_blocked_nouns = {"lipstick", "blush"}
        cls.nlp = spacy.load("en_core_web_sm")
        cls.expression_definitions = load_expression_definitions()

    def expected_modifiers(self, *keys, extras=None):
        result = set()
        for key in keys:
            if key in self.expression_definitions:
                result.update(self.expression_definitions[key].get("modifiers", []))
        if extras:
            result.update(extras)
        return sorted(result)

    def run_test(self, text, expected, debug=True):
        doc = self.nlp(text.lower())
        tokens = list(doc)
        token_counts = Counter([t.text.lower() for t in tokens])
        result = extract_standalone_phrases(
            tokens=tokens,
            token_counts=token_counts,
            raw_compounds=[],
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers,
            all_webcolor_names=self.webcolors,
            hardcoded_blocked_nouns=self.hardcoded_blocked_nouns,
            debug=debug
        )
        self.assertEqual(sorted(expected), sorted(result))
    def test_case_01(self): self.run_test("I like soft colors", ["soft"])
    def test_case_02(self): self.run_test("Give me something bold", ["bold"])
    def test_case_03(self): self.run_test("I want pink lipstick", ["pink"])
    def test_case_04(self): self.run_test("She likes nude tones", ["nude"])
    def test_case_05(self): self.run_test("The dress is purple", ["purple"])
    def test_case_06(self): self.run_test("I like light and dark colors", ["light", "dark"])
    def test_case_07(self): self.run_test("I prefer coral blush", ["coral"])
    def test_case_08(self): self.run_test("Soft and romantic vibes", self.expected_modifiers("romantic", extras=["soft"]))
    def test_case_09(self): self.run_test("Muted pink with a beige touch", ["beige", "muted", "pink"])
    def test_case_10(self): self.run_test("I dislike bright shades", ["bright"])
    def test_case_11(self): self.run_test("Please avoid flashy, just keep it neutral", self.expected_modifiers("natural", extras=["flashy"]))

    def test_case_12(self): self.run_test("I enjoy earthy, golden tones", self.expected_modifiers("earthy", extras=["golden"]))

    def test_case_13(self): self.run_test("Subtle or intense?", ["intense", "subtle"])

    def test_case_14(self): self.run_test("Dreamy pastel pinks", ["dreamy", "pastel", "pinks"])

    def test_case_15(self): self.run_test("Some matte and clean options", self.expected_modifiers("clean", extras=["matte"]))

    def test_case_16(self): self.run_test("Anything skin-like", ["skin-like"])

    def test_case_17(self): self.run_test("Supernatural glow, not bold", ["bold", "glowy"])

    def test_case_18(self): self.run_test("bronzed elegance", self.expected_modifiers("elegance", extras=["bronzed"]))

    def test_case_19(self): self.run_test("Creamy tones", ["creamy"])

    def test_case_20(self): self.run_test("Nothing vibrant or flashy", ["flashy", "vibrant"])

    def test_case_21(self): self.run_test("Something mysterious and moody", ["mysterious", "moody"])

    def test_case_22(self): self.run_test("Elegant but edgy", self.expected_modifiers(["elegant", "edgy"]))

    def test_case_23(self): self.run_test("Simple and barely-there", ["bare"])

    def test_case_24(self): self.run_test("Classic yet romantic", ["classic", "romantic"])

    def test_case_25(self): self.run_test("Deep and electric colors", ["deep", "electric"])

    def test_case_26(self): self.run_test("Refined finish", ["refined"])

    def test_case_27(self): self.run_test("Soft shimmer", ["shimmery", "soft"])

    def test_case_28(self): self.run_test("Not too dewy", ["dewy"])

    def test_case_29(self): self.run_test("Rough and burned tones", ["burned", "rough"])

    def test_case_30(self): self.run_test("No glowy or shiny stuff", ["glowy", "shiny"])

    def test_case_31(self): self.run_test("Polished skin look", ["polished"])

    def test_case_32(self): self.run_test("Just light or airy tones", ["airy", "light"])

    def test_case_33(self): self.run_test("Soft and sensual", ["sensual", "soft"])

    def test_case_34(self): self.run_test("Metallic vibes", ["metallic"])

    def test_case_35(self): self.run_test("Nothing too dramatic", ["dramatic"])

    def test_case_36(self): self.run_test("Dusty tones with creamy overlay", ["creamy", "dusty"])

    def test_case_37(self): self.run_test("Muted and refined elegance", ["muted"])

    def test_case_38(self): self.run_test("Nude but bold", ["nude", "bold"])

    def test_case_39(self): self.run_test("Playful with romantic twist", ["playful", "romantic"])

    def test_case_40(self): self.run_test("Experimental but clean", ["clean", "experimental"])

    def test_case_41(self): self.run_test("Something timeless and elegant", ["timeless", "elegant"])

    def test_case_42(self): self.run_test("A barely-there effect", ["bare"])

    def test_case_43(self): self.run_test("Red carpet glam", ["glam"])

    def test_case_44(self): self.run_test("Glow and shine", ["glowy", "shiny"])

    def test_case_45(self): self.run_test("Subdued and earthy", ["subdued", "earthy"])

    def test_case_46(self): self.run_test("A dewy finish please", ["dewy"])

    def test_case_47(self): self.run_test("Dark but clean", ["dark", "clean"])

    def test_case_48(self): self.run_test("Neutral and polished tones", ["neutral", "polished"])

    def test_case_49(self): self.run_test("Skin-like or matte?", ["matte", "skin-like"])

    def test_case_50(self): self.run_test("Chic and refined look", ["chic", "refined"])


if __name__ == "__main__":
    unittest.main()
