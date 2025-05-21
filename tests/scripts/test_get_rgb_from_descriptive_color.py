import unittest
from unittest.mock import patch
from Chatbot.scripts.RGB import get_rgb_from_descriptive_color_llm_first


class TestGetRGBFromDescriptiveColorLLM(unittest.TestCase):

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_01(self, mock_simplify, mock_query):
        mock_query.return_value = (230, 218, 166)
        mock_simplify.return_value = ["beige"]
        self.assertEqual((230, 218, 166), get_rgb_from_descriptive_color_llm_first("warm taupe"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_02(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["beige"]
        self.assertEqual((230, 218, 166), get_rgb_from_descriptive_color_llm_first("shimmery bronze"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_03(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light green"]
        self.assertEqual((144, 238, 144), get_rgb_from_descriptive_color_llm_first("minty green"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_04(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["peach"]
        self.assertEqual((255, 229, 180), get_rgb_from_descriptive_color_llm_first("peach puff"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_05(self, mock_simplify, mock_query):
        mock_query.return_value = (192, 192, 255)
        mock_simplify.return_value = []
        self.assertEqual((192, 192, 255), get_rgb_from_descriptive_color_llm_first("muted lavender"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_06(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["sky blue"]
        self.assertEqual((135, 206, 235), get_rgb_from_descriptive_color_llm_first("airy blue"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_07(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["ivory"]
        self.assertEqual((255, 255, 240), get_rgb_from_descriptive_color_llm_first("creamy white"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_08(self, mock_simplify, mock_query):
        mock_query.return_value = (100, 149, 237)
        mock_simplify.return_value = []
        self.assertEqual((100, 149, 237), get_rgb_from_descriptive_color_llm_first("bluebell"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_09(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["crimson"]
        self.assertEqual((220, 20, 60), get_rgb_from_descriptive_color_llm_first("intense berry red"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_10(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["salmon"]
        self.assertEqual((250, 128, 114), get_rgb_from_descriptive_color_llm_first("coral salmon tint"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_11(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["black"]
        self.assertEqual((0, 0, 0), get_rgb_from_descriptive_color_llm_first("onyx"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_12(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["white"]
        self.assertEqual((255, 255, 255), get_rgb_from_descriptive_color_llm_first("pure snow"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_13(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["chartreuse"]
        self.assertEqual((127, 255, 0), get_rgb_from_descriptive_color_llm_first("neon lime"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_14(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["plum"]
        self.assertEqual((142, 69, 133), get_rgb_from_descriptive_color_llm_first("deep violet plum"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_15(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["hot pink"]
        self.assertEqual((255, 105, 180), get_rgb_from_descriptive_color_llm_first("bold barbie pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_16(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["lavender"]
        self.assertEqual((230, 230, 250), get_rgb_from_descriptive_color_llm_first("light floral purple"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_17(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light coral"]
        self.assertEqual((240, 128, 128), get_rgb_from_descriptive_color_llm_first("rosy orange"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_18(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["midnight blue"]
        self.assertEqual((25, 25, 112), get_rgb_from_descriptive_color_llm_first("dark twilight navy"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_19(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["gold"]
        self.assertEqual((255, 215, 0), get_rgb_from_descriptive_color_llm_first("rich metallic yellow"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_20(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["slate gray"]
        self.assertEqual((112, 128, 144), get_rgb_from_descriptive_color_llm_first("cool industrial grey"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_21(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["orchid"]
        self.assertEqual((218, 112, 214), get_rgb_from_descriptive_color_llm_first("purple magenta blossom"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_22(self, mock_simplify, mock_query):
        mock_query.return_value = (255, 182, 193)
        mock_simplify.return_value = []
        self.assertEqual((255, 182, 193), get_rgb_from_descriptive_color_llm_first("strawberry milk pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_23(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["pale turquoise"]
        self.assertEqual((175, 238, 238), get_rgb_from_descriptive_color_llm_first("frosty teal"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_24(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light pink"]
        self.assertEqual((255, 182, 193), get_rgb_from_descriptive_color_llm_first("baby blush"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_25(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["firebrick"]
        self.assertEqual((178, 34, 34), get_rgb_from_descriptive_color_llm_first("rusty red"))
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_06(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["sky blue"]
        self.assertEqual((135, 206, 235), get_rgb_from_descriptive_color_llm_first("airy blue"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_07(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["ivory"]
        self.assertEqual((255, 255, 240), get_rgb_from_descriptive_color_llm_first("creamy white"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_08(self, mock_simplify, mock_query):
        mock_query.return_value = (100, 149, 237)
        mock_simplify.return_value = []
        self.assertEqual((100, 149, 237), get_rgb_from_descriptive_color_llm_first("bluebell"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_09(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["crimson"]
        self.assertEqual((220, 20, 60), get_rgb_from_descriptive_color_llm_first("intense berry red"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_10(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["salmon"]
        self.assertEqual((250, 128, 114), get_rgb_from_descriptive_color_llm_first("coral salmon tint"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_11(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["black"]
        self.assertEqual((0, 0, 0), get_rgb_from_descriptive_color_llm_first("onyx"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_12(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["white"]
        self.assertEqual((255, 255, 255), get_rgb_from_descriptive_color_llm_first("pure snow"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_13(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["chartreuse"]
        self.assertEqual((127, 255, 0), get_rgb_from_descriptive_color_llm_first("neon lime"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_14(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["plum"]
        self.assertEqual((142, 69, 133), get_rgb_from_descriptive_color_llm_first("deep violet plum"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_15(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["hot pink"]
        self.assertEqual((255, 105, 180), get_rgb_from_descriptive_color_llm_first("bold barbie pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_16(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["lavender"]
        self.assertEqual((230, 230, 250), get_rgb_from_descriptive_color_llm_first("light floral purple"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_17(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light coral"]
        self.assertEqual((240, 128, 128), get_rgb_from_descriptive_color_llm_first("rosy orange"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_18(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["midnight blue"]
        self.assertEqual((25, 25, 112), get_rgb_from_descriptive_color_llm_first("dark twilight navy"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_19(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["gold"]
        self.assertEqual((255, 215, 0), get_rgb_from_descriptive_color_llm_first("rich metallic yellow"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_20(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["slate gray"]
        self.assertEqual((112, 128, 144), get_rgb_from_descriptive_color_llm_first("cool industrial grey"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_21(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["orchid"]
        self.assertEqual((218, 112, 214), get_rgb_from_descriptive_color_llm_first("purple magenta blossom"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_22(self, mock_simplify, mock_query):
        mock_query.return_value = (255, 182, 193)
        mock_simplify.return_value = []
        self.assertEqual((255, 182, 193), get_rgb_from_descriptive_color_llm_first("strawberry milk pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_23(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["pale turquoise"]
        self.assertEqual((175, 238, 238), get_rgb_from_descriptive_color_llm_first("frosty teal"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_24(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light pink"]
        self.assertEqual((255, 182, 193), get_rgb_from_descriptive_color_llm_first("baby blush"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_25(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["firebrick"]
        self.assertEqual((178, 34, 34), get_rgb_from_descriptive_color_llm_first("rusty red"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_26(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["seashell"]
        self.assertEqual((255, 245, 238), get_rgb_from_descriptive_color_llm_first("pale shell pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_27(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["tomato"]
        self.assertEqual((255, 99, 71), get_rgb_from_descriptive_color_llm_first("sunset tomato red"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_28(self, mock_simplify, mock_query):
        mock_query.return_value = (200, 180, 120)
        mock_simplify.return_value = []
        self.assertEqual((200, 180, 120), get_rgb_from_descriptive_color_llm_first("wheat gold"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_29(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["peru"]
        self.assertEqual((205, 133, 63), get_rgb_from_descriptive_color_llm_first("burnt copper brown"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_30(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["steel blue"]
        self.assertEqual((70, 130, 180), get_rgb_from_descriptive_color_llm_first("cold denim"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_31(self, mock_simplify, mock_query):
        mock_query.return_value = (244, 164, 96)
        mock_simplify.return_value = []
        self.assertEqual((244, 164, 96), get_rgb_from_descriptive_color_llm_first("muted golden sand"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_32(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["rosybrown"]
        self.assertEqual((188, 143, 143), get_rgb_from_descriptive_color_llm_first("rosy brownish tint"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_33(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["powder blue"]
        self.assertEqual((176, 224, 230), get_rgb_from_descriptive_color_llm_first("gentle baby blue"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_34(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["misty rose"]
        self.assertEqual((255, 228, 225), get_rgb_from_descriptive_color_llm_first("barely-there pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_35(self, mock_simplify, mock_query):
        mock_query.return_value = (240, 255, 255)
        mock_simplify.return_value = []
        self.assertEqual((240, 255, 255), get_rgb_from_descriptive_color_llm_first("icy pastel aqua"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_36(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["medium orchid"]
        self.assertEqual((186, 85, 211), get_rgb_from_descriptive_color_llm_first("bold fuchsia"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_37(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["dim gray"]
        self.assertEqual((105, 105, 105), get_rgb_from_descriptive_color_llm_first("stormy grey"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_38(self, mock_simplify, mock_query):
        mock_query.return_value = (128, 128, 0)
        mock_simplify.return_value = []
        self.assertEqual((128, 128, 0), get_rgb_from_descriptive_color_llm_first("olive tone"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_39(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["navajo white"]
        self.assertEqual((255, 222, 173), get_rgb_from_descriptive_color_llm_first("buttery cream"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_40(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["medium violet red"]
        self.assertEqual((199, 21, 133), get_rgb_from_descriptive_color_llm_first("electric magenta"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_41(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["sandy brown"]
        self.assertEqual((244, 164, 96), get_rgb_from_descriptive_color_llm_first("beach bronze"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_42(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["lemon chiffon"]
        self.assertEqual((255, 250, 205), get_rgb_from_descriptive_color_llm_first("pale zesty yellow"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_43(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["indigo"]
        self.assertEqual((75, 0, 130), get_rgb_from_descriptive_color_llm_first("deep galaxy purple"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_44(self, mock_simplify, mock_query):
        mock_query.return_value = (221, 160, 221)
        mock_simplify.return_value = []
        self.assertEqual((221, 160, 221), get_rgb_from_descriptive_color_llm_first("lavender mist"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_45(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["light salmon"]
        self.assertEqual((255, 160, 122), get_rgb_from_descriptive_color_llm_first("apricot blush"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_46(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["khaki"]
        self.assertEqual((240, 230, 140), get_rgb_from_descriptive_color_llm_first("dry golden grass"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_47(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["coral"]
        self.assertEqual((255, 127, 80), get_rgb_from_descriptive_color_llm_first("glowy orange pink"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_48(self, mock_simplify, mock_query):
        mock_query.return_value = (192, 192, 255)
        mock_simplify.return_value = []
        self.assertEqual((192, 192, 255), get_rgb_from_descriptive_color_llm_first("dreamy lilac"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_49(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = []
        self.assertEqual(None, get_rgb_from_descriptive_color_llm_first("unicorn dust gray"))

    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.query_llm_for_rgb")
    @patch("Chatbot.scripts.get_approx_rgb_from_color_name.simplify_color_description_with_llm")
    def test_case_50(self, mock_simplify, mock_query):
        mock_query.return_value = None
        mock_simplify.return_value = ["medium slate blue"]
        self.assertEqual((123, 104, 238), get_rgb_from_descriptive_color_llm_first("vibrant denim blue"))


if __name__ == "__main__":
    unittest.main()
