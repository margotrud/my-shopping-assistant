import unittest
from unittest.mock import patch
from Chatbot.extractors.color.llm.simplifier import simplify_color_description_with_llm

class TestSimplifyColorDescriptionWithLLM(unittest.TestCase):

    def run_case(self, phrase, mock_return, expected, status=200, api_key="fake-key"):
        with patch("os.getenv", return_value=api_key), \
             patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post:
            mock_post.return_value.status_code = status
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_return}}]
            }
            if status != 200:
                with self.assertRaises(RuntimeError):
                    simplify_color_description_with_llm(phrase)
            elif api_key is None:
                with self.assertRaises(ValueError):
                    simplify_color_description_with_llm(phrase)
            else:
                self.assertEqual(expected, simplify_color_description_with_llm(phrase))

    def test_case_01(self): self.run_case("blushy", "soft pink", ["soft pink"])
    def test_case_02(self): self.run_case("rosy", "light rose", ["light rose"])
    def test_case_03(self): self.run_case("natural taupe", "taupe", ["taupe"])
    def test_case_04(self): self.run_case("icy", "frost white", ["frost white"])
    def test_case_05(self): self.run_case("luxurious", "", [])
    def test_case_06(self): self.run_case("creamy", "milky beige", ["milky beige"])
    def test_case_07(self): self.run_case("ashy", "soft gray", ["soft gray"])
    def test_case_08(self): self.run_case("minty", "cool mint", ["cool mint"])
    def test_case_09(self): self.run_case("beachy", "sand", ["sand"])
    def test_case_10(self): self.run_case("burnt coral", "burnt coral", ["burnt coral"])
    def test_case_11(self): self.run_case("mossy", "moss green", ["moss green"])
    def test_case_12(self): self.run_case("blush", "pink", ["pink"])
    def test_case_13(self): self.run_case("candy", "", [])
    def test_case_14(self): self.run_case("velvety", "", [])
    def test_case_15(self): self.run_case("mochish", "mocha", ["mocha"])
    def test_case_16(self): self.run_case("foggy", "fog white", ["fog white"])
    def test_case_17(self): self.run_case("cooly", "cool blue", ["cool blue"])
    def test_case_18(self): self.run_case("syrupy", "", [])
    def test_case_19(self): self.run_case("bold", "", [])
    def test_case_20(self): self.run_case("glowy", "radiant pink", ["radiant pink"])
    def test_case_21(self): self.run_case("wine", "deep red", ["deep red"])
    def test_case_22(self): self.run_case("dusty", "muted taupe", ["muted taupe"])
    def test_case_23(self): self.run_case("olivey", "olive", ["olive"])
    def test_case_24(self): self.run_case("citrusy", "lemon yellow", ["lemon yellow"])
    def test_case_25(self): self.run_case("vanilla", "soft cream", ["soft cream"])
    def test_case_26(self): self.run_case("bold pink", "hot pink", ["hot pink"])
    def test_case_27(self): self.run_case("greenish", "forest green", ["forest green"])
    def test_case_28(self): self.run_case("golden", "metallic gold", ["metallic gold"])
    def test_case_29(self): self.run_case("shiny", "", [])
    def test_case_30(self): self.run_case("night", "midnight blue", ["midnight blue"])
    def test_case_31(self): self.run_case("cloudy", "sky white", ["sky white"])
    def test_case_32(self): self.run_case("berry", "berry red", ["berry red"])
    def test_case_33(self): self.run_case("charcoal", "charcoal gray", ["charcoal gray"])
    def test_case_34(self): self.run_case("neon", "neon pink", ["neon pink"])
    def test_case_35(self): self.run_case("electric", "electric blue", ["electric blue"])
    def test_case_36(self): self.run_case("pastel", "pastel lavender", ["pastel lavender"])
    def test_case_37(self): self.run_case("honey", "golden honey", ["golden honey"])
    def test_case_38(self): self.run_case("metallic", "", [])
    def test_case_39(self): self.run_case("bold beige", "deep beige", ["deep beige"])
    def test_case_40(self): self.run_case("frosty", "ice white", ["ice white"])
    def test_case_41(self): self.run_case("rich", "", [])
    def test_case_42(self): self.run_case("earthy", "earth brown", ["earth brown"])
    def test_case_43(self): self.run_case("muted", "", [])
    def test_case_44(self): self.run_case("bare", "bare beige", ["bare beige"])
    def test_case_45(self): self.run_case("vivid", "vivid coral", ["vivid coral"])
    def test_case_46(self): self.run_case("light", "", [])
    def test_case_47(self): self.run_case("forbidden", "error", [], status=403)
    def test_case_48(self): self.run_case("transparent", "", [])
    def test_case_49(self): self.run_case("clear", "", [])
    def test_case_50(self): self.run_case("blush", "soft blush", ["soft blush"], api_key=None)

if __name__ == "__main__":
    unittest.main()
