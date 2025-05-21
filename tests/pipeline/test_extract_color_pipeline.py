import webcolors
from matplotlib.colors import XKCD_COLORS
import unittest
from unittest.mock import patch
from Chatbot.pipelines.color_extractors import extract_color_pipeline
from Chatbot.scripts.cache import clear_caches

class TestExtractColorPipeline(unittest.TestCase):
    def setUp(self):
        # Pull dynamic tone vocabulary from CSS3
        css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
        xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())
        self.known_tones = css_tones.union(xkcd_tones)

        self.known_nouns = {"lipstick", "eyeshadow", "blush"}
        self.known_modifiers = {
            "soft", "bright", "bold", "warm", "cool", "deep", "muted", "light", "dark", "shiny"
        }

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_01(self, mock_find_similar, mock_rgb_lookup):
        text = "I want a cherry red lipstick"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ["red", "crimson"]

        expected = {
            "positive": {
                "tones": ["red"],
                "matched_color_names": ["crimson", "red"]
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_02(self, mock_find_similar, mock_rgb_lookup):
        text = 'Show me a cute pink gloss'
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['pink']

        expected = {
            "positive": {
                "tones": ["pink"],
                "matched_color_names": ['pink']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.simplify_color_description_with_llm")
    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_03(self, mock_find_similar, mock_rgb_lookup, mock_simplify):
        text = 'Looking for a nude base'
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['nude']
        mock_simplify.return_value = ['nude']

        expected = {
            "positive": {
                "tones": ["nude"],
                "matched_color_names": ['nude']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        print(f"[✅ MOCKS CHECK] simplify → {mock_simplify.return_value}")
        print(f"[✅ MOCKS CHECK] rgb_lookup → {mock_rgb_lookup.return_value}")
        print(f"[✅ MOCKS CHECK] find_similar → {mock_find_similar.return_value}")
        print(f"[📚 TONES] → {sorted(self.known_tones)}")
        print(f"[📚 MODIFIERS] → {sorted(self.known_modifiers)}")

        result = extract_color_pipeline(
            text,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_04(self, mock_find_similar, mock_rgb_lookup):
        text = 'Do you have something in brown'
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['brown']

        expected = {
            "positive": {
                "tones": ["brown"],
                "matched_color_names": ['brown']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_05(self, mock_find_similar, mock_rgb_lookup):
        text = 'Beige shades look elegant'
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['beige']

        expected = {
            "positive": {
                "tones": ["beige"],
                "matched_color_names": ['beige']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_06(self, mock_find_similar, mock_rgb_lookup):
        text = 'A peach lipstick would be great'
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['peach']

        expected = {
            "positive": {
                "tones": ["peach"],
                "matched_color_names": ['peach']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_07(self, mock_find_similar, mock_rgb_lookup):
        text = "I'd love a bold red lipstick"
        mock_rgb_lookup.return_value = (200, 30, 50)
        mock_find_similar.return_value = ['red']

        expected = {
            "positive": {
                "tones": ["red"],
                "matched_color_names": ['red']
            },
            "negative": {
                "tones": [],
                "matched_color_names": []
            }
        }

        result = extract_color_pipeline(
            text,
            known_nouns=self.known_nouns,
            known_tones=self.known_tones,
            known_modifiers=self.known_modifiers
        )

        self.assertEqual(expected, result)
if __name__ == "__main__":
    unittest.main()

