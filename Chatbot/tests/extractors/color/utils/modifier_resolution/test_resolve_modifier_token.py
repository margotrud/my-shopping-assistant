import unittest
from Chatbot.extractors.color.utils.modifier_resolution import resolve_modifier_token
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
from Chatbot.extractors.color.shared.vocab import known_tones

class TestResolveModifierToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.known_modifiers = load_known_modifiers()
        cls.known_tones = known_tones

    def run_case(self, word, expected, allow_fuzzy=True, is_tone=False, debug=False):
        result = resolve_modifier_token(
            word,
            self.known_modifiers,
            self.known_tones,
            allow_fuzzy=allow_fuzzy,
            is_tone=is_tone,
            debug=debug
        )
        self.assertEqual(
            expected,
            result,
            f"Word: '{word}' Expected: {expected} Got: {result}"
        )

    def test_case_01(self): self.run_case("soft", "soft")
    def test_case_02(self): self.run_case("dusty", "dust")
    def test_case_03(self): self.run_case("blurred", "blur")
    def test_case_04(self): self.run_case("red", "red")
    def test_case_05(self): self.run_case("soft", "soft", allow_fuzzy=False)
    def test_case_06(self): self.run_case("unknown", None)
    def test_case_07(self): self.run_case("muted", "muted")
    def test_case_08(self): self.run_case("mutedish", "muted")
    def test_case_09(self): self.run_case("brght", "bright")
    def test_case_10(self): self.run_case("blue", "blue")
    def test_case_11(self): self.run_case("cool", "cool")
    def test_case_12(self): self.run_case("cooly", "cool")
    def test_case_13(self): self.run_case("clr", "clear")
    def test_case_14(self): self.run_case("pink", "pinky")
    def test_case_15(self): self.run_case("pinky", "pinky")
    def test_case_16(self): self.run_case("pnk", None)
    def test_case_17(self): self.run_case("bright", "bright")
    def test_case_18(self): self.run_case("brightish", "bright")
    def test_case_19(self): self.run_case("brght", "bright")
    def test_case_20(self): self.run_case("green", "green")
    def test_case_21(self): self.run_case("glowy", "glow")
    def test_case_22(self): self.run_case("glowyish", "glow")
    def test_case_23(self): self.run_case("glw", "glow")
    def test_case_24(self): self.run_case("orange", "orange")
    def test_case_25(self): self.run_case("matte", "matte")
    def test_case_26(self): self.run_case("matty", "matte")
    def test_case_27(self): self.run_case("matt", "matte")
    def test_case_28(self): self.run_case("yellow", "yellowish")
    def test_case_29(self): self.run_case("velvet", "velvet")
    def test_case_30(self): self.run_case("velvety", "velvet")
    def test_case_31(self): self.run_case("vlvt", None)
    def test_case_32(self): self.run_case("black", "black")
    def test_case_33(self): self.run_case("shiny", "shiny")
    def test_case_34(self): self.run_case("shinny", "shiny")
    def test_case_35(self): self.run_case("shny", "shiny")
    def test_case_36(self): self.run_case("white", "white")
    def test_case_37(self): self.run_case("dust", "dust")
    def test_case_38(self): self.run_case("dusty", "dust")
    def test_case_39(self): self.run_case("dst", None)
    def test_case_40(self): self.run_case("transparent", None, is_tone=False)
    def test_case_41(self): self.run_case("bright", "bright")
    def test_case_42(self): self.run_case("brighty", "bright")
    def test_case_43(self): self.run_case("brt", None)
    def test_case_44(self): self.run_case("tan", "tan", is_tone=False)
    def test_case_45(self): self.run_case("bold", "bold")
    def test_case_46(self): self.run_case("boldy", "bold")
    def test_case_47(self): self.run_case("bld", "blood")
    def test_case_48(self): self.run_case("neutral", "neutral")
    def test_case_49(self): self.run_case("neutraly", "neutral")
    def test_case_50(self): self.run_case("nutrl", "neutral")

if __name__ == "__main__":
    unittest.main()
