import unittest
from unittest.mock import patch
from Chatbot.pipelines.color_extractors import extract_color_pipeline

import logging
import sys

# Setup custom logger for ColorPipeline
logger = logging.getLogger("ColorPipeline")
logger.setLevel(logging.DEBUG)

# Remove existing handlers to avoid duplicates
if logger.hasHandlers():
    logger.handlers.clear()

# Add a stream handler explicitly to stdout
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)



class TestExtractColorPipeline(unittest.TestCase):
    def setUp(self):
        from Chatbot.scripts.cache import clear_caches
        clear_caches()
        self.known_tones = {"red", "pink", "orange", "beige"}
        self.known_modifiers = {"soft", "bright", "warm"}

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_01(self, mock_find_similar, mock_get_rgb):
        text = "I love soft pink shades"
        mock_get_rgb.return_value = (255, 182, 193)
        mock_find_similar.return_value = ["soft pink", "light pink", "pink"]

        result = extract_color_pipeline(text, self.known_tones, self.known_modifiers, rgb_map={})

        expected = {
            "positive": {
                "base_rgb": (255, 182, 193),
                "threshold": 60.0,
                "matched_color_names": ["light pink", "pink", "soft pink"]
            },
            "negative": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_02(self, mock_find_similar, mock_get_rgb):
        text = "I don't want anything orange"
        mock_get_rgb.return_value = (255, 165, 0)
        mock_find_similar.return_value = ["orange", "neon orange"]

        result = extract_color_pipeline(text, self.known_tones, self.known_modifiers, rgb_map={})

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (255, 165, 0),
                "threshold": 60.0,
                "matched_color_names": ["neon orange", "orange"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_03(self, mock_find_similar, mock_get_rgb):
        text = "I like cherry red but not bright red"
        mock_get_rgb.side_effect = [(220, 20, 60), (255, 0, 0)]
        mock_find_similar.side_effect = [
            ["cherry red", "red", "ruby"],
            ["red", "bright red"]
        ]

        result = extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (220, 20, 60),
                "threshold": 60.0,
                "matched_color_names": ["cherry red", "ruby"]
            },
            "negative": {
                "base_rgb": (255, 0, 0),
                "threshold": 60.0,
                "matched_color_names": ["bright red", "red"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_04(self, mock_find_similar, mock_get_rgb):
        text = "I like both soft pink and warm beige"
        mock_get_rgb.side_effect = [(255, 182, 193), (245, 245, 220)]
        mock_find_similar.side_effect = [
            ["soft pink", "light pink"],
            ["beige", "warm beige"]
        ]

        result = extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 182, 193),
                "threshold": 60.0,
                "matched_color_names": ["beige", "light pink", "soft pink", "warm beige"]
            },
            "negative": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_05(self, mock_find_similar, mock_get_rgb):
        text = "Please exclude bright red and orange"
        mock_get_rgb.side_effect = [(255, 0, 0), (255, 165, 0)]
        mock_find_similar.side_effect = [
            ["red", "bright red"],
            ["orange", "neon orange"]
        ]

        result = extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (255, 0, 0),
                "threshold": 60.0,
                "matched_color_names": ["bright red", "neon orange", "orange", "red"]
            }
        }
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
