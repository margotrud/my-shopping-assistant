import unittest
import spacy

from Chatbot.extractors.color.extraction.standalone import _inject_expression_modifiers
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.shared.constants import COSMETIC_NOUNS
from Chatbot.extractors.color.utils.token_utils import normalize_token

nlp = spacy.load("en_core_web_sm")
known_modifiers = load_known_modifiers()

class TestInjectExpressionModifiers(unittest.TestCase):
    def run_case(self, text, expected):
        tokens = nlp(text)
        result = _inject_expression_modifiers(tokens, known_modifiers, debug=True)
        self.assertEqual(set(expected), set(result), f"\nExpected: {expected}\nActual:   {result}")

    def test_case_01(self): self.run_case("soft", ["soft"])
    def test_case_02(self): self.run_case("bold", ["bold"])
    def test_case_03(self): self.run_case("light makeup", ["light"])
    def test_case_04(self): self.run_case("lipstick", [])  # Blocked noun
    def test_case_05(self): self.run_case("muted", ["muted"])
    def test_case_06(self): self.run_case("vibrant shade", ["vibrant"])
    def test_case_07(self): self.run_case("foundation", [])  # Blocked noun
    def test_case_08(self): self.run_case("deep bronze", ["bronze", "deep"])
    def test_case_09(self): self.run_case("strong tone", ["strong"])
    def test_case_10(self): self.run_case("highlighter", [])  # Blocked noun
    def test_case_11(self): self.run_case("subtle glow", ["subtle", "glow"])
    def test_case_12(self): self.run_case("nude", ["nude"])
    def test_case_13(self): self.run_case("warm base", ["warm"])
    def test_case_14(self): self.run_case("mascara", [])  # Blocked noun
    def test_case_15(self): self.run_case("icy hue", ["icy"])
    def test_case_16(self): self.run_case("natural", ["natural"])
    def test_case_17(self): self.run_case("rosy", ["rose"])
    def test_case_18(self): self.run_case("blush", [])  # Blocked noun
    def test_case_19(self): self.run_case("neutral skin", ["neutral"])
    def test_case_20(self): self.run_case("dramatic effect", set())
    def test_case_21(self): self.run_case("clean style", ["clean"])
    def test_case_22(self): self.run_case("cool toned", ["cool"])
    def test_case_23(self): self.run_case("minimal look", set())
    def test_case_24(self): self.run_case("classic red", ["classic"])
    def test_case_25(self): self.run_case("gentle finish", set())
    def test_case_26(self): self.run_case("barely there glow", ["glow"])
    def test_case_27(self): self.run_case("refined aesthetic", set())
    def test_case_28(self): self.run_case("bronzer", [])  # Blocked noun
    def test_case_29(self): self.run_case("peachy blush", ["peach"])
    def test_case_30(self): self.run_case("elegant vibe", set())
    def test_case_31(self): self.run_case("cool-neutral skin", ["neutral", "cool"])
    def test_case_32(self): self.run_case("ultra light tone", ["light"])
    def test_case_33(self): self.run_case("rosy lipstick", ["rose"])
    def test_case_34(self): self.run_case("earthy pink", ["earth"])
    def test_case_35(self): self.run_case("romantic shade", set())
    def test_case_36(self): self.run_case("gentle glow", ["glow"])
    def test_case_37(self): self.run_case("bare skin", ["bare"])
    def test_case_38(self): self.run_case("fresh vibe", ["fresh"])
    def test_case_39(self): self.run_case("shiny gloss", ["shiny"])
    def test_case_40(self): self.run_case("invisible makeup", set())
    def test_case_41(self): self.run_case("ashy effect", ["ashy"])
    def test_case_42(self): self.run_case("no-makeup style", set())
    def test_case_43(self): self.run_case("neutral-warm base", ["neutral","warm"])
    def test_case_44(self): self.run_case("pinky tone", ["pinky"])
    def test_case_45(self): self.run_case("daytime look", set())
    def test_case_46(self): self.run_case("polished finish", set())
    def test_case_47(self): self.run_case("minimalist glow", ["glow"])  # Not in modifiers
    def test_case_48(self): self.run_case("romantic blush", set())
    def test_case_49(self): self.run_case("cool lipstick", ["cool"])
    def test_case_50(self): self.run_case("timeless and classic", ["classic"])

if __name__ == "__main__":
    unittest.main()
