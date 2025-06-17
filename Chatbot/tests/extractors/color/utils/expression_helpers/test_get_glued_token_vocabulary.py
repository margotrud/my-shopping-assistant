# tests/helpers/test_get_glued_token_vocabulary.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.expression_helpers import get_glued_token_vocabulary

class TestGetGluedTokenVocabulary(unittest.TestCase):

    def test_case_01(self): self.assertTrue("pink" in get_glued_token_vocabulary())
    def test_case_02(self): self.assertTrue("bold" in get_glued_token_vocabulary())
    def test_case_03(self): self.assertFalse("light pink" in get_glued_token_vocabulary())
    def test_case_04(self): self.assertTrue("red" in get_glued_token_vocabulary())
    def test_case_05(self): self.assertTrue("soft" in get_glued_token_vocabulary())
    def test_case_06(self): self.assertFalse("deep pink" in get_glued_token_vocabulary())
    def test_case_07(self): self.assertTrue("nude" in get_glued_token_vocabulary())
    def test_case_08(self): self.assertFalse("glossy finish" in get_glued_token_vocabulary())
    def test_case_09(self): self.assertTrue("beige" in get_glued_token_vocabulary())
    def test_case_10(self): self.assertTrue("bright" in get_glued_token_vocabulary())

    # Stress-test boundary cases with lowercase & spacing expectations
    def test_case_11(self): self.assertFalse(" bold" in get_glued_token_vocabulary())
    def test_case_12(self): self.assertFalse("soft " in get_glued_token_vocabulary())
    def test_case_13(self): self.assertFalse(" soft " in get_glued_token_vocabulary())
    def test_case_14(self): self.assertTrue("blue" in get_glued_token_vocabulary())
    def test_case_15(self): self.assertFalse("blue green" in get_glued_token_vocabulary())
    def test_case_16(self): self.assertFalse(" " in get_glued_token_vocabulary())
    def test_case_17(self): self.assertFalse("" in get_glued_token_vocabulary())
    def test_case_18(self): self.assertFalse("soft pink" in get_glued_token_vocabulary())
    def test_case_19(self): self.assertTrue("green" in get_glued_token_vocabulary())
    def test_case_20(self): self.assertTrue("warm" in get_glued_token_vocabulary())

    # Consistency checks
    def test_case_21(self): self.assertEqual(len(get_glued_token_vocabulary() - known_tones.union(load_known_modifiers())), 0)
    def test_case_22(self): self.assertTrue(all(" " not in t for t in get_glued_token_vocabulary()))
    def test_case_23(self): self.assertTrue(all(isinstance(t, str) for t in get_glued_token_vocabulary()))
    def test_case_24(self): self.assertTrue(len(get_glued_token_vocabulary()) > 10)
    def test_case_25(self): self.assertTrue("black" in get_glued_token_vocabulary())
    def test_case_26(self): self.assertTrue("orange" in get_glued_token_vocabulary())
    def test_case_27(self): self.assertTrue("yellow" in get_glued_token_vocabulary())
    def test_case_28(self): self.assertTrue("gray" in get_glued_token_vocabulary() or "grey" in get_glued_token_vocabulary())
    def test_case_29(self): self.assertTrue("cool" in get_glued_token_vocabulary() or "cool-toned" not in get_glued_token_vocabulary())
    def test_case_30(self): self.assertTrue("warm" in get_glued_token_vocabulary())

    # Edge additions
    def test_case_31(self): self.assertFalse("rosy glow" in get_glued_token_vocabulary())
    def test_case_32(self): self.assertTrue("rosy" in get_glued_token_vocabulary())
    def test_case_33(self): self.assertTrue("peach" in get_glued_token_vocabulary())
    def test_case_34(self): self.assertFalse("peach beige" in get_glued_token_vocabulary())
    def test_case_35(self): self.assertTrue("bronze" in get_glued_token_vocabulary())
    def test_case_36(self): self.assertFalse("bronzed" not in get_glued_token_vocabulary())
    def test_case_37(self): self.assertTrue("classic" in get_glued_token_vocabulary())
    def test_case_38(self): self.assertTrue("natural" in get_glued_token_vocabulary())
    def test_case_39(self): self.assertFalse("natural finish" in get_glued_token_vocabulary())
    def test_case_40(self): self.assertTrue("muted" in get_glued_token_vocabulary())

    # Final stress tests (immutability)
    def test_case_41(self): self.assertEqual(get_glued_token_vocabulary(), get_glued_token_vocabulary())
    def test_case_42(self): self.assertIsInstance(get_glued_token_vocabulary(), set)
    def test_case_43(self): self.assertTrue("fuchsia" in get_glued_token_vocabulary())
    def test_case_44(self): self.assertTrue("charcoal" in get_glued_token_vocabulary())
    def test_case_45(self): self.assertFalse("shiny red" in get_glued_token_vocabulary())
    def test_case_46(self): self.assertTrue("softened" not in get_glued_token_vocabulary())
    def test_case_47(self): self.assertTrue("bare" in get_glued_token_vocabulary())
    def test_case_48(self): self.assertTrue("rich" in get_glued_token_vocabulary())
    def test_case_49(self): self.assertTrue("mocha" in get_glued_token_vocabulary())
    def test_case_50(self): self.assertFalse("glow up" in get_glued_token_vocabulary())

if __name__ == "__main__":
    unittest.main()
