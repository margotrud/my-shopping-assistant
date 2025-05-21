from collections import defaultdict
from typing import Dict, List, Set
import unittest



def categorize_color_tokens_with_mapping(
    phrases: List[str],
    known_tones: Set[str],
    known_modifiers: Set[str]
) -> Dict[str, object]:
    """
    Analyzes a list of descriptive color phrases to identify tones and modifiers,
    and builds bidirectional mappings between them.

    Args:
        phrases: List of phrases (e.g., ['soft beige', 'bold red'])
        known_tones: Set of known base tones (e.g., {'beige', 'red'})
        known_modifiers: Set of known modifiers (e.g., {'soft', 'bold'})

    Returns:
        {
            "tones": List[str],
            "modifiers": List[str],
            "modifier_to_tone": Dict[str, List[str]],
            "tone_to_modifier": Dict[str, List[str]]
        }
    """
    tones = set()
    modifiers = set()
    modifier_to_tone = defaultdict(set)
    tone_to_modifier = defaultdict(set)

    for phrase in phrases:
        tokens = phrase.lower().split()
        matched_tones = [tok for tok in tokens if tok in known_tones]
        matched_modifiers = [tok for tok in tokens if tok in known_modifiers]

        tones.update(matched_tones)
        modifiers.update(matched_modifiers)

        for mod in matched_modifiers:
            for tone in matched_tones:
                modifier_to_tone[mod].add(tone)
                tone_to_modifier[tone].add(mod)

    return {
        "tones": sorted(tones),
        "modifiers": sorted(modifiers),
        "modifier_to_tone": {mod: sorted(tones) for mod, tones in modifier_to_tone.items()},
        "tone_to_modifier": {tone: sorted(mods) for tone, mods in tone_to_modifier.items()}
    }

