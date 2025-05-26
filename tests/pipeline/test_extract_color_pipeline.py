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

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_02(self, mock_find_similar, mock_get_rgb):
        text = "I don't want anything orange"
        mock_get_rgb.return_value = (255, 165, 0)
        mock_find_similar.return_value = ["orange", "neon orange"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

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
        mock_get_rgb.side_effect = [
            (220, 20, 60),  # cherry
            (255, 0, 0),  # red
            (255, 0, 0)  # bright red — needed for negative block
        ]
        mock_find_similar.side_effect = [
            ["cherry red", "red", "ruby"],
            ["red", "bright red"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

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

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

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

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

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

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_06(self, mock_find_similar, mock_get_rgb):
        text = "I hate bright coral and flashy pink"
        mock_get_rgb.side_effect = [(255, 127, 80), (255, 105, 180)]
        mock_find_similar.side_effect = [
            ["bright coral", "neon coral"],
            ["flashy pink", "hot pink"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (255, 127, 80),
                "threshold": 60.0,
                "matched_color_names": ["bright coral", "flashy pink", "hot pink", "neon coral"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_07(self, mock_find_similar, mock_get_rgb):
        text = "I love nude and beige tones"
        mock_get_rgb.side_effect = [(222, 184, 135), (245, 245, 220)]
        mock_find_similar.side_effect = [
            ["nude", "light beige"],
            ["beige", "warm beige"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (222, 184, 135),
                "threshold": 60.0,
                "matched_color_names": ["beige", "light beige", "nude", "warm beige"]
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
    def test_case_08(self, mock_find_similar, mock_get_rgb):
        text = "I dislike glitter and shimmer"
        mock_get_rgb.side_effect = [(200, 200, 255), (255, 250, 250)]
        mock_find_similar.side_effect = [
            ["glitter", "glitter silver"],
            ["shimmer", "shiny pearl"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (200, 200, 255),
                "threshold": 60.0,
                "matched_color_names": ["glitter", "glitter silver", "shimmer", "shiny pearl"]
            }
        }
        self.assertEqual(expected, result)

    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_09(self, mock_find_similar, mock_get_rgb):
        text = "I want something coral, maybe soft peach"
        mock_get_rgb.side_effect = [(255, 127, 80), (255, 218, 185)]
        mock_find_similar.side_effect = [
            ["coral", "bright coral"],
            ["soft peach", "light peach"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 127, 80),
                "threshold": 60.0,
                "matched_color_names": ["bright coral", "coral", "light peach", "soft peach"]
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
    def test_case_10(self, mock_find_similar, mock_get_rgb):
        text = "Avoid neon green or electric blue"
        mock_get_rgb.side_effect = [(57, 255, 20), (0, 0, 255)]
        mock_find_similar.side_effect = [
            ["neon green", "lime"],
            ["electric blue", "vivid blue"]
        ]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (57, 255, 20),
                "threshold": 60.0,
                "matched_color_names": ["electric blue", "lime", "neon green", "vivid blue"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_11(self, mock_find_similar, mock_get_rgb):
        text = "I like rich gold tones"
        mock_get_rgb.return_value = (255, 215, 0)
        mock_find_similar.return_value = ["gold", "rich gold"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 215, 0),
                "threshold": 60.0,
                "matched_color_names": ["gold", "rich gold"]
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
    def test_case_12(self, mock_find_similar, mock_get_rgb):
        text = "No dark brown or deep burgundy"
        mock_get_rgb.side_effect = [(101, 67, 33), (128, 0, 32)]
        mock_find_similar.side_effect = [["dark brown"], ["deep burgundy"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (101, 67, 33),
                "threshold": 60.0,
                "matched_color_names": ["dark brown", "deep burgundy"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_13(self, mock_find_similar, mock_get_rgb):
        text = "Maybe something like seafoam green"
        mock_get_rgb.return_value = (159, 226, 191)
        mock_find_similar.return_value = ["seafoam", "seafoam green", "mint green"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (159, 226, 191),
                "threshold": 60.0,
                "matched_color_names": ["mint green", "seafoam", "seafoam green"]
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
    def test_case_14(self, mock_find_similar, mock_get_rgb):
        text = "I'd like dusty rose or mauve"
        mock_get_rgb.side_effect = [(183, 132, 167), (224, 176, 255)]
        mock_find_similar.side_effect = [["dusty rose"], ["mauve", "soft purple"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (183, 132, 167),
                "threshold": 60.0,
                "matched_color_names": ["dusty rose", "mauve", "soft purple"]
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
    def test_case_15(self, mock_find_similar, mock_get_rgb):
        text = "Definitely not neon yellow"
        mock_get_rgb.return_value = (255, 255, 0)
        mock_find_similar.return_value = ["yellow", "neon yellow"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (255, 255, 0),
                "threshold": 60.0,
                "matched_color_names": ["neon yellow", "yellow"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_16(self, mock_find_similar, mock_get_rgb):
        text = "I want both taupe and greige options"
        mock_get_rgb.side_effect = [(72, 60, 50), (190, 190, 190)]
        mock_find_similar.side_effect = [["taupe"], ["greige"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (72, 60, 50),
                "threshold": 60.0,
                "matched_color_names": ["greige", "taupe"]
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
    def test_case_17(self, mock_find_similar, mock_get_rgb):
        text = "Avoid anything too bold like crimson"
        mock_get_rgb.return_value = (220, 20, 60)
        mock_find_similar.return_value = ["crimson", "bold red"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (220, 20, 60),
                "threshold": 60.0,
                "matched_color_names": ["bold red", "crimson"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_18(self, mock_find_similar, mock_get_rgb):
        text = "I love icy blue shades"
        mock_get_rgb.return_value = (173, 216, 230)
        mock_find_similar.return_value = ["icy blue", "light blue"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (173, 216, 230),
                "threshold": 60.0,
                "matched_color_names": ["icy blue", "light blue"]
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
    def test_case_19(self, mock_find_similar, mock_get_rgb):
        text = "No to chocolate or mocha"
        mock_get_rgb.side_effect = [(123, 63, 0), (111, 78, 55)]
        mock_find_similar.side_effect = [["chocolate"], ["mocha"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (123, 63, 0),
                "threshold": 60.0,
                "matched_color_names": ["chocolate", "mocha"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_20(self, mock_find_similar, mock_get_rgb):
        text = "I'm looking for pearl white or off white"
        mock_get_rgb.side_effect = [(255, 253, 250), (245, 245, 245)]
        mock_find_similar.side_effect = [["pearl white"], ["off white"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 253, 250),
                "threshold": 60.0,
                "matched_color_names": ["off white", "pearl white"]
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
    def test_case_21(self, mock_find_similar, mock_get_rgb):
        text = "I want something lavender or periwinkle"
        mock_get_rgb.side_effect = [(181, 126, 220), (204, 204, 255)]
        mock_find_similar.side_effect = [["lavender"], ["periwinkle"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (181, 126, 220),
                "threshold": 60.0,
                "matched_color_names": ["lavender", "periwinkle"]
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
    def test_case_22(self, mock_find_similar, mock_get_rgb):
        text = "Please nothing too shiny like gold foil"
        mock_get_rgb.return_value = (255, 223, 0)
        mock_find_similar.return_value = ["gold", "gold foil"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": None,
                "threshold": 60.0,
                "matched_color_names": []
            },
            "negative": {
                "base_rgb": (255, 223, 0),
                "threshold": 60.0,
                "matched_color_names": ["gold", "gold foil"]
            }
        }
        self.assertEqual(expected, result)


    @patch("Chatbot.pipelines.color_extractors.get_rgb_from_descriptive_color_llm_first")
    @patch("Chatbot.pipelines.color_extractors.find_similar_color_names")
    def test_case_23(self, mock_find_similar, mock_get_rgb):
        text = "I love pistachio green"
        mock_get_rgb.return_value = (147, 197, 114)
        mock_find_similar.return_value = ["pistachio", "pistachio green"]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (147, 197, 114),
                "threshold": 60.0,
                "matched_color_names": ["pistachio", "pistachio green"]
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
    def test_case_24(self, mock_find_similar, mock_get_rgb):
        text = "I like either lemon yellow or buttercream"
        mock_get_rgb.side_effect = [(255, 250, 205), (255, 255, 224)]
        mock_find_similar.side_effect = [["lemon yellow"], ["buttercream"]]

        result = color_extractors.extract_color_pipeline(text, self.known_tones, self.known_modifiers)

        expected = {
            "positive": {
                "base_rgb": (255, 250, 205),
                "threshold": 60.0,
                "matched_color_names": ["buttercream", "lemon yellow"]
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
    def test_case_25(self, mock_find_similar, mock_get_rgb):
        text = "I hate teal and turquoise"
        mock_get_rgb.side_effect = [(0, 128, 128), (64, 224, 208)]
        mock_find_similar.side_effect = [["teal"], ["turquoise"]]

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
                "matched_color_names": ["teal", "turquoise"]
            }
        }
        self.assertEqual(expected, result)



if __name__ == "__main__":
    unittest.main()
