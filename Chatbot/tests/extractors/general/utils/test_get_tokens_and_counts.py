import unittest
from collections import Counter
import spacy
from typing import List
from spacy.tokens import Token

from Chatbot.extractors.general.utils.tokenizer import get_tokens_and_counts  # Update path as needed

_nlp = spacy.load("en_core_web_sm")

class TestGetTokensAndCounts(unittest.TestCase):
    def run_test(self, text: str, expected_tokens: List[str], expected_counts: Counter):
        tokens, counts = get_tokens_and_counts(text)
        result_tokens = [t.text for t in tokens]
        self.assertEqual(result_tokens, expected_tokens, f"\nExpected Tokens: {expected_tokens}\nGot: {result_tokens}")
        self.assertEqual(counts, expected_counts, f"\nExpected Counts: {expected_counts}\nGot: {counts}")

    def test_case_01(self): self.run_test("soft pink", ["soft", "pink"], Counter({"soft": 1, "pink": 1}))
    def test_case_02(self): self.run_test("soft pink soft", ["soft", "pink", "soft"], Counter({"soft": 2, "pink": 1}))
    def test_case_03(self): self.run_test("Soft PINK", ["soft", "pink"], Counter({"soft": 1, "pink": 1}))
    def test_case_04(self): self.run_test("Soft, pink.", ["soft", ",", "pink", "."], Counter({"soft": 1, ",": 1, "pink": 1, ".": 1}))
    def test_case_05(self): self.run_test("Soft, soft, soft", ["soft", ",", "soft", ",", "soft"], Counter({"soft": 3, ",": 2}))
    def test_case_06(self): self.run_test("barely-there glow", ["barely", "-", "there", "glow"], Counter({"barely": 1, "-": 1, "there": 1, "glow": 1}))
    def test_case_07(self): self.run_test("    clean   glow   ", ['    ', 'clean', '  ', 'glow', '  '], Counter({'  ': 2, '    ': 1, 'clean': 1, 'glow': 1}))
    def test_case_08(self): self.run_test("123 soft", ["123", "soft"], Counter({"123": 1, "soft": 1}))
    def test_case_09(self): self.run_test("soft soft soft soft", ["soft", "soft", "soft", "soft"], Counter({"soft": 4}))
    def test_case_10(self): self.run_test("!! soft !!", ["!", "!", "soft", "!", "!"], Counter({"!": 4, "soft": 1}))
    def test_case_11(self): self.run_test("glam & glow", ["glam", "&", "glow"], Counter({"glam": 1, "&": 1, "glow": 1}))
    def test_case_12(self): self.run_test("soft-glow", ["soft", "-", "glow"], Counter({"soft": 1, "-": 1, "glow": 1}))
    def test_case_13(self): self.run_test("soft-glow-soft", ["soft", "-", "glow", "-", "soft"], Counter({"soft": 2, "-": 2, "glow": 1}))
    def test_case_14(self): self.run_test("soft soft, pink.", ["soft", "soft", ",", "pink", "."], Counter({"soft": 2, ",": 1, "pink": 1, ".": 1}))
    def test_case_15(self): self.run_test("subtle, soft, pink", ["subtle", ",", "soft", ",", "pink"], Counter({"subtle": 1, ",": 2, "soft": 1, "pink": 1}))
    def test_case_16(self): self.run_test("barely-there barely-there", ["barely", "-", "there", "barely", "-", "there"], Counter({"barely": 2, "-": 2, "there": 2}))
    def test_case_17(self): self.run_test("soft soft SOFT", ["soft", "soft", "soft"], Counter({"soft": 3}))
    def test_case_18(self): self.run_test("refined, luminous makeup", ["refined", ",", "luminous", "makeup"], Counter({"refined": 1, ",": 1, "luminous": 1, "makeup": 1}))
    def test_case_19(self): self.run_test("refined luminous refined luminous", ["refined", "luminous", "refined", "luminous"], Counter({"refined": 2, "luminous": 2}))
    def test_case_20(self): self.run_test("dewy, glowy, radiant", ["dewy", ",", "glowy", ",", "radiant"], Counter({"dewy": 1, ",": 2, "glowy": 1, "radiant": 1}))

    def test_case_21(self): self.run_test("GLAM glamorous glamor", ["glam", "glamorous", "glamor"], Counter({"glam": 1, "glamorous": 1, "glamor": 1}))
    def test_case_22(self): self.run_test("bare pink bare pink bare", ["bare", "pink", "bare", "pink", "bare"], Counter({"bare": 3, "pink": 2}))
    def test_case_23(self): self.run_test("elegant elegant!", ["elegant", "elegant", "!"], Counter({"elegant": 2, "!": 1}))
    def test_case_24(self): self.run_test("glow-up", ["glow", "-", "up"], Counter({"glow": 1, "-": 1, "up": 1}))
    def test_case_25(self): self.run_test("shine shine shine", ["shine", "shine", "shine"], Counter({"shine": 3}))
    def test_case_26(self): self.run_test("bold glam elegant bold", ["bold", "glam", "elegant", "bold"], Counter({"bold": 2, "glam": 1, "elegant": 1}))
    def test_case_27(self): self.run_test("matte finish glow", ["matte", "finish", "glow"], Counter({"matte": 1, "finish": 1, "glow": 1}))
    def test_case_28(self): self.run_test("peachy glow", ["peachy", "glow"], Counter({"peachy": 1, "glow": 1}))
    def test_case_29(self): self.run_test("I like pink", ["i", "like", "pink"], Counter({"i": 1, "like": 1, "pink": 1}))
    def test_case_30(self): self.run_test("I don't want red", ["i", "do", "n't", "want", "red"], Counter({"i": 1, "do": 1, "n't": 1, "want": 1, "red": 1}))
    def test_case_31(self): self.run_test("soft glam and glow", ["soft", "glam", "and", "glow"], Counter({"soft": 1, "glam": 1, "and": 1, "glow": 1}))
    def test_case_32(self): self.run_test("light, airy, peachy", ["light", ",", "airy", ",", "peachy"], Counter({"light": 1, ",": 2, "airy": 1, "peachy": 1}))
    def test_case_33(self): self.run_test("neutral tones for daily wear", ["neutral", "tones", "for", "daily", "wear"], Counter({"neutral": 1, "tones": 1, "for": 1, "daily": 1, "wear": 1}))
    def test_case_34(self): self.run_test("NO red please", ["no", "red", "please"], Counter({"no": 1, "red": 1, "please": 1}))
    def test_case_35(self): self.run_test("dramatic... not for me", ['dramatic', '...', 'not', 'for', 'me'], Counter({'dramatic': 1, '...': 1, 'not': 1, 'for': 1, 'me': 1}))
    def test_case_36(self): self.run_test("Red?! No thanks", ["red", "?", "!", "no", "thanks"], Counter({"red": 1, "?": 1, "!": 1, "no": 1, "thanks": 1}))
    def test_case_37(self): self.run_test("bright pinkish coral", ["bright", "pinkish", "coral"], Counter({"bright": 1, "pinkish": 1, "coral": 1}))
    def test_case_38(self): self.run_test("nude tones or dusty rose", ["nude", "tones", "or", "dusty", "rose"], Counter({"nude": 1, "tones": 1, "or": 1, "dusty": 1, "rose": 1}))
    def test_case_39(self): self.run_test("refined finish. timeless appeal", ["refined", "finish", ".", "timeless", "appeal"], Counter({"refined": 1, "finish": 1, ".": 1, "timeless": 1, "appeal": 1}))
    def test_case_40(self): self.run_test("I'm unsure", ["i", "'m", "unsure"], Counter({"i": 1, "'m": 1, "unsure": 1}))
    def test_case_41(self): self.run_test("vibrant tones!", ["vibrant", "tones", "!"], Counter({"vibrant": 1, "tones": 1, "!": 1}))
    def test_case_42(self): self.run_test("rosy flush + peach glow", ["rosy", "flush", "+", "peach", "glow"], Counter({"rosy": 1, "flush": 1, "+": 1, "peach": 1, "glow": 1}))
    def test_case_43(self): self.run_test("greenish-blue shade", ["greenish", "-", "blue", "shade"], Counter({"greenish": 1, "-": 1, "blue": 1, "shade": 1}))
    def test_case_44(self): self.run_test("bold / dramatic", ["bold", "/", "dramatic"], Counter({"bold": 1, "/": 1, "dramatic": 1}))
    def test_case_45(self): self.run_test("clean natural fresh look", ["clean", "natural", "fresh", "look"], Counter({"clean": 1, "natural": 1, "fresh": 1, "look": 1}))
    def test_case_46(self): self.run_test("matte-mauve lips", ["matte", "-", "mauve", "lips"], Counter({"matte": 1, "-": 1, "mauve": 1, "lips": 1}))
    def test_case_47(self): self.run_test("neutral-ish shades", ["neutral", "-", "ish", "shades"], Counter({"neutral": 1, "-": 1, "ish": 1, "shades": 1}))
    def test_case_48(self): self.run_test("pinky coral cheeks", ["pinky", "coral", "cheeks"], Counter({"pinky": 1, "coral": 1, "cheeks": 1}))
    def test_case_49(self): self.run_test("natural everyday glow", ["natural", "everyday", "glow"], Counter({"natural": 1, "everyday": 1, "glow": 1}))
    def test_case_50(self): self.run_test("soft finish + radiant look", ["soft", "finish", "+", "radiant", "look"], Counter({"soft": 1, "finish": 1, "+": 1, "radiant": 1, "look": 1}))

