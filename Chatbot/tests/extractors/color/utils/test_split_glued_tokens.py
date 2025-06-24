# Chatbot/tests/extractors/color/utils/test_split_glued_tokens.py

import unittest
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
known_modifiers = load_known_modifiers()

known_tokens = known_tones.union(known_modifiers)

class TestSplitGluedTokens(unittest.TestCase):

    def run_case(self, token: str, expected: list):
        result = split_glued_tokens(token, known_tokens, known_modifiers)
        self.assertEqual(expected, result, msg=f"\nExpected : {expected}\nActual   : {result}")

    def test_case_01(self): self.run_case("dustyrose", ["dusty", "rose"])
    def test_case_02(self): self.run_case("mutedbeige", ["muted", "beige"])
    def test_case_03(self): self.run_case("softpink", ["soft", "pink"])
    def test_case_04(self): self.run_case("warmtaupe", ["warm", "taupe"])
    def test_case_05(self): self.run_case("deepnude", ["deep", "nude"])

    def test_case_06(self): self.run_case("richmocha", ["rich", "mocha"])
    def test_case_07(self): self.run_case("lightpeach", ["light", "peach"])
    def test_case_08(self): self.run_case("palesienna", ["pale", "sienna"])
    def test_case_09(self): self.run_case("darkcoral", ["dark", "coral"])
    def test_case_10(self): self.run_case("coolplum", ["cool", "plum"])

    def test_case_11(self): self.run_case("neutralblush", ["neutral", "blush"])
    def test_case_12(self): self.run_case("bronzyglow", ["bronzy", "glow"])
    def test_case_13(self): self.run_case("mochabrown", ["mocha", "brown"])
    def test_case_14(self): self.run_case("boldblue", ["bold", "blue"])
    def test_case_15(self): self.run_case("icygray", ["icy", "gray"])

    def test_case_16(self): self.run_case("intensedust", ["intense", "dust"])
    def test_case_17(self): self.run_case("brightivory", ["bright", "ivory"])
    def test_case_18(self): self.run_case("creampink", ["cream", "pink"])
    def test_case_19(self): self.run_case("earthyrose", ["earthy", "rose"])
    def test_case_20(self): self.run_case("rosybrown", ["rosybrown"])

    def test_case_21(self): self.run_case("nudesand", ["nude", "sand"])
    def test_case_22(self): self.run_case("glowbronze", ["glow", "bronze"])
    def test_case_23(self): self.run_case("satinbeige", ["satin", "beige"])
    def test_case_24(self): self.run_case("peachgold", ["peach", "gold"])
    def test_case_25(self): self.run_case("warmgold", ["warm", "gold"])

    def test_case_26(self): self.run_case("berrydust", ["berry", "dust"])
    def test_case_27(self): self.run_case("rosewood", ["rose", "wood"])
    def test_case_28(self): self.run_case("sandstone", ["sandstone"])
    def test_case_29(self): self.run_case("mattenude", ["matte", "nude"])
    def test_case_30(self): self.run_case("boldberry", ["bold", "berry"])

    def test_case_31(self): self.run_case("ultradeep", ["ultra", "deep"])
    def test_case_32(self): self.run_case("warmivory", ["warm", "ivory"])
    def test_case_33(self): self.run_case("fuzzygreen", ["fuzzy","green"])
    def test_case_34(self): self.run_case("mutedrosewood", ["muted", "rosewood"])
    def test_case_35(self): self.run_case("beigebei", ["beige", "bei"])

    def test_case_36(self): self.run_case("soft", ["soft"])
    def test_case_37(self): self.run_case("nud", [])   # too short
    def test_case_38(self): self.run_case("abc", [])   # nonsense token
    def test_case_39(self): self.run_case("rosedusty", ["rose", "dusty"])
    def test_case_40(self): self.run_case("yellowblue", ["yellow", "blue"])

    def test_case_41(self): self.run_case("graywhite", ["gray", "white"])
    def test_case_42(self): self.run_case("neutralgray", ["neutral", "gray"])
    def test_case_43(self): self.run_case("cooltone", ["cool", "tone"])
    def test_case_44(self): self.run_case("tonecool", ["tone", "cool"])
    def test_case_45(self): self.run_case("sandivory", ["sand", "ivory"])

    def test_case_46(self): self.run_case("creamrose", ["cream", "rose"])
    def test_case_47(self): self.run_case("satinplum", ["satin", "plum"])
    def test_case_48(self): self.run_case("mattetan", ["matte", "tan"])
    def test_case_49(self): self.run_case("glowybronze", ["glowy", "bronze"])
    def test_case_50(self): self.run_case("glamrose", ["glam", "rose"])

if __name__ == "__main__":
    unittest.main()
