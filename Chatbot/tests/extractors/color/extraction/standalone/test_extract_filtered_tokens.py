import unittest
import spacy

from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.extraction.standalone import _extract_filtered_tokens
known_modifiers = load_known_modifiers()
nlp = spacy.load("en_core_web_sm")

class TestExtractFilteredTokens(unittest.TestCase):

    def run_case(self, text, expected):
        tokens = nlp(text)
        result = _extract_filtered_tokens(tokens, known_modifiers, known_tones, debug=True)
        self.assertEqual(set(expected), set(result), f"\nExpected: {expected}\nActual:   {result}")

    def test_case_01(self): self.run_case("soft", ["soft"])
    def test_case_02(self): self.run_case("blush", [])  # cosmetic noun
    def test_case_03(self): self.run_case("dusty", ["dust"])
    def test_case_04(self): self.run_case("muted", ["muted"])
    def test_case_05(self): self.run_case("classic", ["classic"])
    def test_case_06(self): self.run_case("glowy", ["glow"])
    def test_case_07(self): self.run_case("inky", ["ink"])
    def test_case_08(self): self.run_case("elegant", set())
    def test_case_09(self): self.run_case("bare", ["bare"])
    def test_case_10(self): self.run_case("bold", ["bold"])

    def test_case_11(self): self.run_case("natural", ["natural"])
    def test_case_12(self): self.run_case("warm", ["warm"])
    def test_case_13(self): self.run_case("rosy", ["rose"])
    def test_case_14(self): self.run_case("shiny", ["shiny"])
    def test_case_15(self): self.run_case("vibrant", ["vibrant"])
    def test_case_16(self): self.run_case("icy", ["icy"])
    def test_case_17(self): self.run_case("toned", [])  # not standalone
    def test_case_18(self): self.run_case("shade", [])  # cosmetic noun
    def test_case_19(self): self.run_case("neutral", ["neutral"])
    def test_case_20(self): self.run_case("gentle", set())

    def test_case_21(self): self.run_case("moody", set())
    def test_case_22(self): self.run_case("taupey", [])
    def test_case_23(self): self.run_case("minimal", set())
    def test_case_24(self): self.run_case("grimy", set())
    def test_case_25(self): self.run_case("effortless", set())
    def test_case_26(self): self.run_case("invisible", set())
    def test_case_27(self): self.run_case("chalk", ["chalk"])
    def test_case_28(self): self.run_case("barely", ["bare"])  # too generic
    def test_case_29(self): self.run_case("refined", set())
    def test_case_30(self): self.run_case("medium-light", ["medium", "light"])

    def test_case_31(self): self.run_case("peachy", ["peach"])
    def test_case_32(self): self.run_case("deep", ["deep"])
    def test_case_33(self): self.run_case("light", ["light"])
    def test_case_34(self): self.run_case("dim", set())
    def test_case_35(self): self.run_case("barely-there", ["bare"])
    def test_case_36(self): self.run_case("subtle", ["subtle"])
    def test_case_37(self): self.run_case("chalky", ["chalk"])
    def test_case_38(self): self.run_case("darkish", ["dark"])
    def test_case_39(self): self.run_case("cool-neutral", ["neutral", "cool"])
    def test_case_40(self): self.run_case("strong", ["strong"])

    def test_case_41(self): self.run_case("ultra deep", ["deep"])
    def test_case_42(self): self.run_case("warm-toned", ["warm"])
    def test_case_43(self): self.run_case("neon", ["neon"])
    def test_case_44(self): self.run_case("ashy", ["ashy"])
    def test_case_45(self): self.run_case("mochish", [])  # invalid root
    def test_case_46(self): self.run_case("tone", [])     # cosmetic noun
    def test_case_47(self): self.run_case("pink", ["pink"])
    def test_case_48(self): self.run_case("rose blush", ["rose"])  # blush blocked
    def test_case_49(self): self.run_case("dark nude", ["dark", "nude"])
    def test_case_50(self): self.run_case("soft pink and peachy tones", ["soft", "pink", "peach"])

