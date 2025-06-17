# tests/helpers/test_resolve_modifier_token.py

import unittest
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token, fuzzy_match_modifier
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color import known_tones

class TestResolveModifierToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()
        cls.known_tones = known_tones

    def test_case_01(self): self.assertEqual("soft", resolve_modifier_token("soft", self.known_modifiers))
    def test_case_02(self): self.assertEqual("bold", resolve_modifier_token("bold", self.known_modifiers))
    def test_case_03(self): self.assertEqual("clean", resolve_modifier_token("clean", self.known_modifiers))
    def test_case_04(self): self.assertEqual("bare", resolve_modifier_token("bare", self.known_modifiers))
    def test_case_05(self): self.assertEqual("soft", resolve_modifier_token("softy", self.known_modifiers))
    def test_case_06(self): self.assertEqual("bold", resolve_modifier_token("boldish", self.known_modifiers))
    def test_case_07(self): self.assertEqual("clean", resolve_modifier_token("cleany", self.known_modifiers))
    def test_case_08(self): self.assertEqual("bare", resolve_modifier_token("barely", self.known_modifiers))
    def test_case_09(self): self.assertEqual("natural", resolve_modifier_token("naturally", self.known_modifiers))
    def test_case_10(self): self.assertEqual("bare", resolve_modifier_token("bare", self.known_modifiers, allow_fuzzy=False))
    def test_case_11(self): self.assertEqual("glossy", resolve_modifier_token("glossyy", self.known_modifiers))
    def test_case_12(self): self.assertEqual("bare", resolve_modifier_token("bareish", self.known_modifiers))
    def test_case_13(self): self.assertEqual("pinkish", resolve_modifier_token("pinkish", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_14(self): self.assertEqual("red", resolve_modifier_token("reddy", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_15(self): self.assertEqual("peachy", resolve_modifier_token("peachy", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_16(self): self.assertIsNone(resolve_modifier_token("elegant", self.known_modifiers, allow_fuzzy=False))
    def test_case_17(self): self.assertEqual("natural", resolve_modifier_token("natral", self.known_modifiers))
    def test_case_18(self): self.assertIsNone(resolve_modifier_token("glossing", self.known_modifiers, allow_fuzzy=False))
    def test_case_19(self): self.assertEqual("natural", resolve_modifier_token("naturly", self.known_modifiers))
    def test_case_20(self): self.assertEqual("cool", resolve_modifier_token("coolish", self.known_modifiers))
    def test_case_21(self): self.assertIsNone(resolve_modifier_token("hot", self.known_modifiers))
    def test_case_22(self): self.assertIsNone(resolve_modifier_token("boldred", self.known_modifiers))
    def test_case_23(self): self.assertEqual("warm", resolve_modifier_token("warmish", self.known_modifiers))
    def test_case_24(self): self.assertIsNone(resolve_modifier_token("nothing", self.known_modifiers))
    def test_case_25(self): self.assertEqual("nude", resolve_modifier_token("nudy", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_26(self): self.assertEqual("beige", resolve_modifier_token("beigey", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_27(self): self.assertEqual("mocha", resolve_modifier_token("mochish", self.known_modifiers, self.known_tones, is_tone=True))
    def test_case_28(self): self.assertEqual("bare", resolve_modifier_token("bareish", self.known_modifiers))

    def test_case_29(self):
        self.assertEqual(resolve_modifier_token("dusty", self.known_modifiers, allow_fuzzy=False), "dusty")

    def test_case_30(self): self.assertEqual("clean", resolve_modifier_token("cleanish", self.known_modifiers))
    def test_case_31(self): self.assertEqual("soft", resolve_modifier_token("sooft", self.known_modifiers))
    def test_case_32(self): self.assertEqual("natural", resolve_modifier_token("natraly", self.known_modifiers))
    def test_case_33(self): self.assertEqual("bare", resolve_modifier_token("bare", self.known_modifiers, allow_fuzzy=False))
    def test_case_34(self): self.assertEqual("bold", resolve_modifier_token("boldy", self.known_modifiers))
    def test_case_35(self): self.assertEqual("warm", resolve_modifier_token("warmy", self.known_modifiers))
    def test_case_36(self): self.assertIsNone(resolve_modifier_token("", self.known_modifiers))
    def test_case_37(self): self.assertEqual("soft", resolve_modifier_token("SOFT", self.known_modifiers))
    def test_case_38(self): self.assertEqual("bold", resolve_modifier_token("Bold", self.known_modifiers))
    def test_case_39(self): self.assertEqual("cool", resolve_modifier_token("CoolY", self.known_modifiers))
    def test_case_40(self): self.assertEqual("glossy", resolve_modifier_token("Glossish", self.known_modifiers))
    def test_case_41(self): self.assertEqual("warm", resolve_modifier_token("warms", self.known_modifiers))
    def test_case_42(self): self.assertEqual("clean", resolve_modifier_token("cleanish", self.known_modifiers))
    def test_case_43(self): self.assertEqual("glossy", resolve_modifier_token("glosy", self.known_modifiers))
    def test_case_44(self): self.assertEqual("soft", resolve_modifier_token("soofty", self.known_modifiers))
    def test_case_45(self): self.assertEqual("natural", resolve_modifier_token("natural", self.known_modifiers))
    def test_case_46(self): self.assertIsNone(resolve_modifier_token("elegance", self.known_modifiers))
    def test_case_47(self): self.assertIsNone(resolve_modifier_token("exotic", self.known_modifiers))
    def test_case_48(self): self.assertEqual("bare", resolve_modifier_token("bare-ish", self.known_modifiers))
    def test_case_49(self): self.assertEqual("bold", resolve_modifier_token("bold-ish", self.known_modifiers))
    def test_case_50(self): self.assertIsNone(resolve_modifier_token("x", self.known_modifiers))


if __name__ == "__main__":
    unittest.main()
