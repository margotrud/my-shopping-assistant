# tests/extractors/color/test_find_similar_color_names.py

import unittest
from Chatbot.extractors.color.utils.rgb_distance import find_similar_color_names

class TestFindSimilarColorNames(unittest.TestCase):

    def test_case_01(self):
        base_rgb = (5, 3, 7)
        rgb_map = {
            "color_0": (5, 3, 7),
            "color_1": (7, 6, 11),
            "color_2": (9, 9, 15),
            "color_3": (11, 12, 19),
            "color_4": (13, 15, 23)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=20)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_02(self):
        base_rgb = (10, 6, 14)
        rgb_map = {
            "color_0": (10, 6, 14),
            "color_1": (12, 9, 18),
            "color_2": (14, 12, 22),
            "color_3": (16, 15, 26),
            "color_4": (18, 18, 30)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=30)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_03(self):
        base_rgb = (15, 9, 21)
        rgb_map = {
            "color_0": (15, 9, 21),
            "color_1": (17, 12, 25),
            "color_2": (19, 15, 29),
            "color_3": (21, 18, 33),
            "color_4": (23, 21, 37)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=40)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_04(self):
        base_rgb = (20, 12, 28)
        rgb_map = {
            "color_0": (20, 12, 28),
            "color_1": (22, 15, 32),
            "color_2": (24, 18, 36),
            "color_3": (26, 21, 40),
            "color_4": (28, 24, 44)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=50)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_05(self):
        base_rgb = (25, 15, 35)
        rgb_map = {
            "color_0": (25, 15, 35),
            "color_1": (27, 18, 39),
            "color_2": (29, 21, 43),
            "color_3": (31, 24, 47),
            "color_4": (33, 27, 51)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=60)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_06(self):
        base_rgb = (30, 18, 42)
        rgb_map = {
            "color_0": (30, 18, 42),
            "color_1": (32, 21, 46),
            "color_2": (34, 24, 50),
            "color_3": (36, 27, 54),
            "color_4": (38, 30, 58)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=70)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_07(self):
        base_rgb = (35, 21, 49)
        rgb_map = {
            "color_0": (35, 21, 49),
            "color_1": (37, 24, 53),
            "color_2": (39, 27, 57),
            "color_3": (41, 30, 61),
            "color_4": (43, 33, 65)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=80)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_08(self):
        base_rgb = (40, 24, 56)
        rgb_map = {
            "color_0": (40, 24, 56),
            "color_1": (42, 27, 60),
            "color_2": (44, 30, 64),
            "color_3": (46, 33, 68),
            "color_4": (48, 36, 72)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=90)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_09(self):
        base_rgb = (45, 27, 63)
        rgb_map = {
            "color_0": (45, 27, 63),
            "color_1": (47, 30, 67),
            "color_2": (49, 33, 71),
            "color_3": (51, 36, 75),
            "color_4": (53, 39, 79)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=100)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_10(self):
        base_rgb = (50, 30, 70)
        rgb_map = {
            "color_0": (50, 30, 70),
            "color_1": (52, 33, 74),
            "color_2": (54, 36, 78),
            "color_3": (56, 39, 82),
            "color_4": (58, 42, 86)
        }
        expected = ["color_0", "color_1"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=10)
        self.assertEqual(sorted(expected), sorted(result))


    def test_case_11(self):
        base_rgb = (55, 33, 77)
        rgb_map = {
            "color_0": (55, 33, 77),
            "color_1": (57, 36, 81),
            "color_2": (59, 39, 85),
            "color_3": (61, 42, 89),
            "color_4": (63, 45, 93)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=20)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_12(self):
        base_rgb = (60, 36, 84)
        rgb_map = {
            "color_0": (60, 36, 84),
            "color_1": (62, 39, 88),
            "color_2": (64, 42, 92),
            "color_3": (66, 45, 96),
            "color_4": (68, 48, 100)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=30)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_13(self):
        base_rgb = (65, 39, 91)
        rgb_map = {
            "color_0": (65, 39, 91),
            "color_1": (67, 42, 95),
            "color_2": (69, 45, 99),
            "color_3": (71, 48, 103),
            "color_4": (73, 51, 107)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=40)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_14(self):
        base_rgb = (70, 42, 98)
        rgb_map = {
            "color_0": (70, 42, 98),
            "color_1": (72, 45, 102),
            "color_2": (74, 48, 106),
            "color_3": (76, 51, 110),
            "color_4": (78, 54, 114)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=50)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_15(self):
        base_rgb = (75, 45, 105)
        rgb_map = {
            "color_0": (75, 45, 105),
            "color_1": (77, 48, 109),
            "color_2": (79, 51, 113),
            "color_3": (81, 54, 117),
            "color_4": (83, 57, 121)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=60)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_16(self):
        base_rgb = (80, 48, 112)
        rgb_map = {
            "color_0": (80, 48, 112),
            "color_1": (82, 51, 116),
            "color_2": (84, 54, 120),
            "color_3": (86, 57, 124),
            "color_4": (88, 60, 128)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=70)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_17(self):
        base_rgb = (85, 51, 119)
        rgb_map = {
            "color_0": (85, 51, 119),
            "color_1": (87, 54, 123),
            "color_2": (89, 57, 127),
            "color_3": (91, 60, 131),
            "color_4": (93, 63, 135)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=80)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_18(self):
        base_rgb = (90, 54, 126)
        rgb_map = {
            "color_0": (90, 54, 126),
            "color_1": (92, 57, 130),
            "color_2": (94, 60, 134),
            "color_3": (96, 63, 138),
            "color_4": (98, 66, 142)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=90)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_19(self):
        base_rgb = (95, 57, 133)
        rgb_map = {
            "color_0": (95, 57, 133),
            "color_1": (97, 60, 137),
            "color_2": (99, 63, 141),
            "color_3": (101, 66, 145),
            "color_4": (103, 69, 149)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=100)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_20(self):
        base_rgb = (100, 60, 140)
        rgb_map = {
            "color_0": (100, 60, 140),
            "color_1": (102, 63, 144),
            "color_2": (104, 66, 148),
            "color_3": (106, 69, 152),
            "color_4": (108, 72, 156)
        }
        expected = ["color_0", "color_1"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=10)
        self.assertEqual(sorted(expected), sorted(result))


    def test_case_21(self):
        base_rgb = (105, 63, 147)
        rgb_map = {
            "color_0": (105, 63, 147),
            "color_1": (107, 66, 151),
            "color_2": (109, 69, 155),
            "color_3": (111, 72, 159),
            "color_4": (113, 75, 163)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=20)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_22(self):
        base_rgb = (110, 66, 154)
        rgb_map = {
            "color_0": (110, 66, 154),
            "color_1": (112, 69, 158),
            "color_2": (114, 72, 162),
            "color_3": (116, 75, 166),
            "color_4": (118, 78, 170)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=30)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_23(self):
        base_rgb = (115, 69, 161)
        rgb_map = {
            "color_0": (115, 69, 161),
            "color_1": (117, 72, 165),
            "color_2": (119, 75, 169),
            "color_3": (121, 78, 173),
            "color_4": (123, 81, 177)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=40)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_24(self):
        base_rgb = (120, 72, 168)
        rgb_map = {
            "color_0": (120, 72, 168),
            "color_1": (122, 75, 172),
            "color_2": (124, 78, 176),
            "color_3": (126, 81, 180),
            "color_4": (128, 84, 184)
        }
        expected = ["color_0", "color_1", "color_2", "color_3", "color_4"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=50)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_25(self):
        base_rgb = (125, 75, 175)
        rgb_map = {
            "color_0": (125, 75, 175),
            "color_1": (127, 78, 179),
            "color_2": (129, 81, 183),
            "color_3": (131, 84, 187),
            "color_4": (133, 87, 191)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=60)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_26(self):
        base_rgb = (130, 78, 182)
        rgb_map = {
            "color_0": (130, 78, 182),
            "color_1": (132, 81, 186),
            "color_2": (134, 84, 190),
            "color_3": (136, 87, 194),
            "color_4": (138, 90, 198)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=70)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_27(self):
        base_rgb = (135, 81, 189)
        rgb_map = {
            "color_0": (135, 81, 189),
            "color_1": (137, 84, 193),
            "color_2": (139, 87, 197),
            "color_3": (141, 90, 201),
            "color_4": (143, 93, 205)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=80)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_28(self):
        base_rgb = (140, 84, 196)
        rgb_map = {
            "color_0": (140, 84, 196),
            "color_1": (142, 87, 200),
            "color_2": (144, 90, 204),
            "color_3": (146, 93, 208),
            "color_4": (148, 96, 212)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=90)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_29(self):
        base_rgb = (145, 87, 203)
        rgb_map = {
            "color_0": (145, 87, 203),
            "color_1": (147, 90, 207),
            "color_2": (149, 93, 211),
            "color_3": (151, 96, 215),
            "color_4": (153, 99, 219)
        }
        expected = ["color_0", "color_1", "color_2", "color_3"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=100)
        self.assertEqual(sorted(expected), sorted(result))

    def test_case_30(self):
        base_rgb = (150, 90, 210)
        rgb_map = {
            "color_0": (150, 90, 210),
            "color_1": (152, 93, 214),
            "color_2": (154, 96, 218),
            "color_3": (156, 99, 222),
            "color_4": (158, 102, 226)
        }
        expected = ["color_0"]
        result = find_similar_color_names(base_rgb, rgb_map, threshold=10)
        self.assertEqual(sorted(expected), sorted(result))

