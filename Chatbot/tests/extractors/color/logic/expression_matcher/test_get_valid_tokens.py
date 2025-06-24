# tests/test_get_valid_tokens.py

import unittest
import spacy
from Chatbot.extractors.color.logic.expression_matcher import get_valid_tokens
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir

nlp = spacy.load("en_core_web_sm")
expression_map = load_json_from_data_dir("expression_definition.json")

class TestGetValidTokens(unittest.TestCase):

    def run_case(self, text, expected_tokens):
        result = get_valid_tokens(text, expression_map)
        self.assertEqual(expected_tokens, result, f"Expected: {expected_tokens}\nActual: {result}")

    def test_case_01(self): self.run_case("romantic and soft glam", ["romantic", "soft glam"])
    def test_case_02(self): self.run_case("natural elegant look", ["elegant", "natural"])
    def test_case_03(self): self.run_case("subtle but edgy style", ["edgy", "subtle"])
    def test_case_04(self): self.run_case("soft glam with shimmer", ["soft glam"])
    def test_case_05(self): self.run_case("something bold and bright", ["bold", "bright"])
    def test_case_06(self): self.run_case("neutral and casual daytime look", ["casual", "daytime", "neutral"])
    def test_case_07(self): self.run_case("I want something clean", ["clean"])
    def test_case_08(self): self.run_case("classic vibe for the evening", ["classic", "evening"])
    def test_case_09(self): self.run_case("give me modern and fresh", ["fresh"])
    def test_case_10(self): self.run_case("timeless elegance", ["timeless"])
    def test_case_11(self): self.run_case("non-matching words", [])
    def test_case_12(self): self.run_case("abstract words without mapping", [])
    def test_case_13(self): self.run_case("just the word blush", [])
    def test_case_14(self): self.run_case("romantically soft gestures", ["romantic", "soft"])
    def test_case_15(self): self.run_case("I feel glam but not too bold", ["bold", "glam"])
    def test_case_16(self): self.run_case("a very gentle look", ["gentle"])
    def test_case_17(self): self.run_case("soft and neutral tones", ["neutral", "soft"])
    def test_case_18(self): self.run_case("something dramatic but romantic", ["dramatic", "romantic"])
    def test_case_19(self): self.run_case("modern and bold appeal", ["bold"])
    def test_case_20(self): self.run_case("edgy but still subtle", ["edgy", "subtle"])
    def test_case_21(self): self.run_case("elegant clean style", ["clean", "elegant"])
    def test_case_22(self): self.run_case("natural or glam look", ["glam", "natural"])
    def test_case_23(self): self.run_case("casual yet timeless", ["casual", "timeless"])
    def test_case_24(self): self.run_case("daytime or evening", ["daytime", "evening"])
    def test_case_25(self): self.run_case("subtle shimmer glow", ["subtle"])
    def test_case_26(self): self.run_case("vintage romantic vibes", ["romantic"])
    def test_case_27(self): self.run_case("understated clean makeup", ["clean"])
    def test_case_28(self): self.run_case("give me bold and confident", ["bold"])
    def test_case_29(self): self.run_case("something fresh and light", ["fresh", "light"])
    def test_case_30(self): self.run_case("playful and edgy combo", ["edgy", "playful"])
    def test_case_31(self): self.run_case("something classic and strong", ["classic"])
    def test_case_32(self): self.run_case("dramatic strong choice", ["dramatic"])
    def test_case_33(self): self.run_case("soft elegant impression", ["elegant", "soft"])
    def test_case_34(self): self.run_case("natural soft glow", ["natural", "soft"])
    def test_case_35(self): self.run_case("simple neutral tones", ["neutral"])
    def test_case_36(self): self.run_case("moody and bold mix", ["bold"])
    def test_case_37(self): self.run_case("warm and romantic design", ["romantic", "warm"])
    def test_case_38(self): self.run_case("romantic and glowing", ["romantic"])
    def test_case_39(self): self.run_case("glamorous evening choice", ["evening", "glamorous"])
    def test_case_40(self): self.run_case("bright and bold finish", ["bold", "bright"])
    def test_case_41(self): self.run_case("classic glam combo", ["classic", "glam"])
    def test_case_42(self): self.run_case("elegant shimmer", ["elegant"])
    def test_case_43(self): self.run_case("natural finish", ["natural"])
    def test_case_44(self): self.run_case("timeless neutral", ["neutral", "timeless"])
    def test_case_45(self): self.run_case("neutral modern style", ["neutral"])
    def test_case_46(self): self.run_case("glam and shine", ["glam"])
    def test_case_47(self): self.run_case("soft yet bold", ["bold", "soft"])
    def test_case_48(self): self.run_case("give me romantic", ["romantic"])
    def test_case_49(self): self.run_case("something edgy", ["edgy"])
    def test_case_50(self): self.run_case("not romantic, just classic", ["classic", "romantic"])


if __name__ == "__main__":
    unittest.main()
