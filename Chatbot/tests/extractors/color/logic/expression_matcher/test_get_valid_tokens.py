import unittest
import spacy
from typing import List
from Chatbot.extractors.color.logic.expression_matcher import get_valid_tokens
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir  # assumes your standard loader
from spacy.tokens import Token

class TestGetValidTokens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expression_map = load_json_from_data_dir("expression_definition.json")
        cls.nlp = spacy.load("en_core_web_sm")

    def run_test(self, text: str, expected: List[str]):
        doc = self.nlp(text)
        result = get_valid_tokens(list(doc), self.expression_map)
        self.assertEqual(result, expected)

    def test_case_01(self): self.run_test("This is soft", ["soft"])
    def test_case_02(self): self.run_test("This is shiny", ["shiny"])
    def test_case_03(self): self.run_test("I want soft and shiny things", ["soft", "shiny"])
    def test_case_04(self): self.run_test("Neutral pink is my favorite", ["neutral"])
    def test_case_05(self): self.run_test("I prefer vibrant red", ["vibrant"])
    def test_case_06(self): self.run_test("I love subtle makeup", ["subtle"])
    def test_case_07(self): self.run_test("This tone is elegant", ["elegant"])
    def test_case_08(self): self.run_test("I like bold looks", ["bold"])
    def test_case_09(self): self.run_test("Natural style suits me", ["natural"])
    def test_case_10(self): self.run_test("Dramatic styles are great", ["dramatic"])

    def test_case_11(self): self.run_test("A classic pink lipstick", ["classic"])
    def test_case_12(self): self.run_test("Glossy lips are nice", ["glossy"])
    def test_case_13(self): self.run_test("A matte finish is preferred", ["matte"])
    def test_case_14(self): self.run_test("She wore a romantic shade", ["romantic"])
    def test_case_15(self): self.run_test("This is a playful tone", ["playful"])
    def test_case_16(self): self.run_test("Soft glam is trending", ["soft", "glam"])
    def test_case_17(self): self.run_test("Ultra light foundation is best", ["light"])
    def test_case_18(self): self.run_test("A deep purple tone", ["deep"])
    def test_case_19(self): self.run_test("Cool undertones work well", ["cool"])
    def test_case_20(self): self.run_test("Warm colors look better on me", ["warm"])

    def test_case_21(self): self.run_test("Shiny skin is in", ["shiny"])
    def test_case_22(self): self.run_test("Elegant design feels luxurious", ["elegant"])
    def test_case_23(self): self.run_test("Glowy skin products", ["glowy"])
    def test_case_24(self): self.run_test("Muted shades look classy", ["muted"])
    def test_case_25(self): self.run_test("Bold red lipstick", ["bold"])
    def test_case_26(self): self.run_test("Minimalist makeup is trending", ["minimalist"])
    def test_case_27(self): self.run_test("Gentle tones only", ["gentle"])
    def test_case_28(self): self.run_test("Refined pink finish", ["refined"])
    def test_case_29(self): self.run_test("Rustic tones for fall", ["rustic"])
    def test_case_30(self): self.run_test("Classic glam is timeless", ["classic", "glam", "timeless"])

    def test_case_31(self): self.run_test("Tropical tones are back", ["tropical"])
    def test_case_32(self): self.run_test("Playful blush is in", ["playful"])
    def test_case_33(self): self.run_test("Modern yet elegant", ["elegant"])
    def test_case_34(self): self.run_test("I use shiny and glossy highlighter", ["shiny", "glossy"])
    def test_case_35(self): self.run_test("She chose matte and muted colors", ["matte", "muted"])
    def test_case_36(self): self.run_test("He wants a neutral base", ["neutral"])
    def test_case_37(self): self.run_test("Only subtle pinks today", ["subtle"])
    def test_case_38(self): self.run_test("Is that a bold or dramatic look?", ["bold", "dramatic"])
    def test_case_39(self): self.run_test("Nothing too flashy", ["flashy"])
    def test_case_40(self): self.run_test("Too strong for a daytime look", ["daytime"])

    def test_case_41(self): self.run_test("A glamorous finish", ["glamorous"])
    def test_case_42(self): self.run_test("Satin skin is flawless", ["satin"])
    def test_case_43(self): self.run_test("Moist and dewy skin", ["dewy"])
    def test_case_44(self): self.run_test("Cool-toned blush", ["cool"])
    def test_case_45(self): self.run_test("Warm-neutral base", ["warm", "neutral"])
    def test_case_46(self): self.run_test("The classic romantic pink", ["classic", "romantic"])
    def test_case_47(self): self.run_test("Evening tones only", ["evening"])
    def test_case_48(self): self.run_test("Daytime makeup works well", ["daytime"])
    def test_case_49(self): self.run_test("Soft matte base", ["soft", "matte"])
    def test_case_50(self): self.run_test("Deep tone with natural finish", ["deep", "natural"])
