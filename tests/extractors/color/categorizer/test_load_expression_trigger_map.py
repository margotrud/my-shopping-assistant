# tests/extractors/color/test_load_expression_trigger_map.py

import unittest
from pathlib import Path
from Chatbot.extractors.color.extract.categorizer import load_expression_trigger_map

class TestLoadExpressionTriggerMap(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[4] / "Data" / "expression_definition.json"
        cls.data = load_expression_trigger_map(path)

    def test_case_01(self): self.assertIn("natural", self.data)
    def test_case_02(self): self.assertIn("bold", self.data)
    def test_case_03(self): self.assertIn("romantic", self.data)
    def test_case_04(self): self.assertIn("fresh", self.data)
    def test_case_05(self): self.assertGreaterEqual(len(self.data), 4)
    def test_case_06(self): self.assertIsInstance(self.data, dict)
    def test_case_07(self): self.assertEqual(type(self.data["bold"]), list)
    def test_case_08(self): self.assertGreater(len(self.data["fresh"]), 0)
    def test_case_09(self): self.assertIn("soft", self.data["natural"])
    def test_case_10(self): self.assertIn("bright", self.data["bold"])
    def test_case_11(self): self.assertIn("natural", self.data["natural"])
    def test_case_12(self): self.assertTrue("rosy" in self.data["romantic"])
    def test_case_13(self): self.assertTrue("dewy" in self.data["fresh"])
    def test_case_14(self): self.assertTrue(isinstance(self.data["bold"], list))
    def test_case_15(self): self.assertNotIn("grungy", self.data.get("romantic", []))
    def test_case_16(self): self.assertFalse("dark" in self.data.get("fresh", []))
    def test_case_17(self): self.assertTrue(all(isinstance(k, str) for k in self.data.keys()))
    def test_case_18(self): self.assertTrue(all(isinstance(v, list) for v in self.data.values()))
    def test_case_19(self): self.assertGreaterEqual(len(self.data["natural"]), 3)
    def test_case_20(self): self.assertTrue("peachy" in self.data["fresh"])

    def test_case_21(self): self.assertTrue("blush" in self.data["romantic"])
    def test_case_22(self): self.assertTrue("vibrant" in self.data["bold"])
    def test_case_23(self): self.assertTrue("warm" in self.data["fresh"])
    def test_case_24(self): self.assertNotIn("romantic", self.data.get("natural", []))
    def test_case_25(self): self.assertNotIn("bold", self.data.get("natural", []))
    def test_case_26(self): self.assertTrue("sparkly" in self.data.get("glamorous", []))
    def test_case_27(self): self.assertIn("grunge", self.data.get("edgy", []))
    def test_case_28(self): self.assertIn("classic", self.data.get("elegant", []))
    def test_case_29(self): self.assertIn("luminous", self.data.get("soft glam", []))
    def test_case_30(self): self.assertIn("bare", self.data.get("no makeup", []))
    def test_case_31(self): self.assertGreaterEqual(len(self.data.get("glamorous", [])), 3)
    def test_case_32(self): self.assertGreaterEqual(len(self.data.get("elegant", [])), 3)

    def test_case_33(self):
        bronzed = [t.replace("-", "").lower() for t in self.data.get("bronzed", [])]
        self.assertIn("sunkissed", bronzed)

    def test_case_34(self): self.assertIn("clean", self.data.get("natural", []))
    def test_case_35(self): self.assertEqual(type(self.data["natural"]), list)
    def test_case_36(self): self.assertTrue("tan" in self.data["bronzed"])
    def test_case_37(self): self.assertTrue("glam" in self.data["glamorous"])
    def test_case_38(self): self.assertNotIn("bold", self.data.get("elegant", []))
    def test_case_39(self): self.assertTrue("minimal" in self.data["no makeup"])
    def test_case_40(self): self.assertIn("dramatic", self.data["glamorous"])
    def test_case_41(self): self.assertIn("peachy", self.data["fresh"])
    def test_case_42(self): self.assertIn("silky", self.data["soft glam"])
    def test_case_43(self): self.assertIn("refined", self.data["elegant"])
    def test_case_44(self): self.assertTrue("experimental" in self.data["edgy"])
    def test_case_45(self): self.assertTrue("cool" not in self.data["romantic"])
    def test_case_46(self): self.assertTrue("rosy" not in self.data.get("bold", []))
    def test_case_47(self): self.assertTrue("edgy" in self.data)
    def test_case_48(self): self.assertTrue("soft glam" in self.data)
    def test_case_49(self): self.assertTrue("no makeup" in self.data)
    def test_case_50(self): self.assertTrue(set(self.data["fresh"]).issubset(set(["fresh", "peachy", "warm", "dewy"] + list(self.data["fresh"]))))

if __name__ == "__main__":
    unittest.main()
