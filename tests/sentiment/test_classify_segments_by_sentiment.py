# tests/test_classify_segments_by_sentiment_no_neutral.py

import unittest
from unittest.mock import patch
from Chatbot.extractors.sentiment import classify_segments_by_sentiment_no_neutral

class TestClassifySegmentsBySentimentNoNeutral(unittest.TestCase):

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_01(self, mock_detect):
        mock_detect.return_value = "positive"
        expected = {"positive": ["I like pink"], "negative": []}
        result = classify_segments_by_sentiment_no_neutral(True, ["I like pink"])
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_02(self, mock_detect):
        mock_detect.return_value = "negative"
        expected = {"positive": [], "negative": ["I hate red"]}
        result = classify_segments_by_sentiment_no_neutral(True, ["I hate red"])
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_03(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        expected = {
            "positive": ["I love beige"],
            "negative": ["I dislike coral"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, ["I love beige", "I dislike coral"])
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_04(self, mock_detect):
        mock_detect.return_value = "neutral"
        expected = {"positive": ["It’s okay"], "negative": []}
        result = classify_segments_by_sentiment_no_neutral(False, ["It’s okay"])
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_05(self, mock_detect):
        mock_detect.side_effect = ["neutral", "negative"]
        expected = {
            "positive": ["I guess it's fine"],
            "negative": ["I wouldn’t wear purple"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, ["I guess it's fine", "I wouldn’t wear purple"])
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_06(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        segments = ["I enjoy light tones", "I don't like bold colors"]
        expected = {
            "positive": ["I enjoy light tones"],
            "negative": ["I don't like bold colors"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_07(self, mock_detect):
        mock_detect.side_effect = ["negative", "positive"]
        segments = ["I enjoy light tones", "I don't like bold colors"]
        expected = {
            "positive": ["I don't like bold colors"],
            "negative": ["I enjoy light tones"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_08(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        segments = ["Soft beige looks nice", "I avoid anything too flashy"]
        expected = {
            "positive": ["Soft beige looks nice"],
            "negative": ["I avoid anything too flashy"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_09(self, mock_detect):
        mock_detect.side_effect = ["negative", "positive"]
        segments = ["I hate neon", "Muted coral could work"]
        expected = {
            "positive": ["Muted coral could work"],
            "negative": ["I hate neon"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_10(self, mock_detect):
        mock_detect.side_effect = ["neutral", "negative"]
        segments = ["It's okay", "but I dislike orange"]
        expected = {
            "positive": ["It's okay"],
            "negative": ["but I dislike orange"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_11(self, mock_detect):
        mock_detect.side_effect = ["positive", "positive"]
        segments = ["I love soft peach", "and I like nude"]
        expected = {
            "positive": ["I love soft peach", "and I like nude"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_12(self, mock_detect):
        mock_detect.side_effect = ["negative", "negative"]
        segments = ["I hate dark pink", "I never wear orange"]
        expected = {
            "positive": [],
            "negative": ["I hate dark pink", "I never wear orange"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_13(self, mock_detect):
        mock_detect.side_effect = ["positive", "neutral"]
        segments = ["I really like dusty rose", "not sure about bronze"]
        expected = {
            "positive": ["I really like dusty rose", "not sure about bronze"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_14(self, mock_detect):
        mock_detect.side_effect = ["neutral", "negative"]
        segments = ["maybe mauve is okay", "but I avoid neon"]
        expected = {
            "positive": ["maybe mauve is okay"],
            "negative": ["but I avoid neon"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_15(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        segments = ["soft brown is nice", "I never liked flashy pink"]
        expected = {
            "positive": ["soft brown is nice"],
            "negative": ["I never liked flashy pink"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_16(self, mock_detect):
        mock_detect.side_effect = ["negative", "neutral"]
        segments = ["I don’t like bold purple", "taupe might be fine"]
        expected = {
            "positive": ["taupe might be fine"],
            "negative": ["I don’t like bold purple"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_17(self, mock_detect):
        mock_detect.side_effect = ["positive", "positive"]
        segments = ["I love soft lilac", "and I also enjoy beige"]
        expected = {
            "positive": ["I love soft lilac", "and I also enjoy beige"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_18(self, mock_detect):
        mock_detect.side_effect = ["negative", "negative"]
        segments = ["I avoid harsh colors", "and dislike glittery tones"]
        expected = {
            "positive": [],
            "negative": ["I avoid harsh colors", "and dislike glittery tones"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_19(self, mock_detect):
        mock_detect.side_effect = ["positive"]
        segments = ["nude lipstick always works for me"]
        expected = {
            "positive": ["nude lipstick always works for me"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_20(self, mock_detect):
        mock_detect.side_effect = ["negative"]
        segments = ["I don't like red tones"]
        expected = {
            "positive": [],
            "negative": ["I don't like red tones"]
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_21(self, mock_detect):
        mock_detect.side_effect = ["neutral"]
        segments = ["it's kind of okay"]
        expected = {
            "positive": ["it's kind of okay"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_22(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative", "neutral"]
        segments = ["I like rose", "I hate burgundy", "maybe beige"]
        expected = {
            "positive": ["I like rose", "maybe beige"],
            "negative": ["I hate burgundy"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_23(self, mock_detect):
        mock_detect.side_effect = ["positive", "positive", "positive"]
        segments = ["I like taupe", "love bronze", "obsessed with nude"]
        expected = {
            "positive": segments,
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_24(self, mock_detect):
        mock_detect.side_effect = ["negative", "neutral", "negative"]
        segments = ["don't want orange", "lavender maybe", "not red"]
        expected = {
            "positive": ["lavender maybe"],
            "negative": ["don't want orange", "not red"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_25(self, mock_detect):
        mock_detect.side_effect = ["positive", "neutral"]
        segments = ["cherry is cute", "plum might be okay"]
        expected = {
            "positive": ["cherry is cute", "plum might be okay"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_26(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        segments = ["peach is soft", "I dislike anything flashy"]
        expected = {
            "positive": ["peach is soft"],
            "negative": ["I dislike anything flashy"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_27(self, mock_detect):
        mock_detect.side_effect = ["negative", "positive"]
        segments = ["not into shiny gloss", "muted tones are fine"]
        expected = {
            "positive": ["muted tones are fine"],
            "negative": ["not into shiny gloss"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_28(self, mock_detect):
        mock_detect.side_effect = ["neutral", "neutral"]
        segments = ["plum maybe", "soft coral perhaps"]
        expected = {
            "positive": ["plum maybe", "soft coral perhaps"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_29(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative", "positive"]
        segments = ["peach works", "I hate purple", "beige is classic"]
        expected = {
            "positive": ["peach works", "beige is classic"],
            "negative": ["I hate purple"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_30(self, mock_detect):
        mock_detect.side_effect = ["positive"]
        segments = ["brown tones always look great"]
        expected = {
            "positive": ["brown tones always look great"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_31(self, mock_detect):
        mock_detect.side_effect = ["negative"]
        segments = ["never again neon"]
        expected = {
            "positive": [],
            "negative": ["never again neon"]
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_32(self, mock_detect):
        mock_detect.side_effect = ["neutral"]
        segments = ["cherry could work"]
        expected = {
            "positive": ["cherry could work"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_33(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative", "neutral"]
        segments = ["soft pink is great", "hate red", "taupe maybe"]
        expected = {
            "positive": ["soft pink is great", "taupe maybe"],
            "negative": ["hate red"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_34(self, mock_detect):
        mock_detect.side_effect = ["positive", "positive"]
        segments = ["I like coral", "and love dusty rose"]
        expected = {
            "positive": segments,
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_35(self, mock_detect):
        mock_detect.side_effect = ["negative", "negative"]
        segments = ["too much sparkle", "hate shiny gloss"]
        expected = {
            "positive": [],
            "negative": segments
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_36(self, mock_detect):
        mock_detect.side_effect = ["positive", "neutral"]
        segments = ["light beige is elegant", "bronze maybe"]
        expected = {
            "positive": ["light beige is elegant", "bronze maybe"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_37(self, mock_detect):
        mock_detect.side_effect = ["negative", "neutral"]
        segments = ["dislike strong colors", "lavender possibly"]
        expected = {
            "positive": ["lavender possibly"],
            "negative": ["dislike strong colors"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_38(self, mock_detect):
        mock_detect.side_effect = ["neutral", "positive"]
        segments = ["not sure about orange", "love pink nude"]
        expected = {
            "positive": ["not sure about orange", "love pink nude"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_39(self, mock_detect):
        mock_detect.side_effect = ["negative", "positive"]
        segments = ["I dislike red", "but I enjoy peach"]
        expected = {
            "positive": ["but I enjoy peach"],
            "negative": ["I dislike red"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_40(self, mock_detect):
        mock_detect.side_effect = ["positive", "negative"]
        segments = ["soft tones work well", "never liked flashy coral"]
        expected = {
            "positive": ["soft tones work well"],
            "negative": ["never liked flashy coral"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_41(self, mock_detect):
        mock_detect.side_effect = ["positive", "neutral", "negative"]
        segments = ["I like dusty mauve", "taupe maybe", "I hate hot pink"]
        expected = {
            "positive": ["I like dusty mauve", "taupe maybe"],
            "negative": ["I hate hot pink"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_42(self, mock_detect):
        mock_detect.side_effect = ["neutral", "negative", "positive"]
        segments = ["beige is fine", "avoid metallic", "love warm peach"]
        expected = {
            "positive": ["beige is fine", "love warm peach"],
            "negative": ["avoid metallic"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_43(self, mock_detect):
        mock_detect.side_effect = ["neutral"]
        segments = ["maybe something light"]
        expected = {
            "positive": ["maybe something light"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_44(self, mock_detect):
        mock_detect.side_effect = ["negative"]
        segments = ["too much shimmer"]
        expected = {
            "positive": [],
            "negative": ["too much shimmer"]
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_45(self, mock_detect):
        mock_detect.side_effect = ["positive"]
        segments = ["love the elegance of mauve"]
        expected = {
            "positive": ["love the elegance of mauve"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_46(self, mock_detect):
        mock_detect.side_effect = ["negative"]
        segments = ["I don’t like vivid gloss"]
        expected = {
            "positive": [],
            "negative": ["I don’t like vivid gloss"]
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_47(self, mock_detect):
        mock_detect.side_effect = ["positive"]
        segments = ["subtle tones are my thing"]
        expected = {
            "positive": ["subtle tones are my thing"],
            "negative": []
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_48(self, mock_detect):
        mock_detect.side_effect = ["negative"]
        segments = ["no shimmer, please"]
        expected = {
            "positive": [],
            "negative": ["no shimmer, please"]
        }
        result = classify_segments_by_sentiment_no_neutral(False, segments)
        self.assertEqual(expected, result)



    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_49(self, mock_detect):
        mock_detect.side_effect = ["neutral", "positive", "negative"]
        segments = ["it's fine", "I enjoy mauve", "but not bright pink"]
        expected = {
            "positive": ["it's fine", "I enjoy mauve"],
            "negative": ["but not bright pink"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)

    @patch("Chatbot.extractors.sentiment.detect_sentiment")
    def test_case_50(self, mock_detect):
        mock_detect.side_effect = [
            "positive", "negative", "neutral", "positive", "negative"
        ]
        segments = [
            "I adore nude shades",
            "but I hate flashy colors",
            "maybe something soft",
            "light pink is lovely",
            "never bold red again"
        ]
        expected = {
            "positive": ["I adore nude shades", "maybe something soft", "light pink is lovely"],
            "negative": ["but I hate flashy colors", "never bold red again"]
        }
        result = classify_segments_by_sentiment_no_neutral(True, segments)
        self.assertEqual(expected, result)



if __name__ == "__main__":
    unittest.main()
