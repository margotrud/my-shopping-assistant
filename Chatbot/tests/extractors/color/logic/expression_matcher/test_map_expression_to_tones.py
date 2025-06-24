# tests/test_map_expressions_to_tones.py

import unittest
from Chatbot.extractors.color.logic.expression_matcher import map_expressions_to_tones
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.color.shared.vocab import known_tones

expression_def = load_json_from_data_dir("expression_definition.json")


def expected_for(*expressions: str) -> dict:
    return {
        expr: [m for m in expression_def[expr]["modifiers"] if m in known_tones]
        for expr in expressions
    }


class TestMapExpressionsToTones(unittest.TestCase):

    def run_case(self, text, expected_result):
        result = map_expressions_to_tones(text, expression_def, known_tones)
        self.assertEqual(expected_result, result, f"Expected: {expected_result}\nActual: {result}")

    def test_case_01(self): self.run_case("I want something romantic", expected_for("romantic"))
    def test_case_02(self): self.run_case("Give me a soft glam vibe", expected_for("soft glam"))
    def test_case_03(self): self.run_case("A bold and dramatic makeup", expected_for("edgy"))
    def test_case_04(self): self.run_case("Make it elegant and neutral", expected_for("elegant", "natural"))
    def test_case_05(self): self.run_case("I'm into a soft glam with nude and rose", expected_for("soft glam"))
    def test_case_06(self): self.run_case("Daytime look with beige and peach", expected_for("daytime"))
    def test_case_07(self): self.run_case("Give me a romantic pinkish tone", expected_for("romantic"))
    def test_case_08(self): self.run_case("edgy but gentle", expected_for("edgy"))
    def test_case_09(self): self.run_case("clean and natural with cream", expected_for("natural"))
    def test_case_10(self): self.run_case("elegant beige", expected_for("elegant"))
    def test_case_11(self): self.run_case("classic taupe and nude", {})
    def test_case_12(self): self.run_case("glamorous red look", expected_for("glamorous"))
    def test_case_13(self): self.run_case("subtle brown makeup", expected_for("natural"))
    def test_case_14(self): self.run_case("strong navy and deep blue", {})
    def test_case_15(self): self.run_case("timeless soft beige", expected_for("elegant"))
    def test_case_16(self): self.run_case("nothing special here", {})
    def test_case_17(self): self.run_case("barely there makeup", expected_for("natural"))
    def test_case_18(self): self.run_case("soft nude natural", expected_for("natural"))
    def test_case_19(self): self.run_case("moody charcoal or muted gray", {})
    def test_case_20(self): self.run_case("vintage rose", {})
    def test_case_21(self): self.run_case("fresh coral", expected_for("fresh"))
    def test_case_22(self): self.run_case("warm peach", expected_for("fresh"))
    def test_case_23(self): self.run_case("cool mint green", {})
    def test_case_24(self): self.run_case("bronzed glam", expected_for("glamorous"))
    def test_case_25(self): self.run_case("deep purple elegance", expected_for("elegant"))
    def test_case_26(self): self.run_case("office look with soft taupe", expected_for("daytime"))
    def test_case_27(self): self.run_case("give me edgy green", expected_for("edgy"))
    def test_case_28(self): self.run_case("red carpet ready", expected_for("glamorous"))
    def test_case_29(self): self.run_case("natural makeup with light beige", expected_for("natural"))
    def test_case_30(self): self.run_case("soft rose and dusty pink", expected_for("romantic", "elegant", "natural"))
    def test_case_31(self): self.run_case("nude shades only", {})
    def test_case_32(self): self.run_case("neutral elegance", expected_for("elegant", "natural"))
    def test_case_33(self): self.run_case("romantic lavender tones", expected_for("romantic"))
    def test_case_34(self): self.run_case("casual everyday pink", expected_for("daytime", "natural"))
    def test_case_35(self): self.run_case("gentle mauve", {})
    def test_case_36(self): self.run_case("cool ash look", {})
    def test_case_37(self): self.run_case("barely any makeup", expected_for("natural"))
    def test_case_38(self): self.run_case("bronze shimmer glow", expected_for("fresh"))
    def test_case_39(self): self.run_case("elegant golden peach", expected_for("elegant"))
    def test_case_40(self): self.run_case("evening blue", expected_for("evening", "glamorous"))
    def test_case_41(self): self.run_case("clean glossy finish", expected_for("natural"))
    def test_case_42(self): self.run_case("warm and timeless", expected_for( "elegant", "fresh"))
    def test_case_43(self): self.run_case("neutral tones only", expected_for("natural"))
    def test_case_44(self): self.run_case("rose and beige are always safe", expected_for("natural"))
    def test_case_45(self): self.run_case("bright coral lips", expected_for("fresh"))
    def test_case_46(self): self.run_case("muted lilac", {})
    def test_case_47(self): self.run_case("dusty rose or glowy bronze", expected_for("romantic"))
    def test_case_48(self): self.run_case("intense red look", expected_for("glamorous"))
    def test_case_49(self): self.run_case("natural with a twist of edgy green", expected_for("natural", "edgy"))
    def test_case_50(self): self.run_case("soft glam and classic taupe", expected_for("soft glam"))


if __name__ == "__main__":
    unittest.main()
