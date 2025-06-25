# Chatbot/tests/extractors/color/extraction/test_extract_from_split.py

import unittest
import spacy
from Chatbot.extractors.color.extraction.compound import extract_from_split
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()
known_color_tokens = known_tones.union(known_modifiers).union(all_webcolor_names)


class TestExtractFromSplit(unittest.TestCase):

    def run_case(self, text, expected_compounds):
        tokens = nlp(text)
        compounds = set()
        raw_compounds = []
        extract_from_split(
            tokens=tokens,
            compounds=compounds,
            raw_compounds=raw_compounds,
            known_color_tokens=known_color_tokens,
            known_modifiers=known_modifiers,
            known_tones=known_tones,
            all_webcolor_names=all_webcolor_names,
            debug=True
        )
        self.assertEqual(expected_compounds, compounds)

    def test_case_01(self): self.run_case("dustyrose", {"dust rose"})
    def test_case_02(self): self.run_case("taupeybeige", {"taupe beige"})
    def test_case_03(self): self.run_case("ashyrose", {"ashy rose"})
    def test_case_04(self): self.run_case("frostynude", set())
    def test_case_05(self): self.run_case("bluegreen", set())
    def test_case_06(self): self.run_case("warmtaupe", {"warm taupe"})
    def test_case_07(self): self.run_case("smokynude", {"smoke nude"})
    def test_case_08(self): self.run_case("charcoalrose", {"charcoal rose"})
    def test_case_09(self): self.run_case("beigegray", {"beige gray"})
    def test_case_10(self): self.run_case("graybeige", {"gray beige"})
    def test_case_11(self): self.run_case("mutedrose", {"muted rose"})
    def test_case_12(self): self.run_case("deepcoral", {"deep coral"})
    def test_case_13(self): self.run_case("nudepeach", {"nude peach"})
    def test_case_14(self): self.run_case("goldenbronze", {"golden bronze"})
    def test_case_15(self): self.run_case("lightgray", set())
    def test_case_16(self): self.run_case("earthynude", {"earth nude"})
    def test_case_17(self): self.run_case("softbrown", {"soft brown"})
    def test_case_18(self): self.run_case("dustyroseglow", set())  # should skip invalid 3-part glue
    def test_case_19(self): self.run_case("icycoral", {"icy coral"})
    def test_case_20(self): self.run_case("coolbeige", {"cool beige"})
    def test_case_21(self): self.run_case("dimgray", set())
    def test_case_22(self): self.run_case("warmgrey", {"warm grey"})
    def test_case_23(self): self.run_case("nudepink", {"nude pink"})
    def test_case_24(self): self.run_case("muddyyellow", set())
    def test_case_25(self): self.run_case("sunsetcoral", set())
    def test_case_26(self): self.run_case("chalkypink", {"chalk pink"})
    def test_case_27(self): self.run_case("glowyrose", {"glow rose"})  # not valid split
    def test_case_28(self): self.run_case("peachygray", {"peach gray"})  # peachy = modifier; gray known but no mapping
    def test_case_29(self): self.run_case("offwhitebeige", set())  # no valid split
    def test_case_30(self): self.run_case("mintylavender", {"mint lavender"})  # not recognized as valid parts
    def test_case_31(self): self.run_case("rosynude", {"rose nude"})  # suppressed by invalid base/tone relationship
    def test_case_32(self): self.run_case("cooltonedrose", set())  # rejected 3-part or invalid
    def test_case_33(self): self.run_case("edgyblue", set())  # "edgy" is a style expression, not a color mod
    def test_case_34(self): self.run_case("greenpink", {"green pink"})  # conflicting tones
    def test_case_35(self): self.run_case("shinyblush", {"shiny blush"})  # shiny = blocked expression tone
    def test_case_36(self): self.run_case("rosybrown", set())
    def test_case_37(self): self.run_case("mistyrose", set())
    def test_case_38(self): self.run_case("antiquewhite", set())
    def test_case_39(self): self.run_case("salmonpink", {"salmon pink"})
    def test_case_40(self): self.run_case("pinkybeige", {"pinky beige"})
    def test_case_41(self): self.run_case("duskyplum", {"dust plum"})
    def test_case_42(self): self.run_case("mochabrown", {"mocha brown"})
    def test_case_43(self): self.run_case("faintapricot", {"faint apricot"})
    def test_case_44(self): self.run_case("dimbeige", set())
    def test_case_45(self): self.run_case("barelyblush", set())
    def test_case_46(self): self.run_case("chalkynude", {"chalk nude"})
    def test_case_47(self): self.run_case("graypink", {"gray pink"})  # conflicting tones
    def test_case_48(self): self.run_case("tanbrown", {"tan brown"})
    def test_case_49(self): self.run_case("boldcoral", {"bold coral"})
    def test_case_50(self): self.run_case("neutralrose", {"neutral rose"})


if __name__ == "__main__":
    unittest.main()
