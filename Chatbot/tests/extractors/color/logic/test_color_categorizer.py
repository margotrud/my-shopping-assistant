import unittest
from typing import Set, List, Dict, Tuple
from Chatbot.extractors.color.logic.color_categorizer import build_tone_modifier_mappings
from Chatbot.extractors.color import known_tones
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

known_modifiers = load_known_modifiers()

class TestBuildToneModifierMappings(unittest.TestCase):

    def assertMappingsEqual(self,
                             expected_tones: Set[str],
                             expected_modifiers: Set[str],
                             expected_mod_to_tone: Dict[str, Set[str]],
                             expected_tone_to_mod: Dict[str, Set[str]],
                             result: Tuple[Set[str], Set[str], Dict[str, Set[str]], Dict[str, Set[str]]]):

        tones, modifiers, mod_to_tone, tone_to_mod = result
        self.assertEqual(expected_tones, tones)
        self.assertEqual(expected_modifiers, modifiers)
        self.assertEqual(expected_mod_to_tone, mod_to_tone)
        self.assertEqual(expected_tone_to_mod, tone_to_mod)

    def test_case_01(self): self.assertMappingsEqual(
        {"pink"}, {"soft"}, {"soft": {"pink"}}, {"pink": {"soft"}},
        build_tone_modifier_mappings(["soft pink"], known_tones, known_modifiers)
    )

    def test_case_02(self): self.assertMappingsEqual(
        {"blue"}, {"cool"}, {"cool": {"blue"}}, {"blue": {"cool"}},
        build_tone_modifier_mappings(["cool blue"], known_tones, known_modifiers)
    )

    def test_case_03(self): self.assertMappingsEqual(
        {"red"}, {"deep"}, {"deep": {"red"}}, {"red": {"deep"}},
        build_tone_modifier_mappings(["deep red"], known_tones, known_modifiers)
    )

    def test_case_04(self): self.assertMappingsEqual(
        {"peach", "pink"}, {"soft"}, {"soft": {"peach", "pink"}}, {"peach": {"soft"}, "pink": {"soft"}},
        build_tone_modifier_mappings(["soft peach", "soft pink"], known_tones, known_modifiers)
    )

    def test_case_05(self): self.assertMappingsEqual(
        {"lavender", "plum"}, {"deep"}, {"deep": {"lavender", "plum"}}, {"lavender": {"deep"}, "plum": {"deep"}},
        build_tone_modifier_mappings(["deep lavender", "deep plum"], known_tones, known_modifiers)
    )

    def test_case_06(self): self.assertMappingsEqual(
        {"blue", "red"}, {"vibrant", "cool"},
        {"vibrant": {"red"}, "cool": {"blue"}},
        {"red": {"vibrant"}, "blue": {"cool"}},
        build_tone_modifier_mappings(["vibrant red", "cool blue"], known_tones, known_modifiers)
    )

    def test_case_07(self): self.assertMappingsEqual(
        {"yellow"}, {"warm"}, {"warm": {"yellow"}}, {"yellow": {"warm"}},
        build_tone_modifier_mappings(["warm yellow"], known_tones, known_modifiers)
    )

    def test_case_08(self): self.assertMappingsEqual(
        {"green"}, {"neutral"}, {"neutral": {"green"}}, {"green": {"neutral"}},
        build_tone_modifier_mappings(["neutral green"], known_tones, known_modifiers)
    )

    def test_case_09(self): self.assertMappingsEqual(
        {"pink"}, {"barely-there"}, {"barely-there": {"pink"}}, {"pink": {"barely-there"}},
        build_tone_modifier_mappings(["barely-there pink"], known_tones, known_modifiers)
    )

    def test_case_10(self): self.assertMappingsEqual(
        set(), set(), {}, {},
        build_tone_modifier_mappings(["unknown sparkle"], known_tones, known_modifiers)
    )

    def test_case_11(self): self.assertMappingsEqual(
        {"pink", "blue"}, {"soft", "cool"},
        {"soft": {"pink"}, "cool": {"blue"}},
        {"pink": {"soft"}, "blue": {"cool"}},
        build_tone_modifier_mappings(["soft pink", "cool blue"], known_tones, known_modifiers)
    )

    def test_case_12(self): self.assertMappingsEqual(
        {"red", "blue"}, {"bright", "vibrant"},
        {"bright": {"red"}, "vibrant": {"blue"}},
        {"red": {"bright"}, "blue": {"vibrant"}},
        build_tone_modifier_mappings(["bright red", "vibrant blue"], known_tones, known_modifiers)
    )

    def test_case_13(self): self.assertMappingsEqual(
        {"blue", "ocean"}, set(), {}, {},
        build_tone_modifier_mappings(["ocean blue"], known_tones, known_modifiers)
    )

    def test_case_14(self): self.assertMappingsEqual(
        {"pink"}, {"soft"}, {"soft": {"pink"}}, {"pink": {"soft"}},
        build_tone_modifier_mappings(["soft pink", "soft pink"], known_tones, known_modifiers)
    )

    def test_case_15(self): self.assertMappingsEqual(
        {"red"}, {"intense", "deep"}, {"deep": {"red"}, "intense": {"red"}}, {"red": {"deep", "intense"}},
        build_tone_modifier_mappings(["deep red", "intense red"], known_tones, known_modifiers)
    )

    def test_case_16(self): self.assertMappingsEqual(
        {"nude"}, {"warm"}, {"warm": {"nude"}}, {"nude": {"warm"}},
        build_tone_modifier_mappings(["warm nude"], known_tones, known_modifiers)
    )

    def test_case_17(self): self.assertMappingsEqual(
        {"green"}, {"cool"}, {"cool": {"green"}}, {"green": {"cool"}},
        build_tone_modifier_mappings(["cool green", "cool green"], known_tones, known_modifiers)
    )

    def test_case_18(self): self.assertMappingsEqual(
        {"plum"}, {"vibrant"}, {"vibrant": {"plum"}}, {"plum": {"vibrant"}},
        build_tone_modifier_mappings(["vibrant plum"], known_tones, known_modifiers)
    )

    def test_case_19(self): self.assertMappingsEqual(
        {"lavender"}, {"soft"}, {"soft": {"lavender"}}, {"lavender": {"soft"}},
        build_tone_modifier_mappings(["soft lavender"], known_tones, known_modifiers)
    )

    def test_case_20(self): self.assertMappingsEqual(
        {"pink", "plum"}, {"deep", "soft"},
        {"soft": {"pink"}, "deep": {"plum"}},
        {"pink": {"soft"}, "plum": {"deep"}},
        build_tone_modifier_mappings(["soft pink", "deep plum"], known_tones, known_modifiers)
    )

    def test_case_21(self): self.assertMappingsEqual(
        {"pink"}, {"soft"}, {"soft": {"pink"}}, {"pink": {"soft"}},
        build_tone_modifier_mappings(["soft pink"], known_tones, known_modifiers)
    )

    def test_case_22(self): self.assertMappingsEqual(
        {"blue"}, {"cool"}, {"cool": {"blue"}}, {"blue": {"cool"}},
        build_tone_modifier_mappings(["cool blue"], known_tones, known_modifiers)
    )

    def test_case_23(self): self.assertMappingsEqual(
        {"red"}, {"bright"}, {"bright": {"red"}}, {"red": {"bright"}},
        build_tone_modifier_mappings(["bright red"], known_tones, known_modifiers)
    )

    def test_case_24(self): self.assertMappingsEqual(
        {"lavender", "nude"}, {"soft", "warm"},
        {"soft": {"lavender"}, "warm": {"nude"}},
        {"lavender": {"soft"}, "nude": {"warm"}},
        build_tone_modifier_mappings(["soft lavender", "warm nude"], known_tones, known_modifiers)
    )

    def test_case_25(self): self.assertMappingsEqual(
        {"plum"}, {"deep"}, {"deep": {"plum"}}, {"plum": {"deep"}},
        build_tone_modifier_mappings(["deep plum"], known_tones, known_modifiers)
    )

    def test_case_26(self): self.assertMappingsEqual(
        {"yellow"}, {"neutral"}, {"neutral": {"yellow"}}, {"yellow": {"neutral"}},
        build_tone_modifier_mappings(["neutral yellow"], known_tones, known_modifiers)
    )

    def test_case_27(self): self.assertMappingsEqual(
        {"red", "pink"}, {"bright", "soft"},
        {"bright": {"red"}, "soft": {"pink"}},
        {"red": {"bright"}, "pink": {"soft"}},
        build_tone_modifier_mappings(["bright red", "soft pink"], known_tones, known_modifiers)
    )

    def test_case_28(self): self.assertMappingsEqual(
        {"blue", "green"}, {"cool"},
        {"cool": {"blue", "green"}},
        {"blue": {"cool"}, "green": {"cool"}},
        build_tone_modifier_mappings(["cool blue", "cool green"], known_tones, known_modifiers)
    )

    def test_case_29(self): self.assertMappingsEqual(
        {"pink"}, {"barely-there"}, {"barely-there": {"pink"}}, {"pink": {"barely-there"}},
        build_tone_modifier_mappings(["barely-there pink"], known_tones, known_modifiers)
    )

    def test_case_30(self): self.assertMappingsEqual(
        {"red"}, {"vibrant"}, {"vibrant": {"red"}}, {"red": {"vibrant"}},
        build_tone_modifier_mappings(["vibrant red"], known_tones, known_modifiers)
    )

    def test_case_31(self): self.assertMappingsEqual(
        {"green"}, {"deep"}, {"deep": {"green"}}, {"green": {"deep"}},
        build_tone_modifier_mappings(["deep green"], known_tones, known_modifiers)
    )

    def test_case_32(self): self.assertMappingsEqual(
        {"nude"}, {"warm"}, {"warm": {"nude"}}, {"nude": {"warm"}},
        build_tone_modifier_mappings(["warm nude"], known_tones, known_modifiers)
    )

    def test_case_33(self): self.assertMappingsEqual(
        {"pink", "plum"}, {"soft", "deep"},
        {"soft": {"pink"}, "deep": {"plum"}},
        {"pink": {"soft"}, "plum": {"deep"}},
        build_tone_modifier_mappings(["soft pink", "deep plum"], known_tones, known_modifiers)
    )

    def test_case_34(self): self.assertMappingsEqual(
        {"blue"}, {"cool"}, {"cool": {"blue"}}, {"blue": {"cool"}},
        build_tone_modifier_mappings(["cool blue", "cool blue"], known_tones, known_modifiers)
    )

    def test_case_35(self): self.assertMappingsEqual(
        set(), set(), {}, {},
        build_tone_modifier_mappings(["undefined sparkle"], known_tones, known_modifiers)
    )

    def test_case_36(self): self.assertMappingsEqual(
        {"green"}, {"neutral"}, {"neutral": {"green"}}, {"green": {"neutral"}},
        build_tone_modifier_mappings(["neutral green"], known_tones, known_modifiers)
    )

    def test_case_37(self): self.assertMappingsEqual(
        {"yellow", "green"}, {"warm", "deep"},
        {"warm": {"yellow"}, "deep": {"green"}},
        {"yellow": {"warm"}, "green": {"deep"}},
        build_tone_modifier_mappings(["warm yellow", "deep green"], known_tones, known_modifiers)
    )

    def test_case_38(self): self.assertMappingsEqual(
        {"blue", "red", "pink"}, {"bright"},
        {"bright": {"blue", "red", "pink"}},
        {"blue": {"bright"}, "red": {"bright"}, "pink": {"bright"}},
        build_tone_modifier_mappings(["bright blue", "bright red", "bright pink"], known_tones, known_modifiers)
    )

    def test_case_39(self): self.assertMappingsEqual(
        {"peach"}, {"cool"}, {"cool": {"peach"}}, {"peach": {"cool"}},
        build_tone_modifier_mappings(["cool peach"], known_tones, known_modifiers)
    )

    def test_case_40(self): self.assertMappingsEqual(
        {"pink", "nude"}, {"soft", "neutral"},
        {"soft": {"pink"}, "neutral": {"nude"}},
        {"pink": {"soft"}, "nude": {"neutral"}},
        build_tone_modifier_mappings(["soft pink", "neutral nude"], known_tones, known_modifiers)
    )

    def test_case_41(self): self.assertMappingsEqual(
        {"red"}, {"bright"}, {"bright": {"red"}}, {"red": {"bright"}},
        build_tone_modifier_mappings(["bright red"], known_tones, known_modifiers)
    )

    def test_case_42(self): self.assertMappingsEqual(
        {"plum"}, {"warm"}, {"warm": {"plum"}}, {"plum": {"warm"}},
        build_tone_modifier_mappings(["warm plum"], known_tones, known_modifiers)
    )

    def test_case_43(self): self.assertMappingsEqual(
        {"lavender"}, {"soft"}, {"soft": {"lavender"}}, {"lavender": {"soft"}},
        build_tone_modifier_mappings(["soft lavender"], known_tones, known_modifiers)
    )

    def test_case_44(self): self.assertMappingsEqual(
        {"green"}, {"cool"}, {"cool": {"green"}}, {"green": {"cool"}},
        build_tone_modifier_mappings(["cool green"], known_tones, known_modifiers)
    )

    def test_case_45(self): self.assertMappingsEqual(
        {"red", "blue"}, {"bright", "vibrant"},
        {"bright": {"red"}, "vibrant": {"blue"}},
        {"red": {"bright"}, "blue": {"vibrant"}},
        build_tone_modifier_mappings(["bright red", "vibrant blue"], known_tones, known_modifiers)
    )

    def test_case_46(self): self.assertMappingsEqual(
        {"yellow", "green", "plum"}, {"warm", "cool"},
        {"warm": {"yellow"}, "cool": {"green", "plum"}},
        {"yellow": {"warm"}, "green": {"cool"}, "plum": {"cool"}},
        build_tone_modifier_mappings(["warm yellow", "cool green", "cool plum"], known_tones, known_modifiers)
    )

    def test_case_47(self): self.assertMappingsEqual(
        {"peach"}, {"barely-there"}, {"barely-there": {"peach"}}, {"peach": {"barely-there"}},
        build_tone_modifier_mappings(["barely-there peach"], known_tones, known_modifiers)
    )

    def test_case_48(self): self.assertMappingsEqual(
        {"blue", "green"}, {"deep"},
        {"deep": {"blue", "green"}}, {"blue": {"deep"}, "green": {"deep"}},
        build_tone_modifier_mappings(["deep blue", "deep green"], known_tones, known_modifiers)
    )

    def test_case_49(self): self.assertMappingsEqual(
        {"lavender", "peach", "red"}, {"soft", "cool", "bright"},
        {"soft": {"lavender"}, "cool": {"peach"}, "bright": {"red"}},
        {"lavender": {"soft"}, "peach": {"cool"}, "red": {"bright"}},
        build_tone_modifier_mappings(["soft lavender", "cool peach", "bright red"], known_tones, known_modifiers)
    )

    def test_case_50(self): self.assertMappingsEqual(
        {"pink"}, {"soft"}, {"soft": {"pink"}}, {"pink": {"soft"}},
        build_tone_modifier_mappings(["soft pink"], known_tones, known_modifiers)
    )
