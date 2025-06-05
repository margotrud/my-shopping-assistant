import unittest
import json
from unittest.mock import patch
from Chatbot.extractors.color.llm.simplifier import simplify_color_description_with_llm

class TestSimplifyColorDescriptionWithLLM(unittest.TestCase):
    def test_case_01(self):
        phrase = 'soft pink'
        mock_response = 'soft pink'
        expected = ['soft pink']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_02(self):
        phrase = 'deep blue'
        mock_response = 'deep blue'
        expected = ['deep blue']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_03(self):
        phrase = 'peachy tone'
        mock_response = 'peach'
        expected = ['peach']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_04(self):
        phrase = 'bold red lips'
        mock_response = 'bold red'
        expected = ['bold red']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_05(self):
        phrase = 'nude matte'
        mock_response = 'nude'
        expected = ['nude']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_06(self):
        phrase = 'aqua shimmer'
        mock_response = 'aqua shimmer'
        expected = ['aqua shimmer']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_07(self):
        phrase = 'rosy glow'
        mock_response = 'rosy glow'
        expected = ['rosy glow']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_08(self):
        phrase = 'mint freshness'
        mock_response = 'mint green'
        expected = ['mint green']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_09(self):
        phrase = 'pale peach'
        mock_response = 'light peach'
        expected = ['light peach']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_10(self):
        phrase = 'no match here'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)


    def test_case_11(self):
        phrase = 'glowy skin'
        mock_response = 'glowy'
        expected = ['glowy']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_12(self):
        phrase = 'dewy peach'
        mock_response = 'dewy peach'
        expected = ['dewy peach']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_13(self):
        phrase = 'shimmery gold'
        mock_response = 'shimmery gold'
        expected = ['shimmery gold']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_14(self):
        phrase = 'light coral'
        mock_response = 'light coral'
        expected = ['light coral']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_15(self):
        phrase = 'barely-there blush'
        mock_response = 'soft pink'
        expected = ['soft pink']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_16(self):
        phrase = 'warm brown'
        mock_response = 'warm brown'
        expected = ['warm brown']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_17(self):
        phrase = 'cool taupe'
        mock_response = 'muted brown'
        expected = ['muted brown']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_18(self):
        phrase = 'neon green'
        mock_response = 'vibrant green'
        expected = ['vibrant green']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_19(self):
        phrase = 'pastel orange'
        mock_response = 'pastel orange'
        expected = ['pastel orange']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_20(self):
        phrase = 'classic red'
        mock_response = 'classic red'
        expected = ['classic red']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)


    def test_case_21(self):
        phrase = 'simple tone'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_22(self):
        phrase = 'deep tone'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_23(self):
        phrase = 'earthy'
        mock_response = 'brown'
        expected = ['brown']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_24(self):
        phrase = 'bright neutral'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_25(self):
        phrase = 'random phrase'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_26(self):
        phrase = 'not a color'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_27(self):
        phrase = 'complex word salad'
        mock_response = 'green'
        expected = ['green']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_28(self):
        phrase = 'complex blend'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_29(self):
        phrase = 'rosy beige'
        mock_response = 'rosy beige'
        expected = ['rosy beige']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_30(self):
        phrase = 'burnt sienna'
        mock_response = "deep red-brown"
        expected = ["deep red-brown"]
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)


    def test_case_31(self):
        phrase = 'vivid purple'
        mock_response = 'bright purple'
        expected = ['bright purple']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_32(self):
        phrase = 'washed blue'
        mock_response = 'faded blue'
        expected = ['faded blue']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_33(self):
        phrase = 'pinky nude'
        mock_response = 'pinky nude'
        expected = ['pinky nude']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_34(self):
        phrase = 'rosé'
        mock_response = 'rose'
        expected = ['rose']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_35(self):
        phrase = 'blushy glow'
        mock_response = 'rosy pink'
        expected = ['rosy pink']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_36(self):
        phrase = 'sunburn tone'
        mock_response = 'red bronze'
        expected = ['red bronze']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_37(self):
        phrase = 'neon yellow'
        mock_response = 'vibrant yellow'
        expected = ['vibrant yellow']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_38(self):
        phrase = 'bright vibe'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_39(self):
        phrase = 'red matte'
        mock_response = 'red'
        expected = ['red']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_40(self):
        phrase = 'gold sparkle'
        mock_response = 'gold'
        expected = ['gold']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_41(self):
        phrase = 'bronze shimmer'
        mock_response = 'bronze'
        expected = ['bronze']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_42(self):
        phrase = 'fuzzy orange'
        mock_response = 'fuzzy orange'
        expected = ['fuzzy orange']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_43(self):
        phrase = 'milky tone'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_44(self):
        phrase = 'faint hue'
        mock_response = ''
        expected = []
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_45(self):
        phrase = 'stormy look'
        mock_response = 'cool gray'
        expected = ['cool gray']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_46(self):
        phrase = 'dull pink'
        mock_response = 'muted pink'
        expected = ['muted pink']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_47(self):
        phrase = 'silvery shine'
        mock_response = 'silver'
        expected = ['silver']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_48(self):
        phrase = 'icy shade'
        mock_response = 'cool light'
        expected = ['cool light']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_49(self):
        phrase = 'sunset blush'
        mock_response = 'peachy pink'
        expected = ['peachy pink']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)

    def test_case_50(self):
        phrase = 'sun-kissed'
        mock_response = 'warm peach-gold'
        expected = ['warm peach-gold']
        with patch("Chatbot.extractors.color.llm.simplifier.requests.post") as mock_post, \
             patch("Chatbot.extractors.color.llm.simplifier.os.getenv", return_value="fake-key"):
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "choices": [{"message": {"content": mock_response}}]
            }
            result = simplify_color_description_with_llm(phrase)
            self.assertEqual(expected, result)
