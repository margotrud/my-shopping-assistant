# tests/test_build_tone_modifier_mappings.py

import unittest
from Chatbot.extractors.color.logic.color_categorizer import build_tone_modifier_mappings
from Chatbot.extractors.color.shared.vocab import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers
known_modifiers = load_known_modifiers()


class TestBuildToneModifierMappings(unittest.TestCase):

    def run_case(self, phrases, expected_tones, expected_modifiers, expected_mod_to_tone, expected_tone_to_mod):
        tones, modifiers, mod_to_tone, tone_to_mod = build_tone_modifier_mappings(phrases, known_tones, known_modifiers)

        self.assertEqual(expected_tones, tones, f"Expected: {expected_tones}\nActual: {tones}")
        self.assertEqual(expected_modifiers, modifiers, f"Expected: {expected_modifiers}\nActual: {modifiers}")
        self.assertEqual(expected_mod_to_tone, mod_to_tone, f"Expected: {expected_mod_to_tone}\nActual: {mod_to_tone}")
        self.assertEqual(expected_tone_to_mod, tone_to_mod, f"Expected: {expected_tone_to_mod}\nActual: {tone_to_mod}")

    def test_case_01(self): self.run_case(
        ["soft pink"],
        {"pink"}, {"soft"},
        {"soft": {"pink"}},
        {"pink": {"soft"}}
    )

    def test_case_02(self): self.run_case(
        ["bold red"],
        {"red"}, {"bold"},
        {"bold": {"red"}},
        {"red": {"bold"}}
    )

    def test_case_03(self): self.run_case(
        ["soft pink", "bold red"],
        {"pink", "red"}, {"soft", "bold"},
        {"soft": {"pink"}, "bold": {"red"}},
        {"pink": {"soft"}, "red": {"bold"}}
    )

    def test_case_04(self): self.run_case(
        ["muted coral"],
        {"coral"}, {"muted"},
        {"muted": {"coral"}},
        {"coral": {"muted"}}
    )

    def test_case_05(self): self.run_case(
        ["deep nude"],
        {"nude"}, {"deep"},
        {"deep": {"nude"}},
        {"nude": {"deep"}}
    )

    def test_case_06(self): self.run_case(
        ["deep nude", "soft pink"],
        {"nude", "pink"}, {"deep", "soft"},
        {"deep": {"nude"}, "soft": {"pink"}},
        {"nude": {"deep"}, "pink": {"soft"}}
    )

    def test_case_07(self): self.run_case(
        ["faded rose"],
        {"rose"}, {"faded"},
        {"faded": {"rose"}},
        {"rose": {"faded"}}
    )

    def test_case_08(self): self.run_case(
        ["light blue", "cool mint"],
        {"blue", "mint"}, {"light", "cool"},
        {"light": {"blue"}, "cool": {"mint"}},
        {"blue": {"light"}, "mint": {"cool"}}
    )

    def test_case_09(self): self.run_case(
        ["neutral taupe"],
        {"taupe"}, {"neutral"},
        {"neutral": {"taupe"}},
        {"taupe": {"neutral"}}
    )

    def test_case_10(self): self.run_case(
        ["subtle peach"],
        {"peach"}, {"subtle"},
        {"subtle": {"peach"}},
        {"peach": {"subtle"}}
    )

    def test_case_11(self): self.run_case(
        ["intense crimson", "bold crimson"],
        {"crimson"}, {"intense", "bold"},
        {"intense": {"crimson"}, "bold": {"crimson"}},
        {"crimson": {"intense", "bold"}}
    )

    def test_case_12(self): self.run_case(
        ["bright white", "soft white"],
        {"white"}, {"bright", "soft"},
        {"bright": {"white"}, "soft": {"white"}},
        {"white": {"bright", "soft"}}
    )

    def test_case_13(self): self.run_case(
        ["glowy bronze"],
        {"bronze"}, {"glowy"},
        {"glowy": {"bronze"}},
        {"bronze": {"glowy"}}
    )

    def test_case_14(self): self.run_case(
        ["moody charcoal"],
        set(), set(),
        {},
        {}
    )

    def test_case_15(self): self.run_case(
        ["rosy pink", "rosy nude"],
        {"pink", "nude"}, {"rosy"},
        {"rosy": {"pink", "nude"}},
        {"pink": {"rosy"}, "nude": {"rosy"}}
    )

    def test_case_16(self): self.run_case(
        ["cool ash", "warm ash"],
        {"ash"}, {"cool", "warm"},
        {"cool": {"ash"}, "warm": {"ash"}},
        {"ash": {"cool", "warm"}}
    )

    def test_case_17(self): self.run_case(
        ["warm sand", "deep sand", "light sand"],
        {"sand"}, {"warm", "deep", "light"},
        {"warm": {"sand"}, "deep": {"sand"}, "light": {"sand"}},
        {"sand": {"warm", "deep", "light"}}
    )

    def test_case_18(self): self.run_case(
        ["muted beige", "muted rose"],
        {"beige", "rose"}, {"muted"},
        {"muted": {"beige", "rose"}},
        {"beige": {"muted"}, "rose": {"muted"}}
    )

    def test_case_19(self): self.run_case(
        ["dark navy", "deep navy"],
        {"navy"}, {"dark", "deep"},
        {"dark": {"navy"}, "deep": {"navy"}},
        {"navy": {"dark", "deep"}}
    )

    def test_case_20(self): self.run_case(
        ["bright lilac", "soft lilac"],
        {"lilac"}, {"bright", "soft"},
        {"bright": {"lilac"}, "soft": {"lilac"}},
        {"lilac": {"bright", "soft"}}
    )

    def test_case_21(self): self.run_case(
        [],
        set(), set(), {}, {}
    )

    def test_case_22(self): self.run_case(
        ["blue"],
        set(), set(), {}, {}
    )

    def test_case_23(self): self.run_case(
        ["elegant pink"],
        set(), set(), {}, {}
    )

    def test_case_24(self): self.run_case(
        ["soft pink", "pink soft"],
        {"pink"}, {"soft"},
        {"soft": {"pink"}},
        {"pink": {"soft"}}
    )

    def test_case_25(self): self.run_case(
        ["soft"],
        set(), set(), {}, {}
    )

    def test_case_26(self): self.run_case(
        ["bold red", "bold pink", "bold peach"],
        {"red", "pink", "peach"}, {"bold"},
        {"bold": {"red", "pink", "peach"}},
        {"red": {"bold"}, "pink": {"bold"}, "peach": {"bold"}}
    )

    def test_case_27(self): self.run_case(
        ["warm bronze", "cool bronze"],
        {"bronze"}, {"warm", "cool"},
        {"warm": {"bronze"}, "cool": {"bronze"}},
        {"bronze": {"warm", "cool"}}
    )

    def test_case_28(self): self.run_case(
        ["subtle nude", "subtle taupe", "subtle ink"],
        {"nude", "taupe", "ink"}, {"subtle"},
        {"subtle": {"nude", "taupe", "ink"}},
        {"nude": {"subtle"}, "taupe": {"subtle"}, "ink": {"subtle"}}
    )

    def test_case_29(self): self.run_case(
        ["warm pink", "cool pink", "neutral pink"],
        {"pink"}, {"warm", "cool", "neutral"},
        {"warm": {"pink"}, "cool": {"pink"}, "neutral": {"pink"}},
        {"pink": {"warm", "cool", "neutral"}}
    )

    def test_case_30(self): self.run_case(
        ["deep pink", "deep rose", "deep beige"],
        {"pink", "rose", "beige"}, {"deep"},
        {"deep": {"pink", "rose", "beige"}},
        {"pink": {"deep"}, "rose": {"deep"}, "beige": {"deep"}}
    )

    def test_case_31(self): self.run_case(
        ["light coral", "light red", "light nude"],
        {"coral", "red", "nude"}, {"light"},
        {"light": {"coral", "red", "nude"}},
        {"coral": {"light"}, "red": {"light"}, "nude": {"light"}}
    )

    def test_case_32(self): self.run_case(
        ["soft mint", "muted mint"],
        {"mint"}, {"soft", "muted"},
        {"soft": {"mint"}, "muted": {"mint"}},
        {"mint": {"soft", "muted"}}
    )

    def test_case_33(self): self.run_case(
        ["cool charcoal", "moody charcoal"],
        {"charcoal"}, {"cool"},
        {"cool": {"charcoal"}},
        {"charcoal": {"cool"}}
    )

    def test_case_34(self): self.run_case(
        ["rosy coral", "rosy pink", "rosy peach"],
        {"coral", "pink", "peach"}, {"rosy"},
        {"rosy": {"coral", "pink", "peach"}},
        {"coral": {"rosy"}, "pink": {"rosy"}, "peach": {"rosy"}}
    )

    def test_case_35(self): self.run_case(
        ["muted pink", "muted rose", "muted peach"],
        {"pink", "rose", "peach"}, {"muted"},
        {"muted": {"pink", "rose", "peach"}},
        {"pink": {"muted"}, "rose": {"muted"}, "peach": {"muted"}}
    )

    def test_case_36(self): self.run_case(
        ["vibrant red", "vibrant coral"],
        {"red", "coral"}, {"vibrant"},
        {"vibrant": {"red", "coral"}},
        {"red": {"vibrant"}, "coral": {"vibrant"}}
    )

    def test_case_37(self): self.run_case(
        ["dusty mauve"],
        {"mauve"}, {"dusty"},
        {"dusty": {"mauve"}},
        {"mauve": {"dusty"}}
    )

    def test_case_38(self): self.run_case(
        ["faded blush"],
        {"blush"}, {"faded"},
        {"faded": {"blush"}},
        {"blush": {"faded"}}
    )

    def test_case_39(self): self.run_case(
        ["neutral ivory", "neutral bone"],
        {"ivory"}, {"neutral"},
        {"neutral": {"ivory"}},
        {"ivory": {"neutral"}}
    )

    def test_case_40(self): self.run_case(
        ["soft soft", "bold bold"],
        set(), set(), {}, {}
    )

    def test_case_41(self): self.run_case(
        ["vibrant turquoise"],
        {"turquoise"}, {"vibrant"},
        {"vibrant": {"turquoise"}},
        {"turquoise": {"vibrant"}}
    )

    def test_case_42(self): self.run_case(
        ["cool lavender", "soft lavender", "pale lavender"],
        {"lavender"}, {"cool", "soft", "pale"},
        {"cool": {"lavender"}, "soft": {"lavender"}, "pale": {"lavender"}},
        {"lavender": {"cool", "soft", "pale"}}
    )

    def test_case_43(self): self.run_case(
        ["warm cream", "light cream", "muted cream"],
        {"cream"}, {"warm", "light", "muted"},
        {"warm": {"cream"}, "light": {"cream"}, "muted": {"cream"}},
        {"cream": {"warm", "light", "muted"}}
    )

    def test_case_44(self): self.run_case(
        ["deep moss", "dark moss"],
        {"moss"}, {"deep", "dark"},
        {"deep": {"moss"}, "dark": {"moss"}},
        {"moss": {"deep", "dark"}}
    )

    def test_case_45(self): self.run_case(
        ["subtle ruby", "bright ruby"],
        {"ruby"}, {"subtle", "bright"},
        {"subtle": {"ruby"}, "bright": {"ruby"}},
        {"ruby": {"subtle", "bright"}}
    )

    def test_case_46(self): self.run_case(
        ["faded lilac", "faded violet"],
        {"lilac", "violet"}, {"faded"},
        {"faded": {"lilac", "violet"}},
        {"lilac": {"faded"}, "violet": {"faded"}}
    )

    def test_case_47(self): self.run_case(
        ["dusty olive", "moody olive", "neutral olive"],
        {"olive"}, {"neutral", "dusty"},
        {"neutral": {"olive"}, "dusty": {"olive"}},
        {"olive": {"neutral", "dusty"}}
    )

    def test_case_48(self): self.run_case(
        ["intense teal", "bold teal", "vibrant teal"],
        {"teal"}, {"intense", "bold", "vibrant"},
        {"intense": {"teal"}, "bold": {"teal"}, "vibrant": {"teal"}},
        {"teal": {"intense", "bold", "vibrant"}}
    )

    def test_case_49(self): self.run_case(
        ["deep sky", "muted sky", "soft sky", "light sky"],
        {"sky"}, {"deep", "muted", "soft", "light"},
        {"deep": {"sky"}, "muted": {"sky"}, "soft": {"sky"}, "light": {"sky"}},
        {"sky": {"deep", "muted", "soft", "light"}}
    )

    def test_case_50(self): self.run_case(
        ["soft pink", "bold red", "faded rose", "muted coral", "bright lilac", "cool mint", "warm cream", "deep nude"],
        {"pink", "red", "rose", "coral", "lilac", "mint", "cream", "nude"},
        {"soft", "bold", "faded", "muted", "bright", "cool", "warm", "deep"},
        {
            "soft": {"pink"},
            "bold": {"red"},
            "faded": {"rose"},
            "muted": {"coral"},
            "bright": {"lilac"},
            "cool": {"mint"},
            "warm": {"cream"},
            "deep": {"nude"},
        },
        {
            "pink": {"soft"},
            "red": {"bold"},
            "rose": {"faded"},
            "coral": {"muted"},
            "lilac": {"bright"},
            "mint": {"cool"},
            "cream": {"warm"},
            "nude": {"deep"},
        }
    )


if __name__ == "__main__":
    unittest.main()
