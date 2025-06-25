# Chatbot/tests/extractors/color/extraction/test_extract_from_glued.py

import unittest
import spacy

from Chatbot.extractors.color.extraction.compound import extract_from_glued
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()
known_color_tokens = known_tones.union(known_modifiers).union(all_webcolor_names)

class TestExtractFromGlued(unittest.TestCase):

    def run_case(self, text, expected, debug=False):

        tokens = nlp(text)
        compounds = set()
        raw = []
        extract_from_glued(
            tokens=tokens,
            compounds=compounds,
            raw_compounds=raw,
            known_color_tokens=known_color_tokens,
            known_modifiers=known_modifiers,
            known_tones=known_tones,
            all_webcolor_names=all_webcolor_names,
            debug=debug,
        )
        print("[🧪 INPUT TEXT]", text)
        print("[🧪 TOKENS]", [t.text for t in nlp(text)])

        self.assertEqual(expected, compounds, f"\nExpected: {expected}\nActual:   {compounds}")

    def test_case_01(self): self.run_case("dustyrose", {"dust rose"})
    def test_case_02(self): self.run_case("mutedpeach", {"muted peach"})
    def test_case_03(self): self.run_case("coollavender", {"cool lavender"})
    def test_case_04(self): self.run_case("deepnude", {"deep nude"})
    def test_case_05(self): self.run_case("softpinkish", {"soft pinkish"})
    def test_case_06(self): self.run_case("rose", set())
    def test_case_07(self): self.run_case("pinkybeige", {"pinky beige"})
    def test_case_08(self): self.run_case("moodytaupe", set())
    def test_case_09(self): self.run_case("bluegreen", set())
    def test_case_10(self): self.run_case("vibrantorange", {"vibrant orange"})
    def test_case_11(self): self.run_case("rosygold", {"rose gold"})
    def test_case_12(self): self.run_case("barelybeige", {"bare beige"})
    def test_case_13(self): self.run_case("nudenavy", {"nude navy"})
    def test_case_14(self): self.run_case("dustyrosepink", set())
    def test_case_15(self): self.run_case("creamyivory", {"cream ivory"})
    def test_case_16(self): self.run_case("glowypink", {"glow pink"})
    def test_case_17(self): self.run_case("lightmint", {"light mint"})
    def test_case_18(self): self.run_case("bronzebeige", {"bronze beige"})
    def test_case_19(self): self.run_case("freshpeach", {"fresh peach"})
    def test_case_20(self): self.run_case("icyblue", {"icy blue"})
    def test_case_21(self): self.run_case("warmtaupe", {"warm taupe"})
    def test_case_22(self): self.run_case("greylavender", {"grey lavender"})
    def test_case_23(self): self.run_case("nudemaroon", {"nude maroon"})
    def test_case_24(self): self.run_case("intenseplum", {"intense plum"})
    def test_case_25(self): self.run_case("boldcoral", {"bold coral"})
    def test_case_26(self): self.run_case("softnude", {"soft nude"})
    def test_case_27(self): self.run_case("subtlealmond", {"subtle almond"})
    def test_case_28(self): self.run_case("milkybeige", {"milky beige"})
    def test_case_29(self): self.run_case("richburgundy", {"rich burgundy"})
    def test_case_30(self): self.run_case("purepearl", {"pure pearl"})
    def test_case_31(self): self.run_case("mistymauve", {"mist mauve"})
    def test_case_32(self): self.run_case("blushtaupe", {"blush taupe"})
    def test_case_33(self): self.run_case("mochachampagne", {"mocha champagne"})
    def test_case_34(self): self.run_case("softtaupeyrose", set())
    def test_case_35(self): self.run_case("sugaryalmond", set())
    def test_case_36(self): self.run_case("peachyblush", {"peach blush"})
    def test_case_37(self): self.run_case("nudeivory", {"nude ivory"})
    def test_case_38(self): self.run_case("pistachiomint", {"pistachio mint"})
    def test_case_39(self): self.run_case("boldochre", {"bold ochre"})
    def test_case_40(self): self.run_case("lilacyrose", {"lilac rose"})
    def test_case_41(self): self.run_case("beigeygold", {"beigey gold"})
    def test_case_42(self): self.run_case("navyplum", {"navy plum"})
    def test_case_43(self): self.run_case("smokygraphite", set())
    def test_case_44(self): self.run_case("earthyterracotta", {"earth terracotta"})
    def test_case_45(self): self.run_case("skyblush", {"sky blush"})
    def test_case_46(self): self.run_case("berrymocha", {"berry mocha"})
    def test_case_47(self): self.run_case("hazelbronze", {"hazel bronze"})
    def test_case_48(self): self.run_case("oatmilklatte", set())
    def test_case_49(self): self.run_case("nuttyrose", set())
    def test_case_50(self): self.run_case("plumpine", {"plum pine"})
