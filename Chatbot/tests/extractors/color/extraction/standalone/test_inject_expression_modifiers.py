# tests/extractors/color/extraction/test_inject_expression_modifiers.py

import unittest
import spacy
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir, load_known_modifiers
from Chatbot.extractors.color.extraction.standalone import _inject_expression_modifiers
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases
from Chatbot.extractors.color.shared.vocab import known_tones

nlp = spacy.load("en_core_web_sm")

class TestInjectExpressionModifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expression_map = load_json_from_data_dir("expression_definition.json")
        base_mods = load_known_modifiers()
        expr_mods = {
            mod
            for v in cls.expression_map.values()
            for mod in v.get("modifiers", [])
        }
        cls.known_modifiers = base_mods.union(expr_mods)
        cls.known_tones = known_tones

    def full_expr_mods(self, expr):
        return set(self.expression_map.get(expr, {}).get("modifiers", []))

    def reverse_expr_mods(self, modifier):
        matched_exprs = match_expression_aliases(modifier, self.expression_map)
        return set().union(*[self.full_expr_mods(expr) for expr in matched_exprs])

    def run_case(self, text, expected):
        tokens = nlp(text)
        result = _inject_expression_modifiers(
            tokens,
            self.known_modifiers,
            self.known_tones,
            self.expression_map,
            debug=True
        )

        sorted_expected = sorted(expected)
        sorted_result = sorted(result)
        print(f"Expected: {sorted_expected}")
        print(f"Actual  : {sorted_result}")
        self.assertEqual(sorted_expected, sorted_result)

    def test_case_01(self): self.run_case("soft", self.full_expr_mods("soft glam") | {"soft"})
    def test_case_02(self): self.run_case("matte", self.reverse_expr_mods("matte"))
    def test_case_03(self): self.run_case("muted", self.reverse_expr_mods("muted"))
    def test_case_04(self): self.run_case("subtle", self.full_expr_mods("soft glam"))
    def test_case_05(self): self.run_case("warm", self.reverse_expr_mods("warm"))

    def test_case_06(self): self.run_case("romantic", self.full_expr_mods("romantic"))
    def test_case_07(self): self.run_case("night-out", self.full_expr_mods("evening"))
    def test_case_08(self): self.run_case("glamorous", self.full_expr_mods("glamorous"))
    def test_case_09(self): self.run_case("daytime", self.full_expr_mods("daytime"))
    def test_case_10(self): self.run_case("natural", self.full_expr_mods("natural"))

    def test_case_11(self):
        expected = (self.full_expr_mods("romantic")
                    | self.reverse_expr_mods("soft")) - {"medium"}
        self.run_case("romantic soft", expected)
    def test_case_12(self): self.run_case("bold matte", self.reverse_expr_mods("bold") | self.reverse_expr_mods("matte"))
    def test_case_13(self): self.run_case("luminous glamorous", self.full_expr_mods("glamorous") | self.reverse_expr_mods("luminous"))
    def test_case_14(self): self.run_case("pinky", self.reverse_expr_mods("pinky"))
    def test_case_15(self): self.run_case("barely-there natural", self.reverse_expr_mods("barely-there") | self.full_expr_mods("natural"))

    def test_case_16(self): self.run_case("blush", set())
    def test_case_17(self): self.run_case("lipstick", set())
    def test_case_18(self): self.run_case("foundation", set())
    def test_case_19(self): self.run_case("mascara", set())
    def test_case_20(self): self.run_case("concealer", set())

    def test_case_21(self): self.run_case("subtl", self.reverse_expr_mods("subtle"))
    def test_case_22(self): self.run_case("mutd", self.reverse_expr_mods("muted"))
    def test_case_23(self): self.run_case("glowy", self.reverse_expr_mods("glowy"))
    def test_case_24(self): self.run_case("warmy", self.reverse_expr_mods("warm"))
    def test_case_25(self): self.run_case("bareli", self.reverse_expr_mods("barely-there"))

    def test_case_26(self): self.run_case("muted warm matte", self.reverse_expr_mods("muted") | self.reverse_expr_mods("warm") | self.reverse_expr_mods("matte"))
    def test_case_27(self): self.run_case("romantic rosy", self.full_expr_mods("romantic") | self.reverse_expr_mods("rosy"))
    def test_case_28(self): self.run_case("soft and matte", self.reverse_expr_mods("soft") | self.reverse_expr_mods("matte"))
    def test_case_29(self): self.run_case("elegant sheer", self.full_expr_mods("elegant") | self.reverse_expr_mods("sheer"))
    def test_case_30(self): self.run_case("natural minimal", self.full_expr_mods("natural") | self.full_expr_mods("minimal"))

    def test_case_31(self): self.run_case("and or but", set())
    def test_case_32(self): self.run_case("the a an", set())
    def test_case_33(self): self.run_case("is are was", set())
    def test_case_34(self): self.run_case("soft or matte", self.reverse_expr_mods("soft") | self.reverse_expr_mods("matte"))
    def test_case_35(self): self.run_case("muted and radiant", self.reverse_expr_mods("muted") | self.reverse_expr_mods("radiant"))

    def test_case_36(self): self.run_case("sof mutd glam", self.reverse_expr_mods("soft") | self.reverse_expr_mods("muted") | self.full_expr_mods("glamorous"))
    def test_case_37(self): self.run_case("romantic pinkish", self.full_expr_mods("romantic") | self.reverse_expr_mods("pinkish"))
    def test_case_38(self): self.run_case("neutrl subtl lite", self.reverse_expr_mods("neutral") | self.reverse_expr_mods("subtle") | self.reverse_expr_mods("light"))
    def test_case_39(self): self.run_case("warm toned barely natural", self.reverse_expr_mods("warm-toned") | self.reverse_expr_mods("barely-there") | self.full_expr_mods("natural"))
    def test_case_40(self): self.run_case("elegant refined", self.full_expr_mods("elegant") | self.reverse_expr_mods("refined"))

    def test_case_41(self): self.run_case("x", set())
    def test_case_42(self): self.run_case("zzzz", set())
    def test_case_43(self): self.run_case("romantiq", self.reverse_expr_mods("romantic"))
    def test_case_44(self): self.run_case("softish", self.reverse_expr_mods("soft"))
    def test_case_45(self): self.run_case("glamy", self.full_expr_mods("glamorous"))

    def test_case_46(self):
        expected = self.reverse_expr_mods("soft") | self.reverse_expr_mods("romantic") | self.reverse_expr_mods("elegant")
        self.run_case("I want something soft, romantic and elegant", expected)

    def test_case_47(self): self.run_case("bold matte glow", self.reverse_expr_mods("bold") | self.reverse_expr_mods("matte") | self.reverse_expr_mods("glow"))
    def test_case_48(self): self.run_case("natural work-appropriate tone", self.full_expr_mods("natural") | self.full_expr_mods("work-appropriate"))
    def test_case_49(self): self.run_case("daytime pinky shimmer", self.full_expr_mods("daytime") | self.reverse_expr_mods("pinky") | self.reverse_expr_mods("shimmer"))
    def test_case_50(self): self.run_case("rosy flirty minimal glam", self.reverse_expr_mods("rosy") | self.reverse_expr_mods("flirty") | self.full_expr_mods("minimal") | self.full_expr_mods("glamorous"))