class TestCategorizeColorTokensWithMapping(unittest.TestCase):

    def setUp(self):
        self.known_tones = {"pink", "red", "beige", "coral", "brown", "lavender", "blue", "green", "orange"}
        self.known_modifiers = {"soft", "bold", "warm", "cool", "light", "deep", "bright", "muted", "dark"}

    def test_case_01(self): self.assertEqual({'tones': ['pink'], 'modifiers': ['soft'], 'modifier_to_tone': {'soft': ['pink']}, 'tone_to_modifier': {'pink': ['soft']}}, categorize_color_tokens_with_mapping(["soft pink"], self.known_tones, self.known_modifiers))
    def test_case_02(self): self.assertEqual({'tones': ['red'], 'modifiers': ['bold'], 'modifier_to_tone': {'bold': ['red']}, 'tone_to_modifier': {'red': ['bold']}}, categorize_color_tokens_with_mapping(["bold red"], self.known_tones, self.known_modifiers))
    def test_case_03(self): self.assertEqual({'tones': ['beige'], 'modifiers': ['warm'], 'modifier_to_tone': {'warm': ['beige']}, 'tone_to_modifier': {'beige': ['warm']}}, categorize_color_tokens_with_mapping(["warm beige"], self.known_tones, self.known_modifiers))
    def test_case_04(self): self.assertEqual({'tones': ['coral'], 'modifiers': ['cool'], 'modifier_to_tone': {'cool': ['coral']}, 'tone_to_modifier': {'coral': ['cool']}}, categorize_color_tokens_with_mapping(["cool coral"], self.known_tones, self.known_modifiers))
    def test_case_05(self): self.assertEqual({'tones': ['brown'], 'modifiers': ['deep'], 'modifier_to_tone': {'deep': ['brown']}, 'tone_to_modifier': {'brown': ['deep']}}, categorize_color_tokens_with_mapping(["deep brown"], self.known_tones, self.known_modifiers))
    def test_case_06(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['light'], 'modifier_to_tone': {'light': ['blue']}, 'tone_to_modifier': {'blue': ['light']}}, categorize_color_tokens_with_mapping(["light blue"], self.known_tones, self.known_modifiers))
    def test_case_07(self): self.assertEqual({'tones': ['green'], 'modifiers': ['bright'], 'modifier_to_tone': {'bright': ['green']}, 'tone_to_modifier': {'green': ['bright']}}, categorize_color_tokens_with_mapping(["bright green"], self.known_tones, self.known_modifiers))
    def test_case_08(self): self.assertEqual({'tones': ['lavender'], 'modifiers': ['muted'], 'modifier_to_tone': {'muted': ['lavender']}, 'tone_to_modifier': {'lavender': ['muted']}}, categorize_color_tokens_with_mapping(["muted lavender"], self.known_tones, self.known_modifiers))
    def test_case_09(self): self.assertEqual({'tones': ['orange'], 'modifiers': ['dark'], 'modifier_to_tone': {'dark': ['orange']}, 'tone_to_modifier': {'orange': ['dark']}}, categorize_color_tokens_with_mapping(["dark orange"], self.known_tones, self.known_modifiers))
    def test_case_10(self): self.assertEqual({'tones': ['pink', 'red'], 'modifiers': ['bold', 'soft'], 'modifier_to_tone': {'soft': ['pink'], 'bold': ['red']}, 'tone_to_modifier': {'pink': ['soft'], 'red': ['bold']}}, categorize_color_tokens_with_mapping(["soft pink", "bold red"], self.known_tones, self.known_modifiers))
    def test_case_11(self): self.assertEqual({'tones': [], 'modifiers': [], 'modifier_to_tone': {}, 'tone_to_modifier': {}}, categorize_color_tokens_with_mapping([], self.known_tones, self.known_modifiers))
    def test_case_12(self): self.assertEqual({'tones': [], 'modifiers': [], 'modifier_to_tone': {}, 'tone_to_modifier': {}}, categorize_color_tokens_with_mapping(["undefined tone"], self.known_tones, self.known_modifiers))
    def test_case_13(self): self.assertEqual({'tones': ['pink'], 'modifiers': [], 'modifier_to_tone': {}, 'tone_to_modifier': {}}, categorize_color_tokens_with_mapping(["pink"], self.known_tones, self.known_modifiers))
    def test_case_14(self): self.assertEqual({'tones': [], 'modifiers': ['soft'], 'modifier_to_tone': {}, 'tone_to_modifier': {}}, categorize_color_tokens_with_mapping(["soft"], self.known_tones, self.known_modifiers))
    def test_case_15(self): self.assertEqual({'tones': ['red'], 'modifiers': ['deep'], 'modifier_to_tone': {'deep': ['red']}, 'tone_to_modifier': {'red': ['deep']}}, categorize_color_tokens_with_mapping(["deep red"], self.known_tones, self.known_modifiers))
    def test_case_16(self): self.assertEqual({'tones': ['blue', 'green'], 'modifiers': ['cool'], 'modifier_to_tone': {'cool': ['blue', 'green']}, 'tone_to_modifier': {'blue': ['cool'], 'green': ['cool']}}, categorize_color_tokens_with_mapping(["cool green", "cool blue"], self.known_tones, self.known_modifiers))
    def test_case_17(self): self.assertEqual({'tones': ['orange', 'red'], 'modifiers': ['bold'], 'modifier_to_tone': {'bold': ['orange', 'red']}, 'tone_to_modifier': {'orange': ['bold'], 'red': ['bold']}}, categorize_color_tokens_with_mapping(["bold red", "bold orange"], self.known_tones, self.known_modifiers))
    def test_case_18(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['light', 'soft'], 'modifier_to_tone': {'light': ['blue'], 'soft': ['blue']}, 'tone_to_modifier': {'blue': ['light', 'soft']}}, categorize_color_tokens_with_mapping(["soft blue", "light blue"], self.known_tones, self.known_modifiers))
    def test_case_19(self): self.assertEqual({'tones': ['coral', 'pink'], 'modifiers': ['warm'], 'modifier_to_tone': {'warm': ['coral', 'pink']}, 'tone_to_modifier': {'coral': ['warm'], 'pink': ['warm']}}, categorize_color_tokens_with_mapping(["warm pink", "warm coral"], self.known_tones, self.known_modifiers))
    def test_case_20(self): self.assertEqual({'tones': ['brown', 'green'], 'modifiers': ['muted'], 'modifier_to_tone': {'muted': ['brown', 'green']}, 'tone_to_modifier': {'brown': ['muted'], 'green': ['muted']}}, categorize_color_tokens_with_mapping(["muted brown", "muted green"], self.known_tones, self.known_modifiers))
    def test_case_21(self): self.assertEqual({'tones': ['red'], 'modifiers': ['bright', 'deep'], 'modifier_to_tone': {'bright': ['red'], 'deep': ['red']}, 'tone_to_modifier': {'red': ['bright', 'deep']}}, categorize_color_tokens_with_mapping(["deep red", "bright red"], self.known_tones, self.known_modifiers))
    def test_case_22(self): self.assertEqual({'tones': ['beige', 'coral'], 'modifiers': ['soft', 'warm'], 'modifier_to_tone': {'soft': ['coral'], 'warm': ['beige']}, 'tone_to_modifier': {'coral': ['soft'], 'beige': ['warm']}}, categorize_color_tokens_with_mapping(["warm beige", "soft coral"], self.known_tones, self.known_modifiers))
    def test_case_23(self): self.assertEqual({'tones': ['lavender', 'orange'], 'modifiers': ['dark', 'muted'], 'modifier_to_tone': {'dark': ['orange'], 'muted': ['lavender']}, 'tone_to_modifier': {'lavender': ['muted'], 'orange': ['dark']}}, categorize_color_tokens_with_mapping(["muted lavender", "dark orange"], self.known_tones, self.known_modifiers))
    def test_case_24(self): self.assertEqual({'tones': ['green', 'red'], 'modifiers': ['cool'], 'modifier_to_tone': {'cool': ['green', 'red']}, 'tone_to_modifier': {'green': ['cool'], 'red': ['cool']}}, categorize_color_tokens_with_mapping(["cool red", "cool green"], self.known_tones, self.known_modifiers))
    def test_case_25(self): self.assertEqual({'tones': ['pink'], 'modifiers': ['light', 'soft'], 'modifier_to_tone': {'light': ['pink'], 'soft': ['pink']}, 'tone_to_modifier': {'pink': ['light', 'soft']}}, categorize_color_tokens_with_mapping(["light pink", "soft pink"], self.known_tones, self.known_modifiers))
    def test_case_26(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['bold'], 'modifier_to_tone': {'bold': ['blue']}, 'tone_to_modifier': {'blue': ['bold']}}, categorize_color_tokens_with_mapping(["bold blue"], self.known_tones, self.known_modifiers))
    def test_case_27(self): self.assertEqual({'tones': ['orange'], 'modifiers': ['bright', 'deep'], 'modifier_to_tone': {'bright': ['orange'], 'deep': ['orange']}, 'tone_to_modifier': {'orange': ['bright', 'deep']}}, categorize_color_tokens_with_mapping(["bright orange", "deep orange"], self.known_tones, self.known_modifiers))
    def test_case_28(self): self.assertEqual({'tones': ['green'], 'modifiers': ['dark'], 'modifier_to_tone': {'dark': ['green']}, 'tone_to_modifier': {'green': ['dark']}}, categorize_color_tokens_with_mapping(["dark green"], self.known_tones, self.known_modifiers))
    def test_case_29(self): self.assertEqual({'tones': ['beige'], 'modifiers': ['light'], 'modifier_to_tone': {'light': ['beige']}, 'tone_to_modifier': {'beige': ['light']}}, categorize_color_tokens_with_mapping(["light beige"], self.known_tones, self.known_modifiers))
    def test_case_30(self): self.assertEqual({'tones': ['coral'], 'modifiers': ['bright', 'warm'], 'modifier_to_tone': {'bright': ['coral'], 'warm': ['coral']}, 'tone_to_modifier': {'coral': ['bright', 'warm']}}, categorize_color_tokens_with_mapping(["warm coral", "bright coral"], self.known_tones, self.known_modifiers))
    def test_case_31(self): self.assertEqual({'tones': ['brown'], 'modifiers': ['bold', 'deep'], 'modifier_to_tone': {'bold': ['brown'], 'deep': ['brown']}, 'tone_to_modifier': {'brown': ['bold', 'deep']}}, categorize_color_tokens_with_mapping(["bold brown", "deep brown"], self.known_tones, self.known_modifiers))
    def test_case_32(self): self.assertEqual({'tones': ['lavender'], 'modifiers': ['cool', 'muted'], 'modifier_to_tone': {'cool': ['lavender'], 'muted': ['lavender']}, 'tone_to_modifier': {'lavender': ['cool', 'muted']}}, categorize_color_tokens_with_mapping(["cool lavender", "muted lavender"], self.known_tones, self.known_modifiers))
    def test_case_33(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['cool', 'dark'], 'modifier_to_tone': {'cool': ['blue'], 'dark': ['blue']}, 'tone_to_modifier': {'blue': ['cool', 'dark']}}, categorize_color_tokens_with_mapping(["cool blue", "dark blue"], self.known_tones, self.known_modifiers))
    def test_case_34(self): self.assertEqual({'tones': ['red'], 'modifiers': ['soft'], 'modifier_to_tone': {'soft': ['red']}, 'tone_to_modifier': {'red': ['soft']}}, categorize_color_tokens_with_mapping(["soft red"], self.known_tones, self.known_modifiers))
    def test_case_35(self): self.assertEqual({'tones': ['pink'], 'modifiers': ['muted'], 'modifier_to_tone': {'muted': ['pink']}, 'tone_to_modifier': {'pink': ['muted']}}, categorize_color_tokens_with_mapping(["muted pink"], self.known_tones, self.known_modifiers))
    def test_case_36(self): self.assertEqual({'tones': ['green'], 'modifiers': ['bright', 'light'], 'modifier_to_tone': {'bright': ['green'], 'light': ['green']}, 'tone_to_modifier': {'green': ['bright', 'light']}}, categorize_color_tokens_with_mapping(["bright green", "light green"], self.known_tones, self.known_modifiers))
    def test_case_37(self): self.assertEqual({'tones': ['orange'], 'modifiers': ['cool'], 'modifier_to_tone': {'cool': ['orange']}, 'tone_to_modifier': {'orange': ['cool']}}, categorize_color_tokens_with_mapping(["cool orange"], self.known_tones, self.known_modifiers))
    def test_case_38(self): self.assertEqual({'tones': ['coral'], 'modifiers': ['soft'], 'modifier_to_tone': {'soft': ['coral']}, 'tone_to_modifier': {'coral': ['soft']}}, categorize_color_tokens_with_mapping(["soft coral"], self.known_tones, self.known_modifiers))
    def test_case_39(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['muted'], 'modifier_to_tone': {'muted': ['blue']}, 'tone_to_modifier': {'blue': ['muted']}}, categorize_color_tokens_with_mapping(["muted blue"], self.known_tones, self.known_modifiers))
    def test_case_40(self): self.assertEqual({'tones': ['red'], 'modifiers': ['bold', 'warm'], 'modifier_to_tone': {'bold': ['red'], 'warm': ['red']}, 'tone_to_modifier': {'red': ['bold', 'warm']}}, categorize_color_tokens_with_mapping(["warm red", "bold red"], self.known_tones, self.known_modifiers))
    def test_case_41(self): self.assertEqual({'tones': ['green', 'orange'], 'modifiers': ['dark'], 'modifier_to_tone': {'dark': ['green', 'orange']}, 'tone_to_modifier': {'green': ['dark'], 'orange': ['dark']}}, categorize_color_tokens_with_mapping(["dark green", "dark orange"], self.known_tones, self.known_modifiers))
    def test_case_42(self): self.assertEqual({'tones': ['beige'], 'modifiers': ['light', 'soft'], 'modifier_to_tone': {'light': ['beige'], 'soft': ['beige']}, 'tone_to_modifier': {'beige': ['light', 'soft']}}, categorize_color_tokens_with_mapping(["soft beige", "light beige"], self.known_tones, self.known_modifiers))
    def test_case_43(self): self.assertEqual({'tones': ['brown'], 'modifiers': ['muted'], 'modifier_to_tone': {'muted': ['brown']}, 'tone_to_modifier': {'brown': ['muted']}}, categorize_color_tokens_with_mapping(["muted brown"], self.known_tones, self.known_modifiers))
    def test_case_44(self): self.assertEqual({'tones': ['blue', 'pink'], 'modifiers': ['bold'], 'modifier_to_tone': {'bold': ['blue', 'pink']}, 'tone_to_modifier': {'blue': ['bold'], 'pink': ['bold']}}, categorize_color_tokens_with_mapping(["bold pink", "bold blue"], self.known_tones, self.known_modifiers))
    def test_case_45(self): self.assertEqual({'tones': ['brown', 'red'], 'modifiers': ['dark'], 'modifier_to_tone': {'dark': ['brown', 'red']}, 'tone_to_modifier': {'brown': ['dark'], 'red': ['dark']}}, categorize_color_tokens_with_mapping(["dark red", "dark brown"], self.known_tones, self.known_modifiers))
    def test_case_46(self): self.assertEqual({'tones': ['blue'], 'modifiers': ['deep'], 'modifier_to_tone': {'deep': ['blue']}, 'tone_to_modifier': {'blue': ['deep']}}, categorize_color_tokens_with_mapping(["deep blue"], self.known_tones, self.known_modifiers))
    def test_case_47(self): self.assertEqual({'tones': ['beige', 'orange'], 'modifiers': ['warm'], 'modifier_to_tone': {'warm': ['beige', 'orange']}, 'tone_to_modifier': {'beige': ['warm'], 'orange': ['warm']}}, categorize_color_tokens_with_mapping(["warm orange", "warm beige"], self.known_tones, self.known_modifiers))
    def test_case_48(self): self.assertEqual({'tones': ['coral'], 'modifiers': ['deep'], 'modifier_to_tone': {'deep': ['coral']}, 'tone_to_modifier': {'coral': ['deep']}}, categorize_color_tokens_with_mapping(["deep coral"], self.known_tones, self.known_modifiers))
    def test_case_49(self): self.assertEqual({'tones': ['lavender'], 'modifiers': ['muted', 'soft'], 'modifier_to_tone': {'muted': ['lavender'], 'soft': ['lavender']}, 'tone_to_modifier': {'lavender': ['muted', 'soft']}}, categorize_color_tokens_with_mapping(["soft lavender", "muted lavender"], self.known_tones, self.known_modifiers))
    def test_case_50(self): self.assertEqual({'tones': ['blue', 'pink', 'red'], 'modifiers': ['light'], 'modifier_to_tone': {'light': ['blue', 'pink', 'red']}, 'tone_to_modifier': {'blue': ['light'], 'pink': ['light'], 'red': ['light']}}, categorize_color_tokens_with_mapping(["light pink", "light red", "light blue"], self.known_tones, self.known_modifiers))
