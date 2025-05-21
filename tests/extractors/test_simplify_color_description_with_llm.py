import json
import os
import requests
import unittest

import webcolors
from dotenv import load_dotenv
load_dotenv()
load_dotenv(dotenv_path="path/to/.env")

from unittest.mock import patch

def simplify_color_description_with_llm(color_phrase: str) -> list[str]:
    """
    Uses an LLM via OpenRouter to simplify a descriptive color name (e.g. 'cherry')
    into a clean [modifier + tone] format (e.g. ['bright red']).

    Args:
        color_phrase (str): A non-standard color term (e.g. 'cherry')

    Returns:
        list[str]: A single-item list like ['bright red']
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env")

    prompt = (
        f"Simplify the color '{color_phrase}' using a base tone (e.g. red, pink, beige) "
        f"and a modifier (e.g. bright, soft, dark). Return only the simplified phrase, "
        f"no explanation, no punctuation, no quotes. Example: 'bright red'"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 15,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error {response.status_code}: {response.text}")

    raw_output = response.json()["choices"][0]["message"]["content"].strip().lower()

    # ✅ Load all valid webcolors as tones
    tone_keywords = set(map(str.lower, webcolors.CSS3_NAMES_TO_HEX.keys()))
    modifier_keywords = {"bright", "soft", "muted", "warm", "cool", "dark", "light", "bold", "shiny", "deep"}

    # Tokenize and find valid modifier + tone pairs
    tokens = raw_output.split()
    for i in range(len(tokens) - 1):
        mod, tone = tokens[i], tokens[i + 1]
        if mod in modifier_keywords and tone in tone_keywords:
            return [f"{mod} {tone}"]

    # Fallback: return first tone only if no modifier found
    for tok in tokens:
        if tok in tone_keywords:
            return [tok]

    return []  # Nothing matched




import unittest
from unittest.mock import patch


class TestSimplifyColorDescriptionLLM(unittest.TestCase):

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_01(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "bright red"}}]
        }
        self.assertEqual(["bright red"], simplify_color_description_with_llm("cherry"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_02(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft pink"}}]
        }
        self.assertEqual(["soft pink"], simplify_color_description_with_llm("rosé"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_03(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted beige"}}]
        }
        self.assertEqual(["muted beige"], simplify_color_description_with_llm("taupe"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_04(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep brown"}}]
        }
        self.assertEqual(["deep brown"], simplify_color_description_with_llm("mocha"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_05(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "shiny gold"}}]
        }
        self.assertEqual(["shiny gold"], simplify_color_description_with_llm("goldenrod"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_06(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm pink"}}]
        }
        self.assertEqual(["warm pink"], simplify_color_description_with_llm("salmon"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_07(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "bright pink"}}]
        }
        self.assertEqual(["bright pink"], simplify_color_description_with_llm("fuchsia"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_08(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted green"}}]
        }
        self.assertEqual(["muted green"], simplify_color_description_with_llm("olive"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_09(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light blue"}}]
        }
        self.assertEqual(["light blue"], simplify_color_description_with_llm("sky"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_10(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm orange"}}]
        }
        self.assertEqual(["warm orange"], simplify_color_description_with_llm("sunset"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_11(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft beige"}}]
        }
        self.assertEqual(["soft beige"], simplify_color_description_with_llm("almond"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_12(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep orange"}}]
        }
        self.assertEqual(["deep orange"], simplify_color_description_with_llm("copper"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_13(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft purple"}}]
        }
        self.assertEqual(["soft purple"], simplify_color_description_with_llm("lavender"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_14(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light peach"}}]
        }
        self.assertEqual(["light peach"], simplify_color_description_with_llm("apricot"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_15(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm brown"}}]
        }
        self.assertEqual(["warm brown"], simplify_color_description_with_llm("cinnamon"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_16(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "cool blue"}}]
        }
        self.assertEqual(["cool blue"], simplify_color_description_with_llm("ice"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_17(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep purple"}}]
        }
        self.assertEqual(["deep purple"], simplify_color_description_with_llm("grape"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_18(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "shiny pink"}}]
        }
        self.assertEqual(["shiny pink"], simplify_color_description_with_llm("rose gold"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_19(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "dark red"}}]
        }
        self.assertEqual(["dark red"], simplify_color_description_with_llm("brick"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_20(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted blue"}}]
        }
        self.assertEqual(["muted blue"], simplify_color_description_with_llm("slate"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_21(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm beige"}}]
        }
        self.assertEqual(["warm beige"], simplify_color_description_with_llm("butterscotch"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_22(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light beige"}}]
        }
        self.assertEqual(["light beige"], simplify_color_description_with_llm("champagne"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_23(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft beige"}}]
        }
        self.assertEqual(["soft beige"], simplify_color_description_with_llm("vanilla"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_24(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "dark red"}}]
        }
        self.assertEqual(["dark red"], simplify_color_description_with_llm("mulberry"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_25(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "dark gray"}}]
        }
        self.assertEqual(["dark gray"], simplify_color_description_with_llm("charcoal"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_26(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light green"}}]
        }
        self.assertEqual(["light green"], simplify_color_description_with_llm("mint"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_27(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep green"}}]
        }
        self.assertEqual(["deep green"], simplify_color_description_with_llm("pine"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_28(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm beige"}}]
        }
        self.assertEqual(["warm beige"], simplify_color_description_with_llm("honey"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_29(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "bold red"}}]
        }
        self.assertEqual(["bold red"], simplify_color_description_with_llm("berry"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_30(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep blue"}}]
        }
        self.assertEqual(["deep blue"], simplify_color_description_with_llm("sapphire"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_31(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "dark purple"}}]
        }
        self.assertEqual(["dark purple"], simplify_color_description_with_llm("plum"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_32(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm orange"}}]
        }
        self.assertEqual(["warm orange"], simplify_color_description_with_llm("terracotta"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_33(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep red"}}]
        }
        self.assertEqual(["deep red"], simplify_color_description_with_llm("rust"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_34(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft pink"}}]
        }
        self.assertEqual(["soft pink"], simplify_color_description_with_llm("blush"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_35(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "cool green"}}]
        }
        self.assertEqual(["cool green"], simplify_color_description_with_llm("jade"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_36(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted blue"}}]
        }
        self.assertEqual(["muted blue"], simplify_color_description_with_llm("denim"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_37(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light beige"}}]
        }
        self.assertEqual(["light beige"], simplify_color_description_with_llm("ivory"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_38(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft beige"}}]
        }
        self.assertEqual(["soft beige"], simplify_color_description_with_llm("eggshell"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_39(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft pink"}}]
        }
        self.assertEqual(["soft pink"], simplify_color_description_with_llm("rose"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_40(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "bold yellow"}}]
        }
        self.assertEqual(["bold yellow"], simplify_color_description_with_llm("mustard"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_41(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "cool blue"}}]
        }
        self.assertEqual(["cool blue"], simplify_color_description_with_llm("teal"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_42(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light beige"}}]
        }
        self.assertEqual(["light beige"], simplify_color_description_with_llm("sand"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_43(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "deep brown"}}]
        }
        self.assertEqual(["deep brown"], simplify_color_description_with_llm("mahogany"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_44(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "warm orange"}}]
        }
        self.assertEqual(["warm orange"], simplify_color_description_with_llm("amber"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_45(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "bright coral"}}]
        }
        self.assertEqual(["bright coral"], simplify_color_description_with_llm("coral reef"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_46(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "light blue"}}]
        }
        self.assertEqual(["light blue"], simplify_color_description_with_llm("baby blue"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_47(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted gray"}}]
        }
        self.assertEqual(["muted gray"], simplify_color_description_with_llm("ash"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_48(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "soft white"}}]
        }
        self.assertEqual(["soft white"], simplify_color_description_with_llm("pearl"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_49(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "dark blue"}}]
        }
        self.assertEqual(["dark blue"], simplify_color_description_with_llm("ink"))

    @patch("Chatbot.extractors.colors.requests.post")
    @patch("Chatbot.extractors.colors.os.getenv")
    def test_case_50(self, mock_getenv, mock_post):
        mock_getenv.return_value = "FAKE_KEY"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "muted brown"}}]
        }
        self.assertEqual(["muted brown"], simplify_color_description_with_llm("clay"))

if __name__ == "__main__":
    unittest.main()
