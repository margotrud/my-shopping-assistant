import unittest
from unittest.mock import patch
import Chatbot.pipelines.color_extractors as color_extractors

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
        import os
        import json
        import webcolors
        from matplotlib.colors import XKCD_COLORS
        from Chatbot.scripts.cache import clear_caches

        clear_caches()

        # Dynamically load full known_modifiers.json
        script_dir = os.path.dirname(os.path.abspath(__file__))  # test file location
        project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        modifiers_path = os.path.join(project_root, "Data", "known_modifiers.json")
        with open(modifiers_path, "r", encoding="utf-8") as f:
            self.known_modifiers = set(json.load(f))

        # Load known tones from CSS4 and XKCD
        css_tones = set(webcolors.CSS3_NAMES_TO_HEX.keys())
        xkcd_tones = set(name.replace("xkcd:", "") for name in XKCD_COLORS.keys())
        self.known_tones = css_tones.union(xkcd_tones)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_01(self, mock_find_similar, mock_get_rgb):
        text = "I love soft pink shades"
        mock_get_rgb.return_value = (255, 182, 193)
        mock_find_similar.return_value = ["soft pink", "light pink", "pink"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

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

    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_02(self, mock_find_similar, mock_get_rgb):
    #     text = "I don't want anything orange"
    #     mock_get_rgb.return_value = (255, 165, 0)
    #     mock_find_similar.return_value = ["orange", "neon orange"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 165, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["neon orange", "orange"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_03(self, mock_find_similar, mock_get_rgb):
    #     text = "I like cherry red but not bright red"
    #     mock_get_rgb.side_effect = [
    #         (220, 20, 60),  # cherry
    #         (255, 0, 0),  # red
    #         (255, 0, 0)  # bright red — needed for negative block
    #     ]
    #     mock_find_similar.side_effect = [
    #         ["cherry red", "red", "ruby"],
    #         ["red", "bright red"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (220, 20, 60),
    #             "threshold": 60.0,
    #             "matched_color_names": ["cherry red", "ruby"]
    #         },
    #         "negative": {
    #             "base_rgb": (255, 0, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bright red", "red"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_04(self, mock_find_similar, mock_get_rgb):
    #     text = "I like both soft pink and warm beige"
    #     mock_get_rgb.side_effect = [(255, 182, 193), (245, 245, 220)]
    #     mock_find_similar.side_effect = [
    #         ["soft pink", "light pink"],
    #         ["beige", "warm beige"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 182, 193),
    #             "threshold": 60.0,
    #             "matched_color_names": ["beige", "light pink", "soft pink", "warm beige"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_05(self, mock_find_similar, mock_get_rgb):
    #     text = "Please exclude bright red and orange"
    #     mock_get_rgb.side_effect = [(255, 0, 0), (255, 165, 0)]
    #     mock_find_similar.side_effect = [
    #         ["red", "bright red"],
    #         ["orange", "neon orange"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 0, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bright red", "neon orange", "orange", "red"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_06(self, mock_find_similar, mock_get_rgb):
    #     text = "I hate bright coral and flashy pink"
    #     mock_get_rgb.side_effect = [(255, 127, 80), (255, 105, 180)]
    #     mock_find_similar.side_effect = [
    #         ["bright coral", "neon coral"],
    #         ["flashy pink", "hot pink"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 127, 80),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bright coral", "flashy pink", "hot pink", "neon coral"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_07(self, mock_find_similar, mock_get_rgb):
    #     text = "I love nude and beige tones"
    #     mock_get_rgb.side_effect = [(222, 184, 135), (245, 245, 220)]
    #     mock_find_similar.side_effect = [
    #         ["nude", "light beige"],
    #         ["beige", "warm beige"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (222, 184, 135),
    #             "threshold": 60.0,
    #             "matched_color_names": ["beige", "light beige", "nude", "warm beige"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_08(self, mock_find_similar, mock_get_rgb):
    #     text = "I dislike glitter and shimmer"
    #     mock_get_rgb.side_effect = [(200, 200, 255), (255, 250, 250)]
    #     mock_find_similar.side_effect = [
    #         ["glitter", "glitter silver"],
    #         ["shimmer", "shiny pearl"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (200, 200, 255),
    #             "threshold": 60.0,
    #             "matched_color_names": ["glitter", "glitter silver", "shimmer", "shiny pearl"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_09(self, mock_find_similar, mock_get_rgb):
    #     text = "I want something coral, maybe soft peach"
    #     mock_get_rgb.side_effect = [(255, 127, 80), (255, 218, 185)]
    #     mock_find_similar.side_effect = [
    #         ["coral", "bright coral"],
    #         ["soft peach", "light peach"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 127, 80),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bright coral", "coral", "light peach", "soft peach"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_10(self, mock_find_similar, mock_get_rgb):
    #     text = "Avoid neon green or electric blue"
    #     mock_get_rgb.side_effect = [(57, 255, 20), (0, 0, 255)]
    #     mock_find_similar.side_effect = [
    #         ["neon green", "lime"],
    #         ["electric blue", "vivid blue"]
    #     ]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (57, 255, 20),
    #             "threshold": 60.0,
    #             "matched_color_names": ["electric blue", "lime", "neon green", "vivid blue"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_11(self, mock_find_similar, mock_get_rgb):
    #     text = "I like rich gold tones"
    #     mock_get_rgb.return_value = (255, 215, 0)
    #     mock_find_similar.return_value = ["gold", "rich gold"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 215, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["gold", "rich gold"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_12(self, mock_find_similar, mock_get_rgb):
    #     text = "No dark brown or deep burgundy"
    #     mock_get_rgb.side_effect = [(101, 67, 33), (128, 0, 32)]
    #     mock_find_similar.side_effect = [["dark brown"], ["deep burgundy"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (101, 67, 33),
    #             "threshold": 60.0,
    #             "matched_color_names": ["dark brown", "deep burgundy"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_13(self, mock_find_similar, mock_get_rgb):
    #     text = "Maybe something like seafoam green"
    #     mock_get_rgb.return_value = (159, 226, 191)
    #     mock_find_similar.return_value = ["seafoam", "seafoam green", "mint green"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (159, 226, 191),
    #             "threshold": 60.0,
    #             "matched_color_names": ["mint green", "seafoam", "seafoam green"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_14(self, mock_find_similar, mock_get_rgb):
    #     text = "I'd like dusty rose or mauve"
    #     mock_get_rgb.side_effect = [(183, 132, 167), (224, 176, 255)]
    #     mock_find_similar.side_effect = [["dusty rose"], ["mauve", "soft purple"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (183, 132, 167),
    #             "threshold": 60.0,
    #             "matched_color_names": ["dusty rose", "mauve", "soft purple"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_15(self, mock_find_similar, mock_get_rgb):
    #     text = "Definitely not neon yellow"
    #     mock_get_rgb.return_value = (255, 255, 0)
    #     mock_find_similar.return_value = ["yellow", "neon yellow"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 255, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["neon yellow", "yellow"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_16(self, mock_find_similar, mock_get_rgb):
    #     text = "I want both taupe and greige options"
    #     mock_get_rgb.side_effect = [(72, 60, 50), (190, 190, 190)]
    #     mock_find_similar.side_effect = [["taupe"], ["greige"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (72, 60, 50),
    #             "threshold": 60.0,
    #             "matched_color_names": ["greige", "taupe"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_17(self, mock_find_similar, mock_get_rgb):
    #     text = "Avoid anything too bold like crimson"
    #     mock_get_rgb.return_value = (220, 20, 60)
    #     mock_find_similar.return_value = ["crimson", "bold red"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (220, 20, 60),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bold red", "crimson"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_18(self, mock_find_similar, mock_get_rgb):
    #     text = "I love icy blue shades"
    #     mock_get_rgb.return_value = (173, 216, 230)
    #     mock_find_similar.return_value = ["icy blue", "light blue"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (173, 216, 230),
    #             "threshold": 60.0,
    #             "matched_color_names": ["icy blue", "light blue"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_19(self, mock_find_similar, mock_get_rgb):
    #     text = "No to chocolate or mocha"
    #     mock_get_rgb.side_effect = [(123, 63, 0), (111, 78, 55)]
    #     mock_find_similar.side_effect = [["chocolate"], ["mocha"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (123, 63, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["chocolate", "mocha"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_20(self, mock_find_similar, mock_get_rgb):
    #     text = "I'm looking for pearl white or off white"
    #     mock_get_rgb.side_effect = [(255, 253, 250), (245, 245, 245)]
    #     mock_find_similar.side_effect = [["pearl white"], ["off white"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 253, 250),
    #             "threshold": 60.0,
    #             "matched_color_names": ["off white", "pearl white"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_21(self, mock_find_similar, mock_get_rgb):
    #     text = "I want something lavender or periwinkle"
    #     mock_get_rgb.side_effect = [(181, 126, 220), (204, 204, 255)]
    #     mock_find_similar.side_effect = [["lavender"], ["periwinkle"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (181, 126, 220),
    #             "threshold": 60.0,
    #             "matched_color_names": ["lavender", "periwinkle"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_22(self, mock_find_similar, mock_get_rgb):
    #     text = "Please nothing too shiny like gold foil"
    #     mock_get_rgb.return_value = (255, 223, 0)
    #     mock_find_similar.return_value = ["gold", "gold foil"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 223, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["gold", "gold foil"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_23(self, mock_find_similar, mock_get_rgb):
    #     text = "I love pistachio green"
    #     mock_get_rgb.return_value = (147, 197, 114)
    #     mock_find_similar.return_value = ["pistachio", "pistachio green"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (147, 197, 114),
    #             "threshold": 60.0,
    #             "matched_color_names": ["pistachio", "pistachio green"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_24(self, mock_find_similar, mock_get_rgb):
    #     text = "I like either lemon yellow or buttercream"
    #     mock_get_rgb.side_effect = [(255, 250, 205), (255, 255, 224)]
    #     mock_find_similar.side_effect = [["lemon yellow"], ["buttercream"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 250, 205),
    #             "threshold": 60.0,
    #             "matched_color_names": ["buttercream", "lemon yellow"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_25(self, mock_find_similar, mock_get_rgb):
    #     text = "I hate teal and turquoise"
    #     mock_get_rgb.side_effect = [(0, 128, 128), (64, 224, 208)]
    #     mock_find_similar.side_effect = [["teal"], ["turquoise"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (0, 128, 128),
    #             "threshold": 60.0,
    #             "matched_color_names": ["teal", "turquoise"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_26(self, mock_find_similar, mock_get_rgb):
    #     text = "I'm not into anything too sparkly"
    #     mock_get_rgb.return_value = (250, 250, 210)
    #     mock_find_similar.return_value = ["sparkly", "glitter gold"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (250, 250, 210),
    #             "threshold": 60.0,
    #             "matched_color_names": ["glitter gold", "sparkly"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_27(self, mock_find_similar, mock_get_rgb):
    #     text = "I love deep forest green tones"
    #     mock_get_rgb.return_value = (34, 139, 34)
    #     mock_find_similar.return_value = ["forest green", "deep green"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (34, 139, 34),
    #             "threshold": 60.0,
    #             "matched_color_names": ["deep green", "forest green"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_28(self, mock_find_similar, mock_get_rgb):
    #     text = "Not too into gold or metallic finishes"
    #     mock_get_rgb.side_effect = [(255, 215, 0), (192, 192, 192)]
    #     mock_find_similar.side_effect = [["gold"], ["metallic", "silver"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 215, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["gold", "metallic", "silver"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_29(self, mock_find_similar, mock_get_rgb):
    #     text = "I'd love something between coral and tangerine"
    #     mock_get_rgb.side_effect = [(255, 127, 80), (255, 153, 51)]
    #     mock_find_similar.side_effect = [["coral", "light orange"], ["tangerine", "orange"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 127, 80),
    #             "threshold": 60.0,
    #             "matched_color_names": ["coral", "light orange", "orange", "tangerine"]
    #         },
    #         "negative": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_30(self, mock_find_similar, mock_get_rgb):
    #     text = "Stay away from anything like charcoal or ash"
    #     mock_get_rgb.side_effect = [(54, 69, 79), (178, 190, 181)]
    #     mock_find_similar.side_effect = [["charcoal", "graphite"], ["ash", "cool gray"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (54, 69, 79),
    #             "threshold": 60.0,
    #             "matched_color_names": ["ash", "charcoal", "cool gray", "graphite"]
    #         }
    #     }
    #     self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_31(self, mock_find_similar, mock_get_rgb):
        text = "Do you have anything in rosy pink?"
        mock_get_rgb.return_value = (255, 192, 203)
        mock_find_similar.return_value = ["rosy pink", "blush", "warm pink"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 192, 203),
                "threshold": 60.0,
                "matched_color_names": ["blush", "rosy pink", "warm pink"]
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
    def test_case_32(self, mock_find_similar, mock_get_rgb):
        text = "No brown, not even chocolate"
        mock_get_rgb.side_effect = [(139, 69, 19), (123, 63, 0)]
        mock_find_similar.side_effect = [["brown", "mocha"], ["chocolate", "cocoa"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (139, 69, 19),
                "threshold": 60.0,
                "matched_color_names": ["brown", "chocolate", "cocoa", "mocha"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_33(self, mock_find_similar, mock_get_rgb):
        text = "A touch of light lilac would be lovely"
        mock_get_rgb.return_value = (200, 162, 200)
        mock_find_similar.return_value = ["light lilac", "pastel purple", "lavender"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (200, 162, 200),
                "threshold": 60.0,
                "matched_color_names": ["lavender", "light lilac", "pastel purple"]
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
    def test_case_34(self, mock_find_similar, mock_get_rgb):
        text = "Please no bright blue or neon purple"
        mock_get_rgb.side_effect = [(0, 0, 255), (148, 0, 211)]
        mock_find_similar.side_effect = [["bright blue", "electric blue"], ["neon purple", "vivid violet"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (0, 0, 255),
                "threshold": 60.0,
                "matched_color_names": ["bright blue", "electric blue", "neon purple", "vivid violet"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_35(self, mock_find_similar, mock_get_rgb):
        text = "I’m avoiding anything that looks too icy"
        mock_get_rgb.return_value = (224, 255, 255)
        mock_find_similar.return_value = ["icy blue", "frosted mint"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (224, 255, 255),
                "threshold": 60.0,
                "matched_color_names": ["frosted mint", "icy blue"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_36(self, mock_find_similar, mock_get_rgb):
        text = "Can I see something creamy peach or soft apricot?"
        mock_get_rgb.side_effect = [(255, 229, 180), (253, 213, 177)]
        mock_find_similar.side_effect = [["creamy peach"], ["soft apricot", "pastel peach"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 229, 180),
                "threshold": 60.0,
                "matched_color_names": ["creamy peach", "pastel peach", "soft apricot"]
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
    def test_case_37(self, mock_find_similar, mock_get_rgb):
        text = "I'd rather not have anything in vibrant teal"
        mock_get_rgb.return_value = (0, 128, 128)
        mock_find_similar.return_value = ["teal", "vibrant teal"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (0, 128, 128),
                "threshold": 60.0,
                "matched_color_names": ["teal", "vibrant teal"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_38(self, mock_find_similar, mock_get_rgb):
        text = "Could I get something soft bronze?"
        mock_get_rgb.return_value = (205, 127, 50)
        mock_find_similar.return_value = ["bronze", "soft bronze"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (205, 127, 50),
                "threshold": 60.0,
                "matched_color_names": ["bronze", "soft bronze"]
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
    def test_case_39(self, mock_find_similar, mock_get_rgb):
        text = "Please exclude warm taupe or dusty mocha"
        mock_get_rgb.side_effect = [(72, 60, 50), (111, 78, 55)]
        mock_find_similar.side_effect = [["taupe", "warm taupe"], ["mocha", "dusty mocha"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (72, 60, 50),
                "threshold": 60.0,
                "matched_color_names": ["dusty mocha", "mocha", "taupe", "warm taupe"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_40(self, mock_find_similar, mock_get_rgb):
        text = "I want something between rosewood and cranberry"
        mock_get_rgb.side_effect = [(101, 67, 76), (220, 20, 60)]
        mock_find_similar.side_effect = [["rosewood"], ["cranberry", "deep red"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (101, 67, 76),
                "threshold": 60.0,
                "matched_color_names": ["cranberry", "deep red", "rosewood"]
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
    def test_case_41(self, mock_find_similar, mock_get_rgb):
        text = "Not a fan of anything resembling burnt sienna or russet"
        mock_get_rgb.side_effect = [(233, 116, 81), (128, 70, 27)]
        mock_find_similar.side_effect = [["burnt sienna"], ["russet"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (233, 116, 81),
                "threshold": 60.0,
                "matched_color_names": ["burnt sienna", "russet"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_42(self, mock_find_similar, mock_get_rgb):
        text = "I adore peachy tones but dislike anything too orangey"
        mock_get_rgb.side_effect = [(255, 218, 185), (255, 165, 0)]
        mock_find_similar.side_effect = [["peach", "light peach"], ["orange", "orangey"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
        expected = {
            "positive": {
                "base_rgb": (255, 218, 185),
                "threshold": 60.0,
                "matched_color_names": ["light peach", "peach"]
            },
            "negative": {
                "base_rgb": (255, 165, 0),
                "threshold": 60.0,
                "matched_color_names": ["orange", "orangey"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_43(self, mock_find_similar, mock_get_rgb):
        text = "Avoid that icy mint green hue or anything overly pastel"
        mock_get_rgb.side_effect = [(189, 252, 201), (255, 239, 213)]
        mock_find_similar.side_effect = [["icy mint", "mint green"], ["pastel", "pastel peach"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (189, 252, 201),
                "threshold": 60.0,
                "matched_color_names": ["icy mint", "mint green", "pastel", "pastel peach"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_44(self, mock_find_similar, mock_get_rgb):
        text = "I’m okay with bronze but nothing too metallic"
        mock_get_rgb.side_effect = [(205, 127, 50), (192, 192, 192)]
        mock_find_similar.side_effect = [["bronze"], ["metallic silver", "chrome"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
        expected = {
            "positive": {
                "base_rgb": (205, 127, 50),
                "threshold": 60.0,
                "matched_color_names": ["bronze"]
            },
            "negative": {
                "base_rgb": (192, 192, 192),
                "threshold": 60.0,
                "matched_color_names": ["chrome", "metallic silver"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_45(self, mock_find_similar, mock_get_rgb):
        text = "Please no warm beige or anything remotely dusty pink"
        mock_get_rgb.side_effect = [(245, 245, 220), (183, 132, 167)]
        mock_find_similar.side_effect = [["warm beige"], ["dusty pink", "mauve"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (245, 245, 220),
                "threshold": 60.0,
                "matched_color_names": ["dusty pink", "mauve", "warm beige"]
            }
        }
        self.assertEqual(expected, result)

    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_46(self, mock_find_similar, mock_get_rgb):
    #     text = "I want neither olive green nor mustard yellow"
    #     mock_get_rgb.side_effect = [(128, 128, 0), (255, 219, 88)]
    #     mock_find_similar.side_effect = [["olive", "olive green"], ["mustard", "mustard yellow"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (128, 128, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["mustard", "mustard yellow", "olive", "olive green"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_47(self, mock_find_similar, mock_get_rgb):
    #     text = "Everything's okay except for anything neon"
    #     mock_get_rgb.return_value = (255, 20, 147)
    #     mock_find_similar.return_value = ["neon pink", "neon orange", "neon yellow"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 20, 147),
    #             "threshold": 60.0,
    #             "matched_color_names": ["neon orange", "neon pink", "neon yellow"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_48(self, mock_find_similar, mock_get_rgb):
    #     text = "Don't show me anything with gold sparkle or shimmer"
    #     mock_get_rgb.side_effect = [(255, 223, 0), (255, 250, 250)]
    #     mock_find_similar.side_effect = [["gold sparkle"], ["shimmer", "shiny pearl"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 223, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["gold sparkle", "shimmer", "shiny pearl"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_49(self, mock_find_similar, mock_get_rgb):
    #     text = "I'm okay with muted coral, but not with anything that feels too vibrant"
    #     mock_get_rgb.side_effect = [(240, 128, 128), (255, 69, 0)]
    #     mock_find_similar.side_effect = [["muted coral"], ["vibrant red", "hot coral"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (240, 128, 128),
    #             "threshold": 60.0,
    #             "matched_color_names": ["muted coral"]
    #         },
    #         "negative": {
    #             "base_rgb": (255, 69, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["hot coral", "vibrant red"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_50(self, mock_find_similar, mock_get_rgb):
    #     text = "I absolutely don’t want anything that resembles taupe or dusty beige"
    #     mock_get_rgb.side_effect = [(72, 60, 50), (210, 180, 140)]
    #     mock_find_similar.side_effect = [["taupe"], ["dusty beige", "light taupe"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (72, 60, 50),
    #             "threshold": 60.0,
    #             "matched_color_names": ["dusty beige", "light taupe", "taupe"]
    #         }
    #     }
    #     self.assertEqual(expected, result)

    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_51(self, mock_find_similar, mock_get_rgb):
    #     text = "I don’t mind cool brown but please avoid mocha and deep tan"
    #     mock_get_rgb.side_effect = [(101, 67, 33), (111, 78, 55), (210, 180, 140)]
    #     mock_find_similar.side_effect = [["cool brown"], ["mocha"], ["deep tan"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (101, 67, 33),
    #             "threshold": 60.0,
    #             "matched_color_names": ["cool brown"]
    #         },
    #         "negative": {
    #             "base_rgb": (111, 78, 55),
    #             "threshold": 60.0,
    #             "matched_color_names": ["deep tan", "mocha"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_52(self, mock_find_similar, mock_get_rgb):
    #     text = "No to any version of fuchsia, magenta, or punch"
    #     mock_get_rgb.side_effect = [(255, 0, 255), (255, 0, 255), (255, 44, 105)]
    #     mock_find_similar.side_effect = [["fuchsia"], ["magenta"], ["punch", "vibrant pink"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (255, 0, 255),
    #             "threshold": 60.0,
    #             "matched_color_names": ["fuchsia", "magenta", "punch", "vibrant pink"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_53(self, mock_find_similar, mock_get_rgb):
    #     text = "I like cream, but not if it looks too yellow"
    #     mock_get_rgb.side_effect = [(255, 253, 208), (255, 255, 0)]
    #     mock_find_similar.side_effect = [["cream"], ["bright yellow"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 253, 208),
    #             "threshold": 60.0,
    #             "matched_color_names": ["cream"]
    #         },
    #         "negative": {
    #             "base_rgb": (255, 255, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["bright yellow"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_54(self, mock_find_similar, mock_get_rgb):
    #     text = "Soft neutral tones are great, but nothing too stark or chalky"
    #     mock_get_rgb.side_effect = [(230, 224, 210), (255, 255, 255), (250, 250, 240)]
    #     mock_find_similar.side_effect = [["soft neutral"], ["white", "stark"], ["chalk", "chalky"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (230, 224, 210),
    #             "threshold": 60.0,
    #             "matched_color_names": ["soft neutral"]
    #         },
    #         "negative": {
    #             "base_rgb": (255, 255, 255),
    #             "threshold": 60.0,
    #             "matched_color_names": ["chalk", "chalky", "stark", "white"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_55(self, mock_find_similar, mock_get_rgb):
    #     text = "Please nothing between khaki and camel"
    #     mock_get_rgb.return_value = (193, 154, 107)
    #     mock_find_similar.return_value = ["khaki", "camel", "sand"]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (193, 154, 107),
    #             "threshold": 60.0,
    #             "matched_color_names": ["camel", "khaki", "sand"]
    #         }
    #     }
    #     self.assertEqual(expected, result)

    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_56(self, mock_find_similar, mock_get_rgb):
    #     text = "I'm into soft lilac, but not lavender or violet"
    #     mock_get_rgb.side_effect = [(200, 162, 200), (181, 126, 220), (238, 130, 238)]
    #     mock_find_similar.side_effect = [["soft lilac"], ["lavender"], ["violet"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (200, 162, 200),
    #             "threshold": 60.0,
    #             "matched_color_names": ["soft lilac"]
    #         },
    #         "negative": {
    #             "base_rgb": (181, 126, 220),
    #             "threshold": 60.0,
    #             "matched_color_names": ["lavender", "violet"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_57(self, mock_find_similar, mock_get_rgb):
    #     text = "Absolutely no cool-toned red or icy pink"
    #     mock_get_rgb.side_effect = [(170, 0, 0), (255, 192, 203)]
    #     mock_find_similar.side_effect = [["cool red"], ["icy pink"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (170, 0, 0),
    #             "threshold": 60.0,
    #             "matched_color_names": ["cool red", "icy pink"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_58(self, mock_find_similar, mock_get_rgb):
    #     text = "I like creamy vanilla but dislike buttery tones"
    #     mock_get_rgb.side_effect = [(255, 239, 219), (255, 245, 180)]
    #     mock_find_similar.side_effect = [["vanilla", "creamy vanilla"], ["butter", "buttery yellow"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": (255, 239, 219),
    #             "threshold": 60.0,
    #             "matched_color_names": ["creamy vanilla", "vanilla"]
    #         },
    #         "negative": {
    #             "base_rgb": (255, 245, 180),
    #             "threshold": 60.0,
    #             "matched_color_names": ["butter", "buttery yellow"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_59(self, mock_find_similar, mock_get_rgb):
    #     text = "Stay away from anything described as rich plum or deep wine"
    #     mock_get_rgb.side_effect = [(142, 69, 133), (114, 47, 55)]
    #     mock_find_similar.side_effect = [["rich plum", "purple berry"], ["deep wine", "dark red"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (142, 69, 133),
    #             "threshold": 60.0,
    #             "matched_color_names": ["dark red", "deep wine", "purple berry", "rich plum"]
    #         }
    #     }
    #     self.assertEqual(expected, result)
    #
    # @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    # @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    # def test_case_60(self, mock_find_similar, mock_get_rgb):
    #     text = "No to moss green, forest, or earthy khaki shades"
    #     mock_get_rgb.side_effect = [(173, 223, 173), (34, 139, 34), (195, 176, 145)]
    #     mock_find_similar.side_effect = [["moss green"], ["forest green"], ["khaki", "earthy khaki"]]
    #
    #     result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)
    #     expected = {
    #         "positive": {
    #             "base_rgb": None,
    #             "threshold": 60.0,
    #             "matched_color_names": []
    #         },
    #         "negative": {
    #             "base_rgb": (173, 223, 173),
    #             "threshold": 60.0,
    #             "matched_color_names": ["earthy khaki", "forest green", "khaki", "moss green"]
    #         }
    #     }
    #     self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
