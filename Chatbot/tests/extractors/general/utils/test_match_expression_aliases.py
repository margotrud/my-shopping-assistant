# tests/extractors/general/utils/test_match_expression_aliases.py

import unittest
from Chatbot.extractors.color.utils.config_loader import load_json_from_data_dir
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases

class TestMatchExpressionAliases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.expression_def = load_json_from_data_dir("expression_definition.json")

    def run_case(self, input_text, expected_set):
        result = match_expression_aliases(input_text, self.expression_def)
        print(f"Expected: {set(expected_set)} | Actual: {result}")
        self.assertEqual(set(expected_set), result)


    def test_case_01(self): self.run_case("soft glam", ["soft glam"])
    def test_case_02(self): self.run_case("Soft Glam", ["soft glam"])
    def test_case_03(self): self.run_case("I love soft glam", ["soft glam"])
    def test_case_04(self): self.run_case("glam soft", ["soft glam"])
    def test_case_05(self): self.run_case("subtle sparkle", ["soft glam"])
    def test_case_06(self): self.run_case("subtle sparkl", ["soft glam"])
    def test_case_07(self): self.run_case("romantik", ["romantic"])
    def test_case_08(self): self.run_case("romantic", ["romantic"])
    def test_case_09(self): self.run_case("valentine date", ["romantic"])
    def test_case_10(self): self.run_case("valentines", ["romantic"])
    def test_case_11(self): self.run_case("valentine night", ["romantic"])
    def test_case_12(self): self.run_case("red carpet", ["glamorous"])
    def test_case_13(self): self.run_case("redcarpet", ["glamorous"])
    def test_case_14(self): self.run_case("natural", ["soft glam", "natural"])
    def test_case_15(self): self.run_case("no makeup", ["daytime", "natural"])
    def test_case_16(self): self.run_case("bare skin", ["natural"])
    def test_case_17(self): self.run_case("baree skin", ["natural"])
    def test_case_18(self): self.run_case("rock vibe", ["edgy"])
    def test_case_19(self): self.run_case("rockvibe", ["edgy"])
    def test_case_20(self): self.run_case("bold look", ["edgy"])  # assuming overlap
    def test_case_21(self): self.run_case("bold looook", ["edgy"])
    def test_case_22(self): self.run_case("glowy", ['glamorous', 'romantic', 'soft glam', 'evening', 'fresh', 'elegant'])
    def test_case_23(self): self.run_case("clean elegant", ["elegant", "natural"])
    def test_case_24(self): self.run_case("clean and elegant", ["elegant", "natural"])
    def test_case_25(self): self.run_case("clean and classy", ["natural", "elegant"])
    def test_case_26(self): self.run_case("hollywood", ["glamorous"])
    def test_case_27(self): self.run_case("glamourous", ["glamorous"])
    def test_case_28(self): self.run_case("fresh and clean", ["fresh", "natural"])
    def test_case_29(self): self.run_case("fresh clean", ["fresh", "natural"])
    def test_case_30(self): self.run_case("edgy look", ["edgy"])
    def test_case_31(self): self.run_case("edge", ["edgy"])
    def test_case_32(self): self.run_case("bold and edgy", ["edgy"])
    def test_case_33(self): self.run_case("no makeup", ["daytime", "natural"])
    def test_case_34(self): self.run_case("nomakeup", ["natural", "daytime"])
    def test_case_35(self): self.run_case("natural finish", ["natural"])
    def test_case_36(self): self.run_case("softglam", ["soft glam"])
    def test_case_37(self): self.run_case("soft glam glow", ["soft glam"])
    def test_case_38(self): self.run_case("edgy sparkle", ["soft glam", "edgy"])
    def test_case_39(self): self.run_case("barely there", ["natural", "soft glam"])
    def test_case_40(self): self.run_case("glamorous", ["glamorous"])
    def test_case_41(self): self.run_case("elegant", ["elegant"])
    def test_case_42(self): self.run_case("romantic", ["romantic"])
    def test_case_43(self): self.run_case("valentine", ["romantic"])
    def test_case_44(self): self.run_case("bold edge", ["edgy"])
    def test_case_45(self): self.run_case("barely there glam", ["soft glam"])
    def test_case_46(self): self.run_case("minimal makeup", ["natural"])
    def test_case_47(self): self.run_case("minmal", ["natural"])
    def test_case_48(self): self.run_case("vibrnt", ["edgy", "glamorous", "evening"])
    def test_case_49(self): self.run_case("trendii", [])
    def test_case_50(self): self.run_case("fun playful look", [])

if __name__ == "__main__":
    unittest.main()
