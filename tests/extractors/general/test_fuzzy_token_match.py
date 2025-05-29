#tests/extractors/general/test_fuzzy_token_match.py

import unittest
from Chatbot.extractors.general.helpers import fuzzy_token_match

class TestFuzzyTokenMatch(unittest.TestCase):

    def test_case_01(self): self.assertEqual(True, fuzzy_token_match("pink", "pink"))

    def test_case_02(self): self.assertEqual(True, fuzzy_token_match("pink", "pinkish"))

    def test_case_03(self): self.assertEqual(True, fuzzy_token_match("nude", "nudes"))

    def test_case_04(self): self.assertEqual(True, fuzzy_token_match("rosy", "rose"))

    def test_case_05(self): self.assertEqual(True, fuzzy_token_match("muted", "mutted"))

    def test_case_06(self): self.assertEqual(True, fuzzy_token_match("soft", "sofft"))

    def test_case_07(self): self.assertEqual(True, fuzzy_token_match("glam", "glamy"))

    def test_case_08(self): self.assertEqual(True, fuzzy_token_match("bare", "barre"))

    def test_case_09(self): self.assertEqual(True, fuzzy_token_match("gold", "goold"))

    def test_case_10(self): self.assertEqual(True, fuzzy_token_match("deep", "deap"))

    def test_case_11(self): self.assertEqual(True, fuzzy_token_match("tan", "tann"))

    def test_case_12(self): self.assertEqual(True, fuzzy_token_match("peach", "peech"))

    def test_case_13(self): self.assertEqual(True, fuzzy_token_match("cool", "cooool"))

    def test_case_14(self): self.assertEqual(True, fuzzy_token_match("dusty", "dussty"))

    def test_case_15(self): self.assertEqual(True, fuzzy_token_match("blush", "blsh"))

    def test_case_16(self): self.assertEqual(True, fuzzy_token_match("coral", "cora"))

    def test_case_17(self): self.assertEqual(True, fuzzy_token_match("warm", "warrm"))

    def test_case_18(self): self.assertEqual(False, fuzzy_token_match("moody", "muddy"))

    def test_case_19(self): self.assertEqual(True, fuzzy_token_match("retro", "ratro"))

    def test_case_20(self): self.assertEqual(False, fuzzy_token_match("soft", "hard"))

    def test_case_21(self): self.assertEqual(True, fuzzy_token_match("sun", "sunkissed"))

    def test_case_22(self): self.assertEqual(True, fuzzy_token_match("bronze", "bronzed"))

    def test_case_23(self): self.assertEqual(True, fuzzy_token_match("clean", "clen"))

    def test_case_24(self): self.assertEqual(True, fuzzy_token_match("barely", "barely-there"))

    def test_case_25(self): self.assertEqual(True, fuzzy_token_match("glow", "glowy"))

    def test_case_26(self): self.assertEqual(False, fuzzy_token_match("soft", "sofisticated"))

    def test_case_27(self): self.assertEqual(True, fuzzy_token_match("red", "reddish"))

    def test_case_28(self): self.assertEqual(True, fuzzy_token_match("bright", "brighte"))

    def test_case_29(self): self.assertEqual(True, fuzzy_token_match("classic", "classique"))

    def test_case_30(self): self.assertEqual(True, fuzzy_token_match("dramatic", "drama"))

    def test_case_31(self): self.assertEqual(False, fuzzy_token_match("effortless", "effortfull"))

    def test_case_32(self): self.assertEqual(True, fuzzy_token_match("beige", "beig"))

    def test_case_33(self): self.assertEqual(False, fuzzy_token_match("nude", "newd"))

    def test_case_34(self): self.assertEqual(True, fuzzy_token_match("romantic", "romantique"))

    def test_case_35(self): self.assertEqual(False, fuzzy_token_match("light", "lite"))

    def test_case_36(self): self.assertEqual(True, fuzzy_token_match("earthy", "earth"))

    def test_case_37(self): self.assertEqual(True, fuzzy_token_match("tan", "tanned"))

    def test_case_38(self): self.assertEqual(True, fuzzy_token_match("sparkle", "sparkly"))

    def test_case_39(self): self.assertEqual(True, fuzzy_token_match("glitter", "glittr"))

    def test_case_40(self): self.assertEqual(True, fuzzy_token_match("minimal", "miniml"))

    def test_case_41(self): self.assertEqual(True, fuzzy_token_match("peach", "preach"))

    def test_case_42(self): self.assertEqual(True, fuzzy_token_match("muted", "mutted"))

    def test_case_43(self): self.assertEqual(True, fuzzy_token_match("rosy", "rosey"))

    def test_case_44(self): self.assertEqual(True, fuzzy_token_match("blush", "plush"))

    def test_case_45(self): self.assertEqual(False, fuzzy_token_match("golden", "gilded"))

    def test_case_46(self): self.assertEqual(False, fuzzy_token_match("tan", "taupe"))

    def test_case_47(self): self.assertEqual(True, fuzzy_token_match("red", "read"))

    def test_case_48(self): self.assertEqual(True, fuzzy_token_match("warm", "worm"))

    def test_case_49(self): self.assertEqual(True, fuzzy_token_match("cool", "coal"))

    def test_case_50(self): self.assertEqual(False, fuzzy_token_match("soft", "strong"))


if __name__ == "__main__":
    unittest.main()