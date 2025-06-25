# test_split_tokens_to_parts.py

import unittest
from Chatbot.extractors.color.extraction.compound import split_tokens_to_parts
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
known_modifiers = load_known_modifiers()

class TestSplitTokensToParts(unittest.TestCase):

    def setUp(self):
        self.known_color_tokens = known_modifiers.union(known_tones).union(all_webcolor_names)

    def run_case(self, text, expected):
        result = split_tokens_to_parts(text, self.known_color_tokens)
        print(f"\n[INPUT] {text}")
        print(f"[EXPECTED] {expected}")
        print(f"[ACTUAL]   {result}")
        self.assertEqual(expected, result)
    def test_case_01(self): self.run_case("soft-pink", ["soft", "pink"])
    def test_case_02(self): self.run_case("muted-rose", ["muted", "rose"])
    def test_case_03(self): self.run_case("deep-coral", ["deep", "coral"])
    def test_case_04(self): self.run_case("light-blue", ["light", "blue"])
    def test_case_05(self): self.run_case("rich-brown", ["rich", "brown"])

    def test_case_06(self): self.run_case("dustyrose", ["dusty", "rose"])
    def test_case_07(self): self.run_case("creamyivory", ["creamy", "ivory"])
    def test_case_08(self): self.run_case("coolmint", ["cool", "mint"])
    def test_case_09(self): self.run_case("darkgreen", ["dark", "green"])
    def test_case_10(self): self.run_case("palepeach", ["pale", "peach"])

    def test_case_11(self): self.run_case("vibrantred", ["vibrant", "red"])
    def test_case_12(self): self.run_case("icygray", ["icy", "gray"])
    def test_case_13(self): self.run_case("rosynude", ["rosy", "nude"])
    def test_case_14(self): self.run_case("boldyellow", ["bold", "yellow"])
    def test_case_15(self): self.run_case("subtletaupe", ["subtle", "taupe"])

    def test_case_16(self): self.run_case("barelythere", None)
    def test_case_17(self): self.run_case("burntorange", None)
    def test_case_18(self): self.run_case("neutralcream", ["neutral", "cream"])
    def test_case_19(self): self.run_case("glowybronze", ["glowy", "bronze"])
    def test_case_20(self): self.run_case("dewyrose", ["dewy", "rose"])

    def test_case_21(self): self.run_case("inkblot", None)
    def test_case_22(self): self.run_case("ashbrown", ["ash", "brown"])
    def test_case_23(self): self.run_case("peachybeige", ["peachy", "beige"])
    def test_case_24(self): self.run_case("mistgrey", None)
    def test_case_25(self): self.run_case("glossyred", ["glossy", "red"])

    def test_case_26(self): self.run_case("nightshade", None)
    def test_case_27(self): self.run_case("sunsetgold", None)
    def test_case_28(self): self.run_case("candlelight", None)
    def test_case_29(self): self.run_case("eveningtone", None)
    def test_case_30(self): self.run_case("bluesky", ["blue", "sky"])

    def test_case_31(self): self.run_case("123pink", None)
    def test_case_32(self): self.run_case("soft123pink", None)
    def test_case_33(self): self.run_case("!mutedrose", None)
    def test_case_34(self): self.run_case("rose!", None)
    def test_case_35(self): self.run_case("blu3gray", None)

    def test_case_36(self): self.run_case("a", None)
    def test_case_37(self): self.run_case("ab", None)
    def test_case_38(self): self.run_case("abc", None)
    def test_case_39(self): self.run_case("abcd", None)
    def test_case_40(self): self.run_case("", None)

    def test_case_41(self): self.run_case("longword-yellow", None)
    def test_case_42(self): self.run_case("dusty-rose", ["dusty", "rose"])
    def test_case_43(self): self.run_case("natural-beige", ["natural", "beige"])
    def test_case_44(self): self.run_case("peach-blush", ["peach", "blush"])
    def test_case_45(self): self.run_case("olive-toned", ["olive", "toned"])

    def test_case_46(self): self.run_case("freshmint", ["fresh", "mint"])
    def test_case_47(self): self.run_case("earthybrown", ["earthy", "brown"])
    def test_case_48(self): self.run_case("hazelgreen", ["hazel", "green"])
    def test_case_49(self): self.run_case("bronzeblend", ["bronze", "blend"])
    def test_case_50(self): self.run_case("mattemocha", ["matte", "mocha"])


if __name__ == "__main__":
    unittest.main()
