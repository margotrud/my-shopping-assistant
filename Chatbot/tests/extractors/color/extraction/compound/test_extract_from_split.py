# Chatbot/tests/extractors/color/extraction/test_extract_from_split.py

import unittest
import spacy
from Chatbot.extractors.color.extraction.compound import extract_from_split
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()
known_color_tokens = known_tones.union(known_modifiers).union(all_webcolor_names)

class TestExtractFromSplit(unittest.TestCase):

    def run_case(self, text, expected_compounds):
        tokens = nlp(text)
        compounds = set()
        raw = []
        print("[TEST] Checking known_color_tokens:")
        print("  'soft' in known_color_tokens? ", 'soft' in known_color_tokens)
        print("  'pink' in known_color_tokens? ", 'pink' in known_color_tokens)
        print("  split_glued_tokens('softpink') →", split_glued_tokens("softpink", known_color_tokens))

        extract_from_split(
            tokens=tokens,
            compounds=compounds,
            raw_compounds=raw,
            known_color_tokens=known_color_tokens,
            known_modifiers=known_modifiers,
            known_tones=known_tones,
            all_webcolor_names=all_webcolor_names,
            debug=False,
        )
        self.assertEqual(expected_compounds, compounds)

    def test_case_01(self): self.run_case("glow blue", set())
    def test_case_02(self): self.run_case("softpink peach", {"soft peach", "soft pink"})
    def test_case_03(self): self.run_case("deepbrown red", {"deep red", "deep brown"})
    def test_case_04(self): self.run_case("peachy pink", {"peachy pink"})
    def test_case_05(self): self.run_case("lightred dusty", {"light red"})
    def test_case_06(self): self.run_case("icygreen skyblue", {"icy blue", "icy green"})
    def test_case_07(self): self.run_case("mintyrose", set())
    def test_case_08(self): self.run_case("sunnypink", set())
    def test_case_09(self): self.run_case("coolgray blue", {"cool blue"})
    def test_case_10(self): self.run_case("warmtaupe beige", {"warm taupe", "warm beige"})

    def test_case_11(self): self.run_case("rosybrown", set())
    def test_case_12(self): self.run_case("glowybronze", set())
    def test_case_13(self): self.run_case("barelyred", set())
    def test_case_14(self): self.run_case("mutedpeach", set())
    def test_case_15(self): self.run_case("dustyrose", set())
    def test_case_16(self): self.run_case("coldbeige", set())
    def test_case_17(self): self.run_case("creamyivory", set())
    def test_case_18(self): self.run_case("chalkypink", set())
    def test_case_19(self): self.run_case("coolblue", set())
    def test_case_20(self): self.run_case("inkybrown", set())

    def test_case_21(self): self.run_case("mattegreen", set())
    def test_case_22(self): self.run_case("freshorange", set())
    def test_case_23(self): self.run_case("mochabrown", set())
    def test_case_24(self): self.run_case("glamgold", set())
    def test_case_25(self): self.run_case("shinycopper", set())
    def test_case_26(self): self.run_case("taupeybeige", {"taupe beige"})
    def test_case_27(self): self.run_case("edgyred", set())
    def test_case_28(self): self.run_case("rosishpink", set())
    def test_case_29(self): self.run_case("chalkishwhite", set())
    def test_case_30(self): self.run_case("cloudygray", set())

    def test_case_31(self): self.run_case("muddybrown", set())
    def test_case_32(self): self.run_case("butterybeige", set())
    def test_case_33(self): self.run_case("greenyellow", set())
    def test_case_34(self): self.run_case("frostywhite", set())
    def test_case_35(self): self.run_case("lavenderypurple", set())
    def test_case_36(self): self.run_case("rainygray", set())
    def test_case_37(self): self.run_case("orangyred", set())
    def test_case_38(self): self.run_case("limeygreen", set())
    def test_case_39(self): self.run_case("chalkblue", set())
    def test_case_40(self): self.run_case("powderpink", set())

    def test_case_41(self): self.run_case("earthybrown", set())
    def test_case_42(self): self.run_case("mistygreen", set())
    def test_case_43(self): self.run_case("beachysand", set())
    def test_case_44(self): self.run_case("neutralgray", set())
    def test_case_45(self): self.run_case("amberyred", set())
    def test_case_46(self): self.run_case("brightblue", set())
    def test_case_47(self): self.run_case("satinblack", set())
    def test_case_48(self): self.run_case("shimmerypink", set())
    def test_case_49(self): self.run_case("milkywhite", set())
    def test_case_50(self): self.run_case("coolmint", set())

if __name__ == "__main__":
    unittest.main()
