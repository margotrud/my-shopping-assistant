# tests/extractors/general/utils/test_remove_subsumed_matches.py

import unittest
from Chatbot.extractors.general.utils.fuzzy_match import remove_subsumed_matches

class TestRemoveSubsumedMatches(unittest.TestCase):

    def run_case(self, input_list, expected):
        result = remove_subsumed_matches(input_list)
        self.assertEqual(expected, result)

    def test_case_01(self): self.run_case(["glam"], ["glam"])
    def test_case_02(self): self.run_case(["glamorous"], ["glamorous"])
    def test_case_03(self): self.run_case(["glamorous", "glam"], ["glamorous"])
    def test_case_04(self): self.run_case(["soft glam", "glam"], ["soft glam"])
    def test_case_05(self): self.run_case(["glam", "soft glam"], ["soft glam"])
    def test_case_06(self): self.run_case(["bare skin", "skin"], ["bare skin"])
    def test_case_07(self): self.run_case(["romantic", "roma"], ["romantic"])
    def test_case_08(self): self.run_case(["clean skin", "skin", "clean"], ["clean skin"])
    def test_case_09(self): self.run_case(["natural", "natu"], ["natural"])
    def test_case_10(self): self.run_case(["sparkle", "spark"], ["sparkle"])

    def test_case_11(self): self.run_case(["soft", "soft glow"], ["soft glow"])
    def test_case_12(self): self.run_case(["no makeup", "makeup"], ["no makeup"])
    def test_case_13(self): self.run_case(["glow", "subtle glow"], ["subtle glow"])
    def test_case_14(self): self.run_case(["glow", "glow up"], ["glow up"])
    def test_case_15(self): self.run_case(["office look", "look"], ["office look"])
    def test_case_16(self): self.run_case(["bold red", "bold"], ["bold red"])
    def test_case_17(self): self.run_case(["elegant glam", "glam"], ["elegant glam"])
    def test_case_18(self): self.run_case(["date night", "night"], ["date night"])
    def test_case_19(self): self.run_case(["red carpet", "red", "carpet"], ["red carpet"])
    def test_case_20(self): self.run_case(["romantic night", "night", "romantic"], ["romantic night"])

    def test_case_21(self): self.run_case(["barely-there", "bare"], ["barely-there"])
    def test_case_22(self): self.run_case(["chic glam", "glam", "chic"], ["chic glam"])
    def test_case_23(self): self.run_case(["natural", "natural finish"], ["natural finish"])
    def test_case_24(self): self.run_case(["glam", "glam", "glamorous"], ["glamorous"])
    def test_case_25(self): self.run_case(["fresh", "fresh look", "look"], ["fresh look"])
    def test_case_26(self): self.run_case(["glow up", "up"], ["glow up"])
    def test_case_27(self): self.run_case(["spark", "sparkly"], ["sparkly"])
    def test_case_28(self): self.run_case(["bare", "bare skin", "skin"], ["bare skin"])
    def test_case_29(self): self.run_case(["clean", "clean skin", "skin"], ["clean skin"])
    def test_case_30(self): self.run_case(["shine", "shiny", "shine bright"], ["shine bright", "shiny"])

    def test_case_31(self): self.run_case(["red", "red rose", "rose"], ["red rose"])
    def test_case_32(self): self.run_case(["soft", "soft touch", "touch"], ["soft touch"])
    def test_case_33(self): self.run_case(["cream", "creamy", "creamy texture"], ["creamy texture", "cream"])
    def test_case_34(self): self.run_case(["matte", "matte finish", "finish"], ["matte finish"])
    def test_case_35(self): self.run_case(["glow", "glowy", "glowy skin"], ["glowy skin", "glow"])
    def test_case_36(self): self.run_case(["bold", "boldness", "bold vibe"], ["bold vibe", "boldness"])
    def test_case_37(self): self.run_case(["romantic", "romantic vibe", "vibe"], ["romantic vibe"])
    def test_case_38(self): self.run_case(["vibe", "edgy vibe", "edgy"], ["edgy vibe"])
    def test_case_39(self): self.run_case(["no makeup", "makeup", "no"], ["no makeup"])
    def test_case_40(self): self.run_case(["daily", "daily look", "look"], ["daily look"])

    def test_case_41(self): self.run_case(["look", "everyday look", "everyday"], ["everyday look"])
    def test_case_42(self): self.run_case(["work", "work look", "office work"], ["office work", "work look"])
    def test_case_43(self): self.run_case(["bare", "barely-there", "bare skin"], ["barely-there", "bare skin"])
    def test_case_44(self): self.run_case(["fresh", "fresh day", "day", "refresh"], ["fresh day", "refresh"])
    def test_case_45(self): self.run_case(["bold glam", "bold", "glam"], ["bold glam"])
    def test_case_46(self): self.run_case(["subtle", "subtle glam", "glam"], ["subtle glam"])
    def test_case_47(self): self.run_case(["bold sparkle", "bold", "sparkle"], ["bold sparkle"])
    def test_case_48(self): self.run_case(["clean base", "base", "clean"], ["clean base"])
    def test_case_49(self): self.run_case(["soft pink", "pink", "soft"], ["soft pink"])
    def test_case_50(self): self.run_case(["glow", "glow glow glow", "glow glow"], ["glow glow glow"])

if __name__ == "__main__":
    unittest.main()
