# Chatbot/tests/extractors/color/extraction/test_extract_from_adjacent.py

import unittest
import spacy
from Chatbot.extractors.color.extraction.compound import extract_from_adjacent
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()

class TestExtractFromAdjacent(unittest.TestCase):

    def run_case(self, text, expected):
        tokens = nlp(text)
        compounds = set()
        raw_compounds = []
        extract_from_adjacent(tokens, compounds, raw_compounds, known_modifiers, known_tones, debug=True)
        self.assertEqual(expected, compounds, f"\nActual:   {compounds}\nExpected: {expected}")

    def test_case_01(self): self.run_case("soft pink", {"soft pink"})
    def test_case_02(self): self.run_case("muted beige", {"muted beige"})
    def test_case_03(self): self.run_case("light lavender", {"light lavender"})
    def test_case_04(self): self.run_case("deep rose", {"deep rose"})
    def test_case_05(self): self.run_case("warm coral", {"warm coral"})
    def test_case_06(self): self.run_case("cool taupe", {"cool taupe"})
    def test_case_07(self): self.run_case("dark green", {"dark green"})
    def test_case_08(self): self.run_case("dusty pink", {"dust pink"})
    def test_case_09(self): self.run_case("bright red", {"bright red"})
    def test_case_10(self): self.run_case("neutral nude", {"neutral nude"})
    def test_case_11(self): self.run_case("peachy pink", set())
    def test_case_12(self): self.run_case("soft elegant", set())
    def test_case_13(self): self.run_case("muted", set())
    def test_case_14(self): self.run_case("beige", set())
    def test_case_15(self): self.run_case("soft pink soft pink", {"soft pink"})
    def test_case_16(self): self.run_case("cool soft pink", {"soft pink"})
    def test_case_17(self): self.run_case("light light blue", {"light blue"})
    def test_case_18(self): self.run_case("soft pinky beige", {'soft pinky', 'pinky beige'})
    def test_case_19(self): self.run_case("bright light white", {"light white"})
    def test_case_20(self): self.run_case("moody lavender", set())
    def test_case_21(self): self.run_case("faded blush", {"faded blush"})
    def test_case_22(self): self.run_case("gentle mauve", set())
    def test_case_23(self): self.run_case("rich emerald", {"rich emerald"})
    def test_case_24(self): self.run_case("clear turquoise", {"clear turquoise"})
    def test_case_25(self): self.run_case("velvety rose", {"velvet rose"})
    def test_case_26(self): self.run_case("soft soft soft pink", {"soft pink"})
    def test_case_27(self): self.run_case("soft-pink", set())
    def test_case_28(self): self.run_case("intense sky blue", {"intense sky", "sky blue"})
    def test_case_29(self): self.run_case("blue soft", set())
    def test_case_30(self): self.run_case("deep deep rose", {"deep rose"})
    def test_case_31(self): self.run_case("green mint", {"green mint"})
    def test_case_32(self): self.run_case("gray stormy", set())
    def test_case_33(self): self.run_case("subtle honey", set())
    def test_case_34(self): self.run_case("icy cool lavender", {"cool lavender"})
    def test_case_35(self): self.run_case("delicate beige soft pink", {"soft pink"})
    def test_case_36(self): self.run_case("light night", set())  # BLOCKED_TOKENS
    def test_case_37(self): self.run_case("romantic dramatic", set())  # BLOCKED_TOKENS
    def test_case_38(self): self.run_case("night light", set())
    def test_case_39(self): self.run_case("vivid neon pink", {"neon pink"})
    def test_case_40(self): self.run_case("classic navy", {"classic navy"})
    def test_case_41(self): self.run_case("frosty mint",set())
    def test_case_42(self): self.run_case("creamy ivory", {"cream ivory"})
    def test_case_43(self): self.run_case("shiny copper", {"shiny copper"})
    def test_case_44(self): self.run_case("midnight blue", {"midnight blue"})
    def test_case_45(self): self.run_case("airy lilac", set())
    def test_case_46(self): self.run_case("dusky teal", set())
    def test_case_47(self): self.run_case("barely there pink", set())  # only if "barely" is modifier
    def test_case_48(self): self.run_case("bare pink tones", {"bare pink"})
    def test_case_49(self): self.run_case("true olive", set())
    def test_case_50(self): self.run_case("ultra rich plum", {"rich plum"})

