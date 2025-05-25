import unittest
from Chatbot.extractors.sentiment import contains_sentiment_splitter_with_segments  # Adjust path if needed

class TestSentimentSplitter(unittest.TestCase):

    def test_case_01(self):
        text = "I love pink but not bright red"
        expected = (True, ["I love pink", "not bright red"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_02(self):
        text = "Although I like red, I hate coral"
        expected = (True, ["I like red", "I hate coral"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_03(self):
        text = "She wears warm tones and cool tones"
        expected = (False, ['She wears warm tones and cool tones'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_04(self):
        text = "I love soft colors"
        expected = (False, ["I love soft colors"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_05(self):
        text = "Yes, I like beige; however, I avoid anything too orange"
        expected = (True, ["Yes, I like beige;", ", I avoid anything too orange"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_06(self):
        text = "I like red and pink"
        expected = (False, ['I like red and pink'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_07(self):
        text = "I love soft pink, but not too much shimmer"
        expected = (True, ["I love soft pink,", "not too much shimmer"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_08(self):
        text = "Even though I hate orange, I love coral"
        expected = (True, ["I hate orange", "I love coral"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_09(self):
        text = "I don't mind beige"
        expected = (False, ["I don't mind beige"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_10(self):
        text = "Yes; I wear soft tones, and avoid harsh ones"
        expected = (True, ['Yes; I wear soft tones,', 'avoid harsh ones'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_11(self):
        text = "She only likes light pink"
        expected = (False, ["She only likes light pink"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_12(self):
        text = "Soft pink is beautiful, but coral isn’t"
        expected = (True, ['Soft pink is beautiful,', 'coral isn’t'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_13(self):
        text = "Not peach; beige maybe"
        expected = (True, ["Not peach", "beige maybe"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_14(self):
        text = "Despite liking warm tones, I dislike yellow"
        expected = (True, ["Despite liking warm tones", "I dislike yellow"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_15(self):
        text = "She enjoys muted colors. However, I prefer vibrant ones."
        expected = (True, ['She enjoys muted colors.', ', I prefer vibrant ones.'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_16(self):
        text = "I like pink and also purple"
        expected = (True, ["I like pink", "also purple"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_17(self):
        text = "No to orange. Yes to warm coral."
        expected = (True, ["No to orange", "Yes to warm coral"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_18(self):
        text = "I love coral although I don’t like red"
        expected = (True, ["I love coral", "I don’t like red"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_19(self):
        text = "I like red but"
        expected = (True, ["I like red"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_20(self):
        text = "But I prefer beige"
        expected = (True, ["I prefer beige"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_21(self):
        text = "I like beige and I wear it often"
        expected = (True, ["I like beige", "I wear it often"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_22(self):
        text = "If I had to choose, I’d go for peach"
        expected = (True, ['I had to choose', 'I ’d go for peach'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_23(self):
        text = "Even if I dislike orange, I’ll take coral"
        expected = (True, ['I dislike orange', 'I ’ll take coral'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_24(self):
        text = "Either soft pink or light beige"
        expected = (False, ['Either soft pink or light beige'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_25(self):
        text = "I like peach because it's vibrant"
        expected = (True, ['I like peach', "it's vibrant"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_26(self):
        text = "I dislike shiny tones; muted ones are better"
        expected = (True, ["I dislike shiny tones", "muted ones are better"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_27(self):
        text = "Coral is nice but"
        expected = (True, ["Coral is nice"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_28(self):
        text = "but beige is elegant"
        expected = (True, ["beige is elegant"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_29(self):
        text = "I like this color"
        expected = (False, ["I like this color"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_30(self):
        text = "No shimmer; yes matte"
        expected = (True, ['No shimmer', 'yes matte'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_31(self):
        text = "Red. And also beige."
        expected = (True, ['Red.', 'also beige.'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_32(self):
        text = "Light beige and soft peach work well together"
        expected = (False, ['Light beige and soft peach work well together'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_33(self):
        text = "She neither likes gold nor silver"
        expected = (True, ["She neither likes gold", "silver"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_34(self):
        text = "Cool tones are better, not warm"
        expected = (True, ["Cool tones are better", "not warm"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_35(self):
        text = "I like red and orange and peach"
        expected = (False, ['I like red and orange and peach'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_36(self):
        text = "No preference really"
        expected = (False, ["No preference really"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_37(self):
        text = "Not blue. Green works fine."
        expected = (True, ['Not blue', 'Green works fine'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_38(self):
        text = "Yes to shimmery shades, no to matte"
        expected = (True, ["Yes to shimmery shades", "no to matte"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_39(self):
        text = "I dislike neither brown nor beige"
        expected = (True, ["I dislike neither brown", "beige"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_40(self):
        text = "Red, or maybe orange"
        expected = (True, ['Red,', 'maybe orange'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_41(self):
        text = "It's not that I hate coral, but I prefer something else"
        expected = (True, ["It's not", 'I hate coral, but I prefer something else'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_42(self):
        text = "I like soft pink and dusty rose"
        expected = (False, ['I like soft pink and dusty rose'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_43(self):
        text = "Actually, I like pink"
        expected = (True, ["I like pink"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_44(self):
        text = "It’s pink—too pink, in fact"
        expected = (True, ["It’s pink—too pink", "in fact"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_45(self):
        text = "I like lavender; however, violet is too much"
        expected = (True, ['I like lavender;', ', violet is too much'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_46(self):
        text = "Although muted, I still love dusty shades"
        expected = (True, ["muted", "I still love dusty shades"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_47(self):
        text = "Pink. But not bright."
        expected = (True, ['Pink.', 'not bright.'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_48(self):
        text = "Warm, then cool tones"
        expected = (True, ['Warm', 'then cool tones'])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_49(self):
        text = "No"
        expected = (False, ["No"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)

    def test_case_50(self):
        text = "Love this, hate that"
        expected = (True, ["Love this", "hate that"])
        result = contains_sentiment_splitter_with_segments(text)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
