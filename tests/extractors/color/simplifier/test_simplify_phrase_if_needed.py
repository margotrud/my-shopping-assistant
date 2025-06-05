import unittest
from unittest.mock import patch
from Chatbot.extractors.color.llm.simplifier import simplify_phrase_if_needed

class TestSimplifyPhraseIfNeeded(unittest.TestCase):
    def test_case_01(self):
        phrase = 'red'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=['red']), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=None), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['red'], result)

    def test_case_02(self):
        phrase = 'soft pink'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light pink'], result)

    def test_case_03(self):
        phrase = 'peachy'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['peach']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['peach'], result)

    def test_case_04(self):
        phrase = 'nude'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['soft beige']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['soft beige'], result)

    def test_case_05(self):
        phrase = 'glamorous'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['glamorous'], result)

    def test_case_06(self):
        phrase = 'light purple'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light purple']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light purple'], result)

    def test_case_07(self):
        phrase = 'barely-there'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['natural']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['natural'], result)

    def test_case_08(self):
        phrase = 'rosy'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=['rosy']), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=None), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['rosy'], result)

    def test_case_09(self):
        phrase = 'natural glow'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['natural glow']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['natural glow'], result)

    def test_case_10(self):
        phrase = 'blush'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['soft pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['soft pink'], result)


    def test_case_11(self):
        phrase = 'soft orange'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['soft orange']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['soft orange'], result)

    def test_case_12(self):
        phrase = 'dusty rose'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['dusty rose']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['dusty rose'], result)

    def test_case_13(self):
        phrase = 'minty'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['mint green']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['mint green'], result)

    def test_case_14(self):
        phrase = 'vibrant red'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['vibrant red']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['vibrant red'], result)

    def test_case_15(self):
        phrase = 'golden'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['gold']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['gold'], result)

    def test_case_16(self):
        phrase = 'bronzy'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['bronze']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['bronze'], result)

    def test_case_17(self):
        phrase = 'coppery'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['copper']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['copper'], result)

    def test_case_18(self):
        phrase = 'silverish'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['silver']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['silver'], result)

    def test_case_19(self):
        phrase = 'reddish'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['red']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['red'], result)

    def test_case_20(self):
        phrase = 'bluish'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['blue']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['blue'], result)

    def test_case_21(self):
        phrase = 'greenish'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['green']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['green'], result)

    def test_case_22(self):
        phrase = 'peach-beige'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light peach']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light peach'], result)

    def test_case_23(self):
        phrase = 'warm caramel'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['warm caramel']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['warm caramel'], result)

    def test_case_24(self):
        phrase = 'soft lilac'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light purple']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light purple'], result)

    def test_case_25(self):
        phrase = 'mocha'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['brown']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['brown'], result)

    def test_case_26(self):
        phrase = 'charcoal'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['dark grey']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['dark grey'], result)

    def test_case_27(self):
        phrase = 'sky blue'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light blue']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light blue'], result)

    def test_case_28(self):
        phrase = 'forest green'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['dark green']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['dark green'], result)

    def test_case_29(self):
        phrase = 'plum'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['deep purple']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['deep purple'], result)

    def test_case_30(self):
        phrase = 'bubblegum'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['bright pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['bright pink'], result)


    def test_case_31(self):
        phrase = 'baby pink'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light pink'], result)

    def test_case_32(self):
        phrase = 'burgundy'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['deep red']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['deep red'], result)

    def test_case_33(self):
        phrase = 'ivory'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['off white']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['off white'], result)

    def test_case_34(self):
        phrase = 'sand'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['beige']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['beige'], result)

    def test_case_35(self):
        phrase = 'taupe'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['taupe']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['taupe'], result)

    def test_case_36(self):
        phrase = 'almond'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light beige']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light beige'], result)

    def test_case_37(self):
        phrase = 'honey'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['golden beige']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['golden beige'], result)

    def test_case_38(self):
        phrase = 'cherry'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['red']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['red'], result)

    def test_case_39(self):
        phrase = 'rosewood'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['brown red']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['brown red'], result)

    def test_case_40(self):
        phrase = 'mauve'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['muted purple']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['muted purple'], result)


    def test_case_41(self):
        phrase = 'terracotta'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['orange brown']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['orange brown'], result)

    def test_case_42(self):
        phrase = 'coral'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['peach pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['peach pink'], result)

    def test_case_43(self):
        phrase = 'orchid'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['purple pink']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['purple pink'], result)

    def test_case_44(self):
        phrase = 'cream'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light yellow']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light yellow'], result)

    def test_case_45(self):
        phrase = 'beige'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['nude']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['nude'], result)

    def test_case_46(self):
        phrase = 'tan'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['light brown']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['light brown'], result)

    def test_case_47(self):
        phrase = 'espresso'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['dark brown']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['dark brown'], result)

    def test_case_48(self):
        phrase = 'midnight blue'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['navy']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['navy'], result)

    def test_case_49(self):
        phrase = 'slate'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['grey']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['grey'], result)

    def test_case_50(self):
        phrase = 'denim'
        with patch("Chatbot.extractors.color.simplifier.get_cached_simplified", return_value=[]), \
             patch("Chatbot.extractors.color.simplifier.simplify_color_description_with_llm", return_value=['blue']), \
             patch("Chatbot.extractors.color.simplifier.store_simplified_to_cache"):
            result = simplify_phrase_if_needed(phrase)
            self.assertEqual(['blue'], result)
