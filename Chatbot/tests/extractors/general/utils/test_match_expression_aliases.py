import unittest
import json
from pathlib import Path
from Chatbot.extractors.general.utils.fuzzy_match import match_expression_aliases  # Adjust if needed
from Chatbot.extractors.color.utils.config_loader import load_known_modifiers

class TestMatchExpressionAliases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).resolve().parents[4] / "Data" / "expression_definition.json"
        with open(data_path, "r", encoding="utf-8") as f:
            cls.expression_map = json.load(f)
        cls.known_modifiers = load_known_modifiers()

    def test_case_01(self): self.assertEqual({"soft glam"}, match_expression_aliases("soft glam", self.expression_map))

    def test_case_02(self): self.assertEqual({"soft glam"}, match_expression_aliases("Soft Glam", self.expression_map))

    def test_case_03(self): self.assertEqual({"soft glam"},
                                             match_expression_aliases("I like soft glam", self.expression_map))

    def test_case_04(self): self.assertEqual({"natural", "romantic", "soft glam"},
                                             match_expression_aliases("gentle radiance", self.expression_map))

    def test_case_05(self): self.assertEqual({"soft glam"},
                                             match_expression_aliases("subtle sparkle look", self.expression_map))

    def test_case_06(self): self.assertEqual({"romantic"}, match_expression_aliases("romantic", self.expression_map))

    def test_case_07(self): self.assertEqual({"romantic"},
                                             match_expression_aliases("valentine look", self.expression_map))

    def test_case_08(self): self.assertEqual({"romantic"},
                                             match_expression_aliases("going on a date night", self.expression_map))

    def test_case_09(self): self.assertEqual({"edgy"}, match_expression_aliases("edgy makeup", self.expression_map))

    def test_case_10(self): self.assertEqual({"edgy"}, match_expression_aliases("rock vibe", self.expression_map))

    def test_case_11(self): self.assertEqual({"edgy"}, match_expression_aliases("bold look", self.expression_map))

    def test_case_12(self): self.assertEqual({"natural"}, match_expression_aliases("no makeup", self.expression_map))

    def test_case_13(self): self.assertEqual({"natural"}, match_expression_aliases("bare skin", self.expression_map))

    def test_case_14(self): self.assertEqual({"natural"},
                                             match_expression_aliases("natural finish", self.expression_map))

    def test_case_15(self): self.assertEqual({"glamorous"}, match_expression_aliases("red carpet", self.expression_map))

    def test_case_16(self): self.assertEqual({"glamorous"},
                                             match_expression_aliases("hollywood vibe", self.expression_map))

    def test_case_17(self): self.assertEqual({"glamorous"}, match_expression_aliases("glamorous", self.expression_map))

    def test_case_18(self): self.assertEqual({"soft glam", "natural", "romantic"},
                                             match_expression_aliases("gentle radiance for a romantic date",
                                                                      self.expression_map))

    def test_case_19(self): self.assertEqual({"soft glam"},
                                             match_expression_aliases("soft glam with red carpet", self.expression_map))

    def test_case_20(self): self.assertEqual({"natural", "romantic"},
                                             match_expression_aliases("bare skin valentine", self.expression_map))

    def test_case_21(self): self.assertEqual({"natural", "edgy"},
                                             match_expression_aliases("no makeup but edgy vibe", self.expression_map))

    def test_case_22(self): self.assertEqual({"glamorous", "romantic"},
                                             match_expression_aliases("red carpet valentine glam", self.expression_map))

    def test_case_23(self): self.assertEqual({"natural", "elegant"}, match_expression_aliases("clean soft elegant", self.expression_map))

    def test_case_24(self): self.assertEqual({"soft glam"},
                                             match_expression_aliases("subtle sparkl", self.expression_map))

    def test_case_25(self): self.assertEqual({"romantic"},
                                             match_expression_aliases("romantik mood", self.expression_map))

    def test_case_26(self): self.assertEqual({"edgy"}, match_expression_aliases("bold looook", self.expression_map))

    def test_case_27(self): self.assertEqual({"natural"}, match_expression_aliases("baree skin", self.expression_map))

    def test_case_28(self): self.assertEqual({"glamorous"},
                                             match_expression_aliases("hollywod style", self.expression_map))

    def test_case_29(self): self.assertEqual({"romantic", "glamorous"},
                                             match_expression_aliases("red carpet romance", self.expression_map))

    def test_case_30(self): self.assertEqual({"soft glam", "edgy"},
                                             match_expression_aliases("soft glam bold look", self.expression_map))

    def test_case_31(self): self.assertEqual({"natural", "soft glam"},
                                             match_expression_aliases("no makeup and soft glam", self.expression_map))

    def test_case_32(self): self.assertEqual({"romantic", "natural"},
                                             match_expression_aliases("valentine bare skin", self.expression_map))

    def test_case_33(self): self.assertEqual({"fresh"}, match_expression_aliases("fresh look only", self.expression_map))

    def test_case_34(self): self.assertEqual({"edgy", "glamorous"},
                                             match_expression_aliases("rock vibe hollywood", self.expression_map))

    def test_case_35(self): self.assertEqual({"soft glam"}, match_expression_aliases("softglam", self.expression_map))

    def test_case_36(self): self.assertEqual({"romantic"},
                                             match_expression_aliases("date nite vibes", self.expression_map))

    def test_case_37(self): self.assertEqual({"glamorous"}, match_expression_aliases("glamourous", self.expression_map))

    def test_case_38(self): self.assertEqual({"edgy"}, match_expression_aliases("rockvibe", self.expression_map))

    def test_case_39(self): self.assertEqual({"natural"}, match_expression_aliases("nomakeup", self.expression_map))

    def test_case_40(self): self.assertEqual({"romantic"},
                                             match_expression_aliases("valentine sparkle", self.expression_map))

    def test_case_41(self): self.assertEqual({"glamorous"},
                                             match_expression_aliases("hollywood glam", self.expression_map))

    def test_case_42(self): self.assertEqual({"natural", "edgy"},
                                             match_expression_aliases("bare skin bold look", self.expression_map))

    def test_case_43(self): self.assertEqual({"romantic", "glamorous"},
                                             match_expression_aliases("valentine red carpet", self.expression_map))

    def test_case_44(self): self.assertEqual({"natural"},
                                             match_expression_aliases("bare skin vibe", self.expression_map))

    def test_case_45(self): self.assertEqual({"soft glam", "edgy"},
                                             match_expression_aliases("soft glam rock vibe", self.expression_map))

    def test_case_46(self): self.assertEqual({"natural", "romantic", "glamorous"},
                                             match_expression_aliases("bare skin valentine red carpet",
                                                                      self.expression_map))

    def test_case_47(self): self.assertEqual({"soft glam"},
                                             match_expression_aliases("subtle sparkles", self.expression_map))

    def test_case_48(self): self.assertEqual({"glamorous", "romantic"},
                                             match_expression_aliases("hollywood night", self.expression_map))

    def test_case_49(self): self.assertEqual({"edgy"},
                                             match_expression_aliases("boldness and edge", self.expression_map))

    def test_case_50(self): self.assertEqual({"natural", "glamorous"},
                                             match_expression_aliases("barely there glam and red carpet",
                                                                      self.expression_map))

