import unittest
import spacy

from Chatbot.extractors.color.extraction.standalone import _inject_expression_modifiers
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

known_modifiers = load_known_modifiers()

nlp = spacy.load("en_core_web_sm")

class TestInjectExpressionModifiers(unittest.TestCase):

    def setUp(self):
        self.known_modifiers = known_modifiers

    def run_case(self, text, expected, debug=False):
        tokens = list(nlp(text))
        result = _inject_expression_modifiers(tokens, self.known_modifiers, debug)
        print(f"Expected: {set(expected)}")
        print(f"Actual  : {result}")
        self.assertEqual(set(expected), result)

    def test_case_01(self): self.run_case("soft", ["soft"])
    def test_case_02(self): self.run_case("muted", ["muted"])
    def test_case_03(self): self.run_case("rosy", ["rose"])
    def test_case_04(self): self.run_case("peachy", ["peach"])
    def test_case_05(self): self.run_case("romantic", ["soft", "rosy"])
    def test_case_06(self): self.run_case("elegant", ["classic", "rosy", "soft"])
    def test_case_07(self): self.run_case("natural", ["natural", "muted", "bare", "neutral", "soft", "rosy"])
    def test_case_08(self): self.run_case("evening", ["bold", "rosy", "soft"])
    def test_case_09(self): self.run_case("soft glam", ["soft", "rosy"])
    def test_case_10(self): self.run_case("daytime", ["light", "muted", "natural", "rosy", "soft", "warm"])
    def test_case_11(self): self.run_case("earthy", ["muted", "dusty", "rosy", "warm"])
    def test_case_12(self): self.run_case("fresh", ["bare", "light", "rosy", "soft"])
    def test_case_13(self): self.run_case("edgy", ["bold", "dark", "vibrant"])
    def test_case_14(self): self.run_case("classic", ["classic"])
    def test_case_15(self): self.run_case("barely-there", ["barely-there"])
    def test_case_16(self): self.run_case("dewy", ["dewy"])
    def test_case_17(self): self.run_case("powdery", ["powdery"])
    def test_case_18(self): self.run_case("glowy", ["glowy"])
    def test_case_19(self): self.run_case("shiny", ["shiny"])
    def test_case_20(self): self.run_case("soft pink", ["soft"])
    def test_case_21(self): self.run_case("deep tone", ["deep"])
    def test_case_22(self): self.run_case("medium-light beige", ["medium-light"])
    def test_case_23(self): self.run_case("icy blush", ["icy"])
    def test_case_24(self): self.run_case("cool and warm", ["cool", "warm"])
    def test_case_25(self): self.run_case("clean natural makeup", ["clean", "natural", "soft", "rosy", "bare", "muted", "neutral"])
    def test_case_26(self): self.run_case("minimal look", ["minimalist", "bare"])
    def test_case_27(self): self.run_case("feminine", ["soft", "rosy"])
    def test_case_28(self): self.run_case("flirty tones", ["soft", "rosy"])
    def test_case_29(self): self.run_case("refined finish", ["soft", "rosy"])
    def test_case_30(self): self.run_case("subtle sparkle", ["subtle", "soft"])
    def test_case_31(self): self.run_case("very fair", ["very fair"])
    def test_case_32(self): self.run_case("tan shade", ["tan"])
    def test_case_33(self): self.run_case("bold red", ["bold"])
    def test_case_34(self): self.run_case("neon pink", ["neon"])
    def test_case_35(self): self.run_case("dramatic night look", ["dramatic", "bold", "rosy", "soft"])
    def test_case_36(self): self.run_case("party-ready", ["bold", "rosy", "soft"])
    def test_case_37(self): self.run_case("moody tones", ["bold", "muted", "dark"])
    def test_case_38(self): self.run_case("summer tone", ["bare", "light", "rosy", "soft"])
    def test_case_39(self): self.run_case("hydrated skin", ["dewy", "glowy"])
    def test_case_40(self): self.run_case("very dark glam", ["very dark", "glam"])
    def test_case_41(self): self.run_case("satin finish", ["satin"])
    def test_case_42(self): self.run_case("creamy lipstick", ["creamy"])
    def test_case_43(self): self.run_case("matte foundation", ["matte"])
    def test_case_44(self): self.run_case("bronzed tone", ["bronzed"])
    def test_case_45(self): self.run_case("skin-like result", ["bare", "natural"])
    def test_case_46(self): self.run_case("enhanced but subtle", ["subtle", "soft", "rosy"])
    def test_case_47(self): self.run_case("wedding makeup", ["soft", "rosy"])
    def test_case_48(self): self.run_case("red carpet", ["bold", "rosy", "soft"])
    def test_case_49(self): self.run_case("timeless style", ["classic", "rosy", "soft"])
    def test_case_50(self): self.run_case("polished finish", ["rosy", "soft"])

if __name__ == "__main__":
    unittest.main()
