import unittest
from Chatbot.extractors.general.helpers import split_glued_tokens
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.core.matcher import load_known_modifiers

class TestSplitGluedTokens(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known = known_tones.union(load_known_modifiers())

    def test_case_01(self): self.assertEqual([], split_glued_tokens("greige", self.known))
    def test_case_02(self): self.assertEqual([], split_glued_tokens("rosewood", self.known))
    def test_case_03(self): self.assertEqual(["soft", "pink"], split_glued_tokens("softpink", self.known))
    def test_case_04(self): self.assertEqual(["light", "mauve"], split_glued_tokens("lightmauve", self.known))
    def test_case_05(self): self.assertEqual(["deep", "nude"], split_glued_tokens("deepnude", self.known))
    def test_case_06(self): self.assertEqual(["burnt", "orange"], split_glued_tokens("burntorange", self.known))
    def test_case_07(self): self.assertEqual(["cool", "beige"], split_glued_tokens("coolbeige", self.known))
    def test_case_08(self): self.assertEqual(["peach", "brown"], split_glued_tokens("peachbrown", self.known))
    def test_case_09(self): self.assertEqual(["pink", "taupe"], split_glued_tokens("pinktaupe", self.known))
    def test_case_10(self): self.assertEqual(["tan", "gold"], split_glued_tokens("tangold", self.known))
    def test_case_11(self): self.assertEqual(["gold", "bronze"], split_glued_tokens("goldbronze", self.known))
    def test_case_12(self): self.assertEqual([], split_glued_tokens("nonmatch", self.known))
    def test_case_13(self): self.assertEqual(["deep", "red"], split_glued_tokens("deepred", self.known))
    def test_case_14(self): self.assertEqual(["blush", "rose"], split_glued_tokens("blushrose", self.known))
    def test_case_15(self): self.assertEqual(["cool", "pink"], split_glued_tokens("coolpink", self.known))
    def test_case_16(self): self.assertEqual(["light", "peach"], split_glued_tokens("lightpeach", self.known))
    def test_case_17(self): self.assertEqual(["soft", "blush"], split_glued_tokens("softblush", self.known))
    def test_case_18(self): self.assertEqual(["pink", "beige"], split_glued_tokens("pinkbeige", self.known))
    def test_case_19(self): self.assertEqual(["grey", "rose"], split_glued_tokens("greyrose", self.known))
    def test_case_20(self): self.assertEqual(["bare", "mauve"], split_glued_tokens("baremauve", self.known))

    def test_case_21(self): self.assertEqual(["rosy", "glow"], split_glued_tokens("rosyglow", self.known))
    def test_case_22(self): self.assertEqual([], split_glued_tokens("naturaltone", self.known))
    def test_case_23(self): self.assertEqual(["bare", "peach"], split_glued_tokens("barepeach", self.known))
    def test_case_24(self): self.assertEqual(["muted", "rose"], split_glued_tokens("mutedrose", self.known))
    def test_case_25(self): self.assertEqual(["warm", "mauve"], split_glued_tokens("warmmauve", self.known))
    def test_case_26(self): self.assertEqual(["light", "blush"], split_glued_tokens("lightblush", self.known))
    def test_case_27(self): self.assertEqual(["burnt", "peach"], split_glued_tokens("burntpeach", self.known))
    def test_case_28(self): self.assertEqual(["intense", "red"], split_glued_tokens("intensered", self.known))
    def test_case_29(self): self.assertEqual(["soft", "taupe"], split_glued_tokens("softtaupe", self.known))
    def test_case_30(self): self.assertEqual(["dusty", "rose"], split_glued_tokens("dustyrose", self.known))

    def test_case_31(self): self.assertEqual(["warm", "beige"], split_glued_tokens("warmbeige", self.known))
    def test_case_32(self): self.assertEqual(["nude", "peach"], split_glued_tokens("nudepeach", self.known))
    def test_case_33(self): self.assertEqual(["blush", "bronze"], split_glued_tokens("blushbronze", self.known))
    def test_case_34(self): self.assertEqual(["red", "orange"], split_glued_tokens("redorange", self.known))
    def test_case_35(self): self.assertEqual(["natural", "pink"], split_glued_tokens("naturalpink", self.known))
    def test_case_36(self): self.assertEqual([], split_glued_tokens("peachtone", self.known))
    def test_case_37(self): self.assertEqual(["bare", "blush"], split_glued_tokens("bareblush", self.known))
    def test_case_38(self): self.assertEqual(["cool", "taupe"], split_glued_tokens("cooltaupe", self.known))
    def test_case_39(self): self.assertEqual(["deep", "beige"], split_glued_tokens("deepbeige", self.known))
    def test_case_40(self): self.assertEqual(["light", "rose"], split_glued_tokens("lightrose", self.known))

    def test_case_41(self): self.assertEqual(['rose', 'pink', 'gold'], split_glued_tokens("rosepinkgold", self.known))  # triple not supported
    def test_case_42(self): self.assertEqual(["light", "gold"], split_glued_tokens("lightgold", self.known))
    def test_case_43(self): self.assertEqual(["deep", "brown"], split_glued_tokens("deepbrown", self.known))
    def test_case_44(self): self.assertEqual(["burnt", "gold"], split_glued_tokens("burntgold", self.known))
    def test_case_45(self): self.assertEqual(["natural", "glow"], split_glued_tokens("naturalglow", self.known))
    def test_case_46(self): self.assertEqual(["bare", "nude"], split_glued_tokens("barenude", self.known))
    def test_case_47(self): self.assertEqual(["grey", "gold"], split_glued_tokens("greygold", self.known))
    def test_case_48(self): self.assertEqual([], split_glued_tokens("rosyshine", self.known))
    def test_case_49(self): self.assertEqual(["blush", "mauve"], split_glued_tokens("blushmauve", self.known))
    def test_case_50(self): self.assertEqual([], split_glued_tokens("invisiblematch", self.known))

if __name__ == "__main__":
    unittest.main()
