# test_attempt_mod_tone_pair.py

import unittest
from Chatbot.extractors.color.extraction.compound import attempt_mod_tone_pair
from Chatbot.extractors.color.shared.vocab import known_tones, all_webcolor_names
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

known_modifiers = load_known_modifiers()
class TestAttemptModTonePair(unittest.TestCase):

    def setUp(self):
        self.known_modifiers = known_modifiers
        self.known_tones = known_tones
        self.webcolors = all_webcolor_names

    def run_case(self, mod_candidate, tone_candidate, expected_compound):
        compounds = set()
        raw_compounds = []
        attempt_mod_tone_pair(
            mod_candidate=mod_candidate,
            tone_candidate=tone_candidate,
            compounds=compounds,
            raw_compounds=raw_compounds,
            known_modifiers=self.known_modifiers,
            known_tones=self.known_tones,
            all_webcolor_names=self.webcolors,
            debug=True
        )
        result = next(iter(compounds)) if compounds else None
        print(f"\n[INPUT] mod_candidate='{mod_candidate}', tone_candidate='{tone_candidate}'")
        print(f"[EXPECTED] {expected_compound}")
        print(f"[ACTUAL]   {result}")
        self.assertEqual(expected_compound, result)

    def test_case_01(self): self.run_case("soft", "pink", "soft pink")
    def test_case_02(self): self.run_case("dusty", "rose", "dust rose")
    def test_case_03(self): self.run_case("muted", "coral", "muted coral")
    def test_case_04(self): self.run_case("light", "blue", "light blue")
    def test_case_05(self): self.run_case("bold", "red", "bold red")
    def test_case_06(self): self.run_case("icy", "lavender", "icy lavender")
    def test_case_07(self): self.run_case("creamy", "ivory", "cream ivory")
    def test_case_08(self): self.run_case("cool", "grey", "cool grey")
    def test_case_09(self): self.run_case("deep", "gray", "deep gray")
    def test_case_10(self): self.run_case("faded", "rose", "faded rose")
    def test_case_11(self): self.run_case("pale", "aqua", "pale aqua")
    def test_case_12(self): self.run_case("burnt", "orange", None)
    def test_case_13(self): self.run_case("natural", "tan", "natural tan")
    def test_case_14(self): self.run_case("subtle", "taupe", "subtle taupe")
    def test_case_15(self): self.run_case("airy", "pink", None)
    def test_case_16(self): self.run_case("rich", "brown", "rich brown")
    def test_case_17(self): self.run_case("warm", "beige", "warm beige")
    def test_case_18(self): self.run_case("bright", "yellow", "bright yellow")
    def test_case_19(self): self.run_case("gentle", "lilac", None)
    def test_case_20(self): self.run_case("moody", "wine", None)
    def test_case_21(self): self.run_case("faint", "blush", "faint blush")
    def test_case_22(self): self.run_case("sheer", "white", "sheer white")
    def test_case_23(self): self.run_case("dim", "olive", None)
    def test_case_24(self): self.run_case("rosy", "gold", "rose gold")
    def test_case_25(self): self.run_case("inky", "black", "ink black")
    def test_case_26(self): self.run_case("dusty", "dusty", None)
    def test_case_27(self): self.run_case("light", "night", None)
    def test_case_28(self): self.run_case("nonexistent", "pink", None)
    def test_case_29(self): self.run_case("romantic", "dramatic", None)
    def test_case_30(self): self.run_case("elegant", "rose", None)
    def test_case_31(self): self.run_case("soft", "nonexistent", None)
    def test_case_32(self): self.run_case("nonexistent", "nonexistent", None)
    def test_case_33(self): self.run_case("rosy", "nude", "rose nude")
    def test_case_34(self): self.run_case("glowing", "sun", None)
    def test_case_35(self): self.run_case("moist", "charcoal", None)
    def test_case_36(self): self.run_case("classic", "red", "classic red")
    def test_case_37(self): self.run_case("dark", "rose", "dark rose")
    def test_case_38(self): self.run_case("neutral", "cream", "neutral cream")
    def test_case_39(self): self.run_case("soft", "ivory", "soft ivory")
    def test_case_40(self): self.run_case("mellow", "beige", None)
    def test_case_41(self): self.run_case("chalky", "white", "chalk white")
    def test_case_42(self): self.run_case("inky", "blue", "ink blue")
    def test_case_43(self): self.run_case("dewy", "rose", "dewy rose")
    def test_case_44(self): self.run_case("sunny", "yellow", None)
    def test_case_45(self): self.run_case("cloudy", "gray", None)
    def test_case_46(self): self.run_case("peachy", "pink", "peach pink")
    def test_case_47(self): self.run_case("soft", "pinkish", "soft pinkish")
    def test_case_48(self): self.run_case("light", "goldish", "light gold")
    def test_case_49(self): self.run_case("clear", "mint", "clear mint")
    def test_case_50(self): self.run_case("puffy", "lavender", None)

if __name__ == "__main__":
    unittest.main()
