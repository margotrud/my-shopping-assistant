# tests/extractors/general/helpers/test_split_glued_tokens.py

import unittest
from Chatbot.extractors.color.utils.token_utils import split_glued_tokens
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

class TestSplitGluedTokens(unittest.TestCase):

    def setUp(self):
        from Chatbot.extractors.color import known_tones, all_webcolor_names

        self.known_tokens = load_known_modifiers().union(known_tones, all_webcolor_names)


    def test_case_01(self): self.assertEqual(["soft", "pink"], split_glued_tokens("softpink", self.known_tokens))
    def test_case_02(self): self.assertEqual(["deep", "blue"], split_glued_tokens("deepblue", self.known_tokens))
    def test_case_03(self): self.assertEqual(["light", "green"], split_glued_tokens("lightgreen", self.known_tokens))
    def test_case_04(self): self.assertEqual(["cool", "tone"], split_glued_tokens("cooltone", self.known_tokens))
    def test_case_05(self): self.assertEqual(["warm", "tone"], split_glued_tokens("warmtone", self.known_tokens))
    def test_case_06(self): self.assertEqual(["bright", "red"], split_glued_tokens("brightred", self.known_tokens))
    def test_case_07(self): self.assertEqual(["gold", "tone"], split_glued_tokens("goldtone", self.known_tokens))
    def test_case_08(self): self.assertEqual(["peach", "tone"], split_glued_tokens("peachtone", self.known_tokens))
    def test_case_09(self): self.assertEqual(["rose", "gold"], split_glued_tokens("rosegold", self.known_tokens))
    def test_case_10(self): self.assertEqual(["beige", "tone"], split_glued_tokens("beigetone", self.known_tokens))

    def test_case_11(self): self.assertEqual(["brown", "tone"], split_glued_tokens("browntone", self.known_tokens))
    def test_case_12(self): self.assertEqual(["grey", "blue"], split_glued_tokens("greyblue", self.known_tokens))
    def test_case_13(self): self.assertEqual(["gray", "tone"], split_glued_tokens("graytone", self.known_tokens))
    def test_case_14(self): self.assertEqual(["violet", "tone"], split_glued_tokens("violettone", self.known_tokens))
    def test_case_15(self): self.assertEqual(["aqua", "tone"], split_glued_tokens("aquatone", self.known_tokens))
    def test_case_16(self): self.assertEqual(["mint", "tone"], split_glued_tokens("minttone", self.known_tokens))
    def test_case_17(self): self.assertEqual(["coral", "pink"], split_glued_tokens("coralpink", self.known_tokens))
    def test_case_18(self): self.assertEqual(["nude", "rose"], split_glued_tokens("nuderose", self.known_tokens))
    def test_case_19(self): self.assertEqual(["ivory", "tone"], split_glued_tokens("ivorytone", self.known_tokens))
    def test_case_20(self): self.assertEqual(["pale", "rose"], split_glued_tokens("palerose", self.known_tokens))

    def test_case_21(self): self.assertEqual(["dark", "rose"], split_glued_tokens("darkrose", self.known_tokens))
    def test_case_22(self): self.assertEqual(["soft", "brown"], split_glued_tokens("softbrown", self.known_tokens))
    def test_case_23(self): self.assertEqual(["cool", "brown"], split_glued_tokens("coolbrown", self.known_tokens))
    def test_case_24(self): self.assertEqual(["olive", "tone"], split_glued_tokens("olivetone", self.known_tokens))
    def test_case_25(self): self.assertEqual(["bronze", "tone"], split_glued_tokens("bronzetone", self.known_tokens))
    def test_case_26(self): self.assertEqual(["dusty", "rose"], split_glued_tokens("dustyrose", self.known_tokens))
    def test_case_27(self): self.assertEqual(["blush", "pink"], split_glued_tokens("blushpink", self.known_tokens))
    def test_case_28(self): self.assertEqual(["mauve", "tone"], split_glued_tokens("mauvetone", self.known_tokens))
    def test_case_29(self): self.assertEqual(["peach", "pink"], split_glued_tokens("peachpink", self.known_tokens))
    def test_case_30(self): self.assertEqual(["warm", "pink"], split_glued_tokens("warmpink", self.known_tokens))

    def test_case_31(self): self.assertEqual(["cool", "peach"], split_glued_tokens("coolpeach", self.known_tokens))
    def test_case_32(self): self.assertEqual(["light", "coral"], split_glued_tokens("lightcoral", self.known_tokens))
    def test_case_33(self): self.assertEqual(["deep", "rose"], split_glued_tokens("deeprose", self.known_tokens))
    def test_case_34(self): self.assertEqual(["dark", "green"], split_glued_tokens("darkgreen", self.known_tokens))
    def test_case_35(self): self.assertEqual(["soft", "blush"], split_glued_tokens("softblush", self.known_tokens))
    def test_case_36(self): self.assertEqual(["cool", "blush"], split_glued_tokens("coolblush", self.known_tokens))
    def test_case_37(self): self.assertEqual(["neutral", "tone"], split_glued_tokens("neutraltone", self.known_tokens))
    def test_case_38(self): self.assertEqual(["bright", "tone"], split_glued_tokens("brighttone", self.known_tokens))
    def test_case_39(self): self.assertEqual(["olive", "green"], split_glued_tokens("olivegreen", self.known_tokens))
    def test_case_40(self): self.assertEqual(["mint", "green"], split_glued_tokens("mintgreen", self.known_tokens))

    def test_case_41(self): self.assertEqual(["blue"], split_glued_tokens("blue", self.known_tokens))
    def test_case_42(self): self.assertEqual(["pink"], split_glued_tokens("pink", self.known_tokens))
    def test_case_43(self): self.assertEqual(["mauve"], split_glued_tokens("mauve", self.known_tokens))
    def test_case_44(self): self.assertEqual(["nude"], split_glued_tokens("nude", self.known_tokens))
    def test_case_45(self): self.assertEqual(["coral"], split_glued_tokens("coral", self.known_tokens))
    def test_case_46(self): self.assertEqual(["brown", "gray"], split_glued_tokens("browngray", {"brown", "green"}))  # local override
    def test_case_47(self): self.assertEqual([], split_glued_tokens("unknowncolor", self.known_tokens))
    def test_case_48(self): self.assertEqual(["deep","bluish"], split_glued_tokens("deepbluish", self.known_tokens))
    def test_case_49(self): self.assertEqual([], split_glued_tokens("", self.known_tokens))
    def test_case_50(self): self.assertEqual([], split_glued_tokens("xyz", self.known_tokens))
