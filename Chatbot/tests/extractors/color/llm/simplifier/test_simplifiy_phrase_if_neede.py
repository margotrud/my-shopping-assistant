import unittest
from unittest.mock import patch
from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed
from Chatbot.cache.llm_cache import ColorLLMCache

class TestSimplifyPhraseIfNeeded(unittest.TestCase):

    def setUp(self):
        self.cache = ColorLLMCache.get_instance()
        self.cache.clear()

    def run_cached(self, phrase, expected, raw_key=None):
        self.cache.store_simplified(raw_key or phrase, expected)
        result = simplify_phrase_if_needed(phrase)
        self.assertEqual(expected, result)

    def run_mocked(self, phrase, expected, mock_return):
        with patch("Chatbot.extractors.color.llm.simplifier.simplify_color_description_with_llm", return_value=mock_return):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(expected, result)
            self.assertEqual(expected, self.cache.get_simplified(phrase))

    def test_case_01(self): self.run_cached("peachy", ["light peach"])
    def test_case_02(self): self.run_mocked("blushy", ["soft pink"], ["soft pink"])
    def test_case_03(self): self.run_mocked("notacolor", ["notacolor"], ["notacolor"])
    def test_case_04(self): self.run_cached("dusty", ["soft beige"], raw_key=" dusty ")
    def test_case_05(self): self.run_cached("rosy", ["light pink"], raw_key="Rosy")
    def test_case_06(self): self.run_mocked("mochish", ["light mocha"], ["light mocha"])
    def test_case_07(self): self.run_mocked("glittery pink", ["glam pink"], ["glam pink"])
    def test_case_08(self): self.run_cached("icy", ["cool white"])
    def test_case_09(self): self.run_mocked("sparkle", ["sparkle"], ["sparkle"])
    def test_case_10(self): self.run_cached("creamy", ["milky beige"])

    def test_case_11(self): self.run_mocked("nudy", ["nude beige"], ["nude beige"])
    def test_case_12(self): self.run_cached("deepish", ["deep plum"])
    def test_case_13(self): self.run_mocked("lavendery", ["soft lavender"], ["soft lavender"])
    def test_case_14(self): self.run_cached("yellowy", ["pale yellow"])
    def test_case_15(self): self.run_mocked("brownish", ["muted brown"], ["muted brown"])
    def test_case_16(self): self.run_mocked("burnt sugar", ["warm caramel"], ["warm caramel"])
    def test_case_17(self): self.run_cached("greenish", ["mint green"])
    def test_case_18(self): self.run_mocked("neony", ["neon pink"], ["neon pink"])
    def test_case_19(self): self.run_cached("ashy", ["soft gray"])
    def test_case_20(self): self.run_mocked("misty", ["mist gray"], ["mist gray"])

    def test_case_21(self): self.run_mocked("cherryish", ["bright red"], ["bright red"])
    def test_case_22(self): self.run_cached("bubblegummy", ["light pink"])
    def test_case_23(self): self.run_mocked("inkish", ["dark navy"], ["dark navy"])
    def test_case_24(self): self.run_cached("olivey", ["muted olive"])
    def test_case_25(self): self.run_mocked("lemony", ["light yellow"], ["light yellow"])
    def test_case_26(self): self.run_cached("mossy", ["earth green"])
    def test_case_27(self): self.run_mocked("coalish", ["charcoal"], ["charcoal"])
    def test_case_28(self): self.run_cached("frosty", ["icy white"])
    def test_case_29(self): self.run_mocked("orangy", ["soft orange"], ["soft orange"])
    def test_case_30(self): self.run_cached("goldeny", ["pale gold"])

    def test_case_31(self): self.run_mocked("reddishy", ["rose red"], ["rose red"])
    def test_case_32(self): self.run_cached("silverish", ["frost silver"])
    def test_case_33(self): self.run_mocked("bronzy", ["warm bronze"], ["warm bronze"])
    def test_case_34(self): self.run_cached("beachy", ["sand beige"])
    def test_case_35(self): self.run_mocked("mauvey", ["dusty mauve"], ["dusty mauve"])
    def test_case_36(self): self.run_cached("taupey", ["gray taupe"])
    def test_case_37(self): self.run_mocked("mintish", ["fresh mint"], ["fresh mint"])
    def test_case_38(self): self.run_cached("grayish", ["soft gray"])
    def test_case_39(self): self.run_mocked("cloudy", ["fog white"], ["fog white"])
    def test_case_40(self): self.run_cached("glowy", ["radiant rose"])

    def test_case_41(self): self.run_mocked("moony", ["cool silver"], ["cool silver"])
    def test_case_42(self): self.run_cached("fairy", ["fair pink"])
    def test_case_43(self): self.run_mocked("berryish", ["berry rose"], ["berry rose"])
    def test_case_44(self): self.run_cached("metallicy", ["chrome silver"])
    def test_case_45(self): self.run_mocked("ashy beige", ["taupe beige"], ["taupe beige"])
    def test_case_46(self): self.run_cached("shiny", ["glass white"])
    def test_case_47(self): self.run_mocked("winey", ["deep burgundy"], ["deep burgundy"])
    def test_case_48(self): self.run_cached("matte", ["soft clay"])
    def test_case_49(self): self.run_mocked("flashy", ["hot pink"], ["hot pink"])
    def test_case_50(self): self.run_cached("powdery", ["powder blue"])

if __name__ == "__main__":
    unittest.main()
