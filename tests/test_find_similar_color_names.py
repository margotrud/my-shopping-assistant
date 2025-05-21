import unittest
from Chatbot.scripts.RGB import find_similar_color_names

class TestFindSimilarColorNames(unittest.TestCase):
    def setUp(self):
        self.red = (255, 0, 0)
        self.sample_rgb_map = {
            "red": (255, 0, 0),
            "crimson": (220, 20, 60),
            "tomato": (255, 99, 71),
            "salmon": (250, 128, 114),
            "pink": (255, 192, 203),
            "peach": (255, 229, 180),
            "dark red": (139, 0, 0),
            "maroon": (128, 0, 0),
            "orange red": (255, 69, 0),
            "hot pink": (255, 105, 180),
            "firebrick": (178, 34, 34),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "blue": (0, 0, 255),
        }

    def test_case_01(self):
        expected = ["red"]
        result = find_similar_color_names(self.red, {"red": (255, 0, 0)}, threshold=0)
        self.assertEqual(expected, result)

    def test_case_02(self):
        expected = ['red', 'orange red']
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=70)
        self.assertEqual(expected, result)

    def test_case_03(self):
        expected = ['red', 'crimson', 'tomato', 'dark red', 'orange red', 'firebrick']
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=125)
        self.assertEqual(expected, result)

    def test_case_04(self):
        expected = ["red", "crimson", "tomato", "salmon"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=140)
        self.assertEqual(expected, result)

    def test_case_05(self):
        expected = []
        result = find_similar_color_names(self.red, {"blue": (0, 0, 255)}, threshold=100)
        self.assertEqual(expected, result)

    def test_case_06(self):
        expected = ["red", "crimson", "tomato", "orange red"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=130)
        self.assertEqual(expected, result)

    def test_case_07(self):
        expected = ["red", "dark red", "maroon", "firebrick"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=130)
        self.assertEqual(expected, result)

    def test_case_08(self):
        expected = ["red", "crimson", "tomato", "orange red"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=129.9)
        self.assertEqual(expected, result)

    def test_case_09(self):
        expected = []
        result = find_similar_color_names((0, 255, 0), self.sample_rgb_map, threshold=30)
        self.assertEqual(expected, result)

    def test_case_10(self):
        expected = ["white"]
        result = find_similar_color_names((255, 255, 255), self.sample_rgb_map, threshold=0)
        self.assertEqual(expected, result)

    def test_case_11(self):
        expected = ["black"]
        result = find_similar_color_names((0, 0, 0), self.sample_rgb_map, threshold=0)
        self.assertEqual(expected, result)

    def test_case_12(self):
        expected = ["red", "crimson", "tomato", "orange red", "firebrick"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=135)
        self.assertEqual(expected, result)

    def test_case_13(self):
        expected = ["crimson"]
        result = find_similar_color_names((230, 30, 60), self.sample_rgb_map, threshold=40)
        self.assertEqual(expected, result)

    def test_case_14(self):
        expected = []
        result = find_similar_color_names((123, 222, 100), self.sample_rgb_map, threshold=50)
        self.assertEqual(expected, result)

    def test_case_15(self):
        expected = ["red", "dark red", "maroon"]
        result = find_similar_color_names((200, 0, 0), self.sample_rgb_map, threshold=130)
        self.assertEqual(expected, result)

    def test_case_16(self):
        expected = ["pink", "hot pink"]
        result = find_similar_color_names((255, 160, 190), self.sample_rgb_map, threshold=70)
        self.assertEqual(expected, result)

    def test_case_17(self):
        expected = ["salmon", "tomato"]
        result = find_similar_color_names((250, 115, 100), self.sample_rgb_map, threshold=50)
        self.assertEqual(expected, result)

    def test_case_18(self):
        expected = ["red", "crimson", "tomato"]
        result = find_similar_color_names((255, 10, 5), self.sample_rgb_map, threshold=125)
        self.assertEqual(expected, result)

    def test_case_19(self):
        expected = ["peach"]
        result = find_similar_color_names((255, 230, 180), self.sample_rgb_map, threshold=15)
        self.assertEqual(expected, result)

    def test_case_20(self):
        expected = []
        result = find_similar_color_names((50, 50, 200), self.sample_rgb_map, threshold=40)
        self.assertEqual(expected, result)

    def test_case_21(self):
        expected = ["orange red", "tomato"]
        result = find_similar_color_names((255, 70, 10), self.sample_rgb_map, threshold=50)
        self.assertEqual(expected, result)

    def test_case_22(self):
        expected = ["dark red", "maroon"]
        result = find_similar_color_names((140, 0, 0), self.sample_rgb_map, threshold=20)
        self.assertEqual(expected, result)

    def test_case_23(self):
        expected = ["crimson", "firebrick"]
        result = find_similar_color_names((200, 30, 40), self.sample_rgb_map, threshold=70)
        self.assertEqual(expected, result)

    def test_case_24(self):
        expected = ["salmon", "peach"]
        result = find_similar_color_names((252, 150, 140), self.sample_rgb_map, threshold=100)
        self.assertEqual(expected, result)

    def test_case_25(self):
        expected = ["blue"]
        result = find_similar_color_names((0, 0, 254), self.sample_rgb_map, threshold=5)
        self.assertEqual(expected, result)

    def test_case_26(self):
        expected = []
        result = find_similar_color_names((100, 100, 100), self.sample_rgb_map, threshold=50)
        self.assertEqual(expected, result)

    def test_case_27(self):
        expected = ["red", "crimson"]
        result = find_similar_color_names((254, 5, 10), self.sample_rgb_map, threshold=90)
        self.assertEqual(expected, result)

    def test_case_28(self):
        expected = ["red", "tomato", "salmon", "orange red"]
        result = find_similar_color_names((255, 60, 50), self.sample_rgb_map, threshold=140)
        self.assertEqual(expected, result)

    def test_case_29(self):
        expected = ["pink"]
        result = find_similar_color_names((255, 180, 200), self.sample_rgb_map, threshold=40)
        self.assertEqual(expected, result)

    def test_case_30(self):
        expected = ["maroon"]
        result = find_similar_color_names((130, 0, 0), self.sample_rgb_map, threshold=5)
        self.assertEqual(expected, result)

    def test_case_31(self):
        expected = ["red"]
        result = find_similar_color_names((255, 0, 10), self.sample_rgb_map, threshold=15)
        self.assertEqual(expected, result)

    def test_case_32(self):
        expected = ["pink", "hot pink"]
        result = find_similar_color_names((255, 170, 190), self.sample_rgb_map, threshold=80)
        self.assertEqual(expected, result)

    def test_case_33(self):
        expected = ["firebrick"]
        result = find_similar_color_names((180, 35, 35), self.sample_rgb_map, threshold=15)
        self.assertEqual(expected, result)

    def test_case_34(self):
        expected = []
        result = find_similar_color_names((123, 222, 10), self.sample_rgb_map, threshold=20)
        self.assertEqual(expected, result)

    def test_case_35(self):
        expected = ["dark red"]
        result = find_similar_color_names((140, 0, 5), self.sample_rgb_map, threshold=10)
        self.assertEqual(expected, result)

    def test_case_36(self):
        expected = ["salmon"]
        result = find_similar_color_names((248, 130, 115), self.sample_rgb_map, threshold=20)
        self.assertEqual(expected, result)

    def test_case_37(self):
        expected = ["crimson", "tomato", "orange red"]
        result = find_similar_color_names((240, 50, 50), self.sample_rgb_map, threshold=100)
        self.assertEqual(expected, result)

    def test_case_38(self):
        expected = ["white"]
        result = find_similar_color_names((250, 250, 250), self.sample_rgb_map, threshold=10)
        self.assertEqual(expected, result)

    def test_case_39(self):
        expected = []
        result = find_similar_color_names((30, 30, 30), self.sample_rgb_map, threshold=10)
        self.assertEqual(expected, result)

    def test_case_40(self):
        expected = ["hot pink"]
        result = find_similar_color_names((255, 110, 185), self.sample_rgb_map, threshold=20)
        self.assertEqual(expected, result)

    def test_case_41(self):
        expected = ["red", "crimson", "tomato", "firebrick"]
        result = find_similar_color_names((250, 20, 50), self.sample_rgb_map, threshold=130)
        self.assertEqual(expected, result)

    def test_case_42(self):
        expected = []
        result = find_similar_color_names((120, 200, 150), self.sample_rgb_map, threshold=30)
        self.assertEqual(expected, result)

    def test_case_43(self):
        expected = ["red", "tomato"]
        result = find_similar_color_names((255, 40, 40), self.sample_rgb_map, threshold=90)
        self.assertEqual(expected, result)

    def test_case_44(self):
        expected = ["salmon", "peach", "pink"]
        result = find_similar_color_names((255, 180, 170), self.sample_rgb_map, threshold=95)
        self.assertEqual(expected, result)

    def test_case_45(self):
        expected = ["blue"]
        result = find_similar_color_names((0, 0, 255), self.sample_rgb_map, threshold=0)
        self.assertEqual(expected, result)

    def test_case_46(self):
        expected = ["dark red", "firebrick", "maroon"]
        result = find_similar_color_names((150, 0, 0), self.sample_rgb_map, threshold=50)
        self.assertEqual(expected, result)

    def test_case_47(self):
        expected = ["orange red"]
        result = find_similar_color_names((255, 60, 0), self.sample_rgb_map, threshold=20)
        self.assertEqual(expected, result)

    def test_case_48(self):
        expected = ["pink"]
        result = find_similar_color_names((255, 193, 200), self.sample_rgb_map, threshold=10)
        self.assertEqual(expected, result)

    def test_case_49(self):
        expected = []
        result = find_similar_color_names((80, 90, 100), self.sample_rgb_map, threshold=25)
        self.assertEqual(expected, result)

    def test_case_50(self):
        expected = ["red", "crimson", "tomato", "salmon", "orange red", "firebrick", "dark red", "maroon"]
        result = find_similar_color_names(self.red, self.sample_rgb_map, threshold=145)
        self.assertEqual(expected, result)
