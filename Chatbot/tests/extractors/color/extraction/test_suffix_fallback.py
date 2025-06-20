# Chatbot/tests/extractors/color/extraction/test_suffix_fallback.py

import unittest
import spacy
from unittest.mock import patch
from Chatbot.extractors.color.extraction.suffix_fallback import extract_suffix_fallbacks
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names

nlp = spacy.load("en_core_web_sm")
known_mods = load_known_modifiers()

class TestExtractSuffixFallbacks(unittest.TestCase):

    def run_case(self, text, expected, simplified_result=None):
        tokens = nlp(text)
        with patch("Chatbot.extractors.color.extraction.suffix_fallback.simplify_phrase_if_needed",
                   return_value=simplified_result):
            result = extract_suffix_fallbacks(tokens, known_tones, known_mods, all_webcolor_names, debug=True)
            self.assertEqual(expected, result)

    def test_case_01(self): self.run_case("peachy", ["peachy"], ["light peach"])
    def test_case_02(self): self.run_case("bluish", ["bluish"], ["sky blue"])
    def test_case_03(self): self.run_case("minty", ["minty"], ["mint"])
    def test_case_04(self): self.run_case("luxurious", [], [""])
    def test_case_05(self): self.run_case("rosy", ["rosy"], ["rosy pink"])
    def test_case_06(self): self.run_case("edgy", [], [""])
    def test_case_07(self): self.run_case("mochish", ["mochish"], ["mocha brown"])
    def test_case_08(self): self.run_case("shimmery", [], [""])
    def test_case_09(self): self.run_case("foggy", ["foggy"], ["gray white"])
    def test_case_10(self): self.run_case("fairy", ["fairy"], ["fairy pink"])
    def test_case_11(self): self.run_case("creamy", ["creamy"], ["light cream"])
    def test_case_12(self): self.run_case("ashy", ["ashy"], ["cool ash"])
    def test_case_13(self): self.run_case("cloudy", ["cloudy"], ["sky white"])
    def test_case_14(self): self.run_case("inky", ["inky"], ["deep ink"])
    def test_case_15(self): self.run_case("muddy", ["muddy"], ["brown mud"])
    def test_case_16(self): self.run_case("dusty", ["dusty"], ["dust rose"])
    def test_case_17(self): self.run_case("pinky", ["pinky"], ["pink"])
    def test_case_18(self): self.run_case("plummy", ["plummy"], ["plum"])
    def test_case_19(self): self.run_case("grassy", ["grassy"], ["grass green"])
    def test_case_20(self): self.run_case("buttery", ["buttery"], ["butter yellow"])
    def test_case_21(self): self.run_case("sunny", [], ["sunshine"])
    def test_case_22(self): self.run_case("chalky", ["chalky"], ["chalk white"])
    def test_case_23(self): self.run_case("beachy", ["beachy"], ["sand beige"])
    def test_case_24(self): self.run_case("rainy", ["rainy"], ["storm gray"])
    def test_case_25(self): self.run_case("icy", ["icy"], ["ice blue"])
    def test_case_26(self): self.run_case("fiery", ["fiery"], ["fiery red"])
    def test_case_27(self): self.run_case("orangy", ["orangy"], ["orange"])
    def test_case_28(self): self.run_case("limey", ["limey"], ["lime green"])
    def test_case_29(self): self.run_case("glowy", ["glowy"], ["glow pink"])
    def test_case_30(self): self.run_case("frosty", ["frosty"], ["frost white"])
    def test_case_31(self): self.run_case("ambery", ["ambery"], ["amber gold"])
    def test_case_32(self): self.run_case("berry", ["berry"], ["berry red"])
    def test_case_33(self): self.run_case("lavendery", ["lavendery"], ["lavender"])
    def test_case_34(self): self.run_case("cinnamony", ["cinnamony"], ["cinnamon"])
    def test_case_35(self): self.run_case("watery", ["watery"], ["aqua blue"])
    def test_case_36(self): self.run_case("slimy", ["slimy"], ["green slime"])
    def test_case_37(self): self.run_case("bricky", ["bricky"], ["brick red"])
    def test_case_38(self): self.run_case("taupey", ["taupey"], ["taupe"])
    def test_case_39(self): self.run_case("violety", ["violety"], ["violet"])
    def test_case_40(self): self.run_case("chalkish", ["chalkish"], ["chalk white"])
    def test_case_41(self): self.run_case("neutralish", ["neutralish"], ["neutral beige"])
    def test_case_42(self): self.run_case("rosish", ["rosish"], ["rose pink"])
    def test_case_43(self): self.run_case("greenish", ["greenish"], ["forest green"])
    def test_case_44(self): self.run_case("goldish", ["goldish"], ["gold"])
    def test_case_45(self): self.run_case("tanish", ["tanish"], ["tan"])
    def test_case_46(self): self.run_case("whitish", ["whitish"], ["white"])
    def test_case_47(self): self.run_case("reddish", ["reddish"], ["red"])
    def test_case_48(self): self.run_case("bluish", ["bluish"], ["blue"])
    def test_case_49(self): self.run_case("pinkish", ["pinkish"], ["pink"])
    def test_case_50(self): self.run_case("grayish", ["grayish"], ["gray"])


if __name__ == "__main__":
    unittest.main()
