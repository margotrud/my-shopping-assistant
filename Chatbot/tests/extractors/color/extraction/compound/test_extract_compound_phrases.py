# Chatbot/tests/extractors/color/extraction/test_extract_compound_phrases.py

import unittest
import spacy
from Chatbot.extractors.color.extraction.compound import extract_compound_phrases
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()
known_color_tokens = known_modifiers.union(known_tones).union(all_webcolor_names)

class TestExtractCompoundPhrases(unittest.TestCase):

    def run_case(self, text, expected_phrases):

        tokens = nlp(text)
        compounds = set()
        raw_compounds = []

        extract_compound_phrases(
            tokens,
            compounds,
            raw_compounds,
            known_color_tokens,
            known_modifiers,
            known_tones,
            all_webcolor_names,
            raw_text=text,  # 👈 pass user string
            debug=True
        )

        self.assertEqual(expected_phrases, compounds)

    def test_case_01(self): self.run_case("soft pink", {"soft pink"})
    def test_case_02(self): self.run_case("muted rose", {"muted rose"})
    def test_case_03(self): self.run_case("dustyrose", {"dust rose"})
    def test_case_04(self): self.run_case("peachybeige", {"peach beige"})
    def test_case_05(self): self.run_case("nude blush", {"nude blush"})
    def test_case_06(self): self.run_case("deep coral", {"deep coral"})
    def test_case_07(self): self.run_case("intense violet", {"intense violet"})
    def test_case_08(self): self.run_case("glowy bronze", {"glow bronze"})
    def test_case_09(self): self.run_case("palegold", {"pale gold"})
    def test_case_10(self): self.run_case("subtle peach", {"subtle peach"})
    def test_case_11(self): self.run_case("softpink", {"soft pink"})
    def test_case_12(self): self.run_case("bluegreen", set())
    def test_case_13(self): self.run_case("moody purple", set())
    def test_case_14(self): self.run_case("taupeybeige", {"taupe beige"})
    def test_case_15(self): self.run_case("babyblue", {"baby blue"})
    def test_case_16(self): self.run_case("cool tone", set())
    def test_case_17(self): self.run_case("mochish blush", {"mocha blush"})
    def test_case_18(self): self.run_case("elegant blush", set())
    def test_case_19(self): self.run_case("darknight", set())
    def test_case_20(self): self.run_case("glamorousred", set())
    def test_case_21(self): self.run_case("nudepeach", {"nude peach"})
    def test_case_22(self): self.run_case("matte taupe", {"matte taupe"})
    def test_case_23(self): self.run_case("bronzybrown", {"bronze brown"})
    def test_case_24(self): self.run_case("rosybrown", set())
    def test_case_25(self): self.run_case("intensecranberry", {"intense cranberry"})
    def test_case_26(self): self.run_case("dark pink blush", {"pink blush", "dark pink"})
    def test_case_27(self): self.run_case("soft-glow", set())
    def test_case_28(self): self.run_case("offwhite", set())
    def test_case_29(self): self.run_case("faded rose", {"faded rose"})
    def test_case_30(self): self.run_case("rose beige", {"rose beige"})
    def test_case_31(self): self.run_case("brownishpink", {"brownish pink"})
    def test_case_32(self): self.run_case("rosycoral", {"rose coral"})
    def test_case_33(self): self.run_case("goldenyellow", {"golden yellow"})
    def test_case_34(self): self.run_case("darkpeachy", {"dark peach"})
    def test_case_35(self): self.run_case("ultra light beige", {"light beige"})
    def test_case_36(self): self.run_case("silvergrey", {"silver grey"})
    def test_case_37(self): self.run_case("inky blue", {"ink blue"})
    def test_case_38(self): self.run_case("clean peach", {"clean peach"})
    def test_case_39(self): self.run_case("brightred", {"bright red"})
    def test_case_40(self): self.run_case("nude taupe", {"nude taupe"})
    def test_case_41(self): self.run_case("mossygreen", {"moss green"})
    def test_case_42(self): self.run_case("coolmint", {"cool mint"})
    def test_case_43(self): self.run_case("warmapricot", {"warm apricot"})
    def test_case_44(self): self.run_case("milkyrose", {"milky rose"})
    def test_case_45(self): self.run_case("rosebeige", {"rose beige"})
    def test_case_46(self): self.run_case("rustyred", {"rust red"})
    def test_case_47(self): self.run_case("warm beige peach", {"beige peach", "warm beige"})
    def test_case_48(self): self.run_case("bold crimson", {"bold crimson"})
    def test_case_49(self): self.run_case("pinky nude", {"pinky nude"})
    def test_case_50(self): self.run_case("earthy pinky", {"earth pinky"})
