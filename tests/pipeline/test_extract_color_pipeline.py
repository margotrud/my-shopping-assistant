import os
import json
import unittest
import webcolors
from matplotlib.colors import XKCD_COLORS
from unittest.mock import patch

from Chatbot.pipelines.color_extractors import extract_color_pipeline


class TestExtractColorPipeline(unittest.TestCase):
    def setUp(self):
        css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
        xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())
        self.known_tones = css_tones.union(xkcd_tones)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        json_path = os.path.join(project_root, "Data", "known_modifiers.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.known_modifiers = set(json.load(f))

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_01(self, mock_find_similar, mock_rgb_lookup):
        text = "I want a cherry red lipstick"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["red", "crimson"]

        expected = {
            "positive": {"tones": ["red"], "matched_color_names": ["crimson", "red"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_02(self, mock_find_similar, mock_rgb_lookup):
        text = "Show me a cute pink gloss"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["pink"]

        expected = {
            "positive": {"tones": ["pink"], "matched_color_names": ["pink"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.simplify_color_description_with_llm")
    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_03(self, mock_find_similar, mock_rgb_lookup, mock_simplify):
        text = "Looking for a nude base"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["nude"]
        mock_simplify.return_value = ["nude"]

        expected = {
            "positive": {"tones": [], "matched_color_names": ["nude"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_04(self, mock_find_similar, mock_rgb_lookup):
        text = "Do you have something in brown"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["brown"]

        expected = {
            "positive": {"tones": ["brown"], "matched_color_names": ["brown"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.simplify_color_description_with_llm")
    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_05(self, mock_find_similar, mock_rgb_lookup, mock_simplify):
        text = "Beige shades look elegant"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["beige"]
        mock_simplify.return_value = []

        expected = {
            "positive": {"tones": ["beige"], "matched_color_names": ["beige"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

    from Chatbot.scripts.cache import _simplify_cache
    _simplify_cache.pop("peach", None)

    @patch("Chatbot.pipelines.color_extractors.simplify_color_description_with_llm")
    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_06(self, mock_find_similar, mock_rgb_lookup, mock_simplify):
        text = "A peach lipstick would be great"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["peach"]
        mock_simplify.return_value = []

        expected = {
            "positive": {"tones": [], "matched_color_names": ["peach"]},
            "negative": {"tones": [], "matched_color_names": []}
        }

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
