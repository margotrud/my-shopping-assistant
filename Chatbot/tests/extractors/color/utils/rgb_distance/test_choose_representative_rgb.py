# Chatbot/tests/extractors/color/utils/test_choose_representative_rgb.py

import unittest
from Chatbot.extractors.color.utils.rgb_distance import choose_representative_rgb, rgb_distance

class TestChooseRepresentativeRgb(unittest.TestCase):

    def run_case(self, rgb_map, expected):
        result = choose_representative_rgb(rgb_map)
        self.assertEqual(expected, result, msg=f"\nExpected : {expected}\nActual   : {result}")

    def test_case_01(self): self.run_case({}, None)
    def test_case_02(self): self.run_case({"a": (0, 0, 0)}, (0, 0, 0))
    def test_case_03(self): self.run_case({"a": (255, 255, 255)}, (255, 255, 255))
    def test_case_04(self): self.run_case({"a": (10, 10, 10), "b": (10, 10, 10)}, (10, 10, 10))
    def test_case_05(self): self.run_case({"a": (0, 0, 0), "b": (255, 255, 255)}, (0, 0, 0))  # Symmetric, either accepted

    def test_case_06(self): self.run_case({"a": (0, 0, 0), "b": (0, 0, 255)}, (0, 0, 0))
    def test_case_07(self): self.run_case({"a": (0, 0, 255), "b": (0, 0, 0)}, (0, 0, 255))
    def test_case_08(self): self.run_case({"a": (0, 0, 0), "b": (0, 255, 0), "c": (255, 0, 0)}, (0, 0, 0))
    def test_case_09(self): self.run_case({"a": (10, 10, 10), "b": (30, 30, 30), "c": (50, 50, 50)}, (30, 30, 30))
    def test_case_10(self): self.run_case({"x": (0, 0, 0), "y": (255, 255, 255), "z": (128, 128, 128)}, (128, 128, 128))

    def test_case_11(self): self.run_case({"a": (5, 5, 5), "b": (10, 10, 10), "c": (20, 20, 20)}, (10, 10, 10))
    def test_case_12(self): self.run_case({"a": (10, 10, 10), "b": (20, 20, 20), "c": (30, 30, 30)}, (20, 20, 20))
    def test_case_13(self): self.run_case({"a": (0, 255, 0), "b": (255, 0, 0), "c": (0, 0, 255)}, (0, 255, 0))
    def test_case_14(self): self.run_case({"a": (100, 100, 100), "b": (150, 150, 150), "c": (200, 200, 200)}, (150, 150, 150))
    def test_case_15(self): self.run_case({"a": (0, 0, 0), "b": (0, 0, 100), "c": (0, 0, 200)}, (0, 0, 100))

    def test_case_16(self): self.run_case({"a": (0, 128, 255), "b": (128, 255, 0), "c": (255, 128, 0)}, (128, 255, 0))
    def test_case_17(self): self.run_case({"a": (10, 20, 30), "b": (40, 50, 60), "c": (70, 80, 90)}, (40, 50, 60))
    def test_case_18(self): self.run_case({"a": (123, 234, 45), "b": (67, 89, 210), "c": (190, 140, 100)}, (190, 140, 100))
    def test_case_19(self): self.run_case({"a": (33, 66, 99), "b": (66, 99, 33), "c": (99, 33, 66)}, (33, 66, 99))
    def test_case_20(self): self.run_case({"a": (0, 100, 200), "b": (200, 100, 0), "c": (100, 100, 100)}, (100, 100, 100))

    def test_case_21(self): self.run_case({"a": (11, 22, 33), "b": (33, 22, 11), "c": (22, 22, 22)}, (22, 22, 22))
    def test_case_22(self): self.run_case({"a": (255, 100, 50), "b": (50, 100, 255), "c": (100, 100, 100)}, (100, 100, 100))
    def test_case_23(self): self.run_case({"a": (100, 0, 0), "b": (0, 100, 0), "c": (0, 0, 100)}, (100, 0, 0))
    def test_case_24(self): self.run_case({"a": (99, 88, 77), "b": (77, 99, 88), "c": (88, 77, 99)}, (99, 88, 77))
    def test_case_25(self): self.run_case({"a": (120, 130, 140), "b": (140, 130, 120), "c": (130, 130, 130)}, (130, 130, 130))

    def test_case_26(self): self.run_case({"a": (1, 2, 3), "b": (4, 5, 6), "c": (7, 8, 9)}, (4, 5, 6))
    def test_case_27(self): self.run_case({"a": (0, 50, 100), "b": (100, 50, 0), "c": (50, 50, 50)}, (50, 50, 50))
    def test_case_28(self): self.run_case({"a": (10, 90, 180), "b": (180, 90, 10), "c": (95, 90, 95)}, (95, 90, 95))
    def test_case_29(self): self.run_case({"a": (25, 50, 75), "b": (75, 50, 25), "c": (50, 50, 50)}, (50, 50, 50))
    def test_case_30(self): self.run_case({"a": (60, 60, 60), "b": (80, 80, 80), "c": (100, 100, 100)}, (80, 80, 80))

    def test_case_31(self): self.run_case({"a": (100, 200, 50), "b": (50, 100, 200), "c": (200, 50, 100)}, (100, 200, 50))
    def test_case_32(self): self.run_case({"a": (123, 0, 255), "b": (255, 0, 123), "c": (200, 0, 200)}, (200, 0, 200))
    def test_case_33(self): self.run_case({"a": (111, 222, 123), "b": (123, 111, 222), "c": (117, 166, 172)}, (117, 166, 172))
    def test_case_34(self): self.run_case({"a": (45, 85, 125), "b": (125, 45, 85), "c": (85, 125, 45)}, (45, 85, 125))
    def test_case_35(self): self.run_case({"a": (20, 40, 60), "b": (60, 40, 20), "c": (40, 40, 40)}, (40, 40, 40))

    def test_case_36(self): self.run_case({"a": (0, 0, 0), "b": (255, 255, 255), "c": (128, 128, 128)}, (128, 128, 128))
    def test_case_37(self): self.run_case({"a": (0, 0, 255), "b": (0, 255, 0), "c": (255, 0, 0)}, (0, 0, 255))
    def test_case_38(self): self.run_case({"a": (0, 255, 128), "b": (128, 255, 0), "c": (64, 255, 64)}, (64, 255, 64))
    def test_case_39(self): self.run_case({"a": (210, 210, 210), "b": (220, 220, 220), "c": (230, 230, 230)}, (220, 220, 220))
    def test_case_40(self): self.run_case({"a": (10, 60, 110), "b": (110, 60, 10), "c": (60, 60, 60)}, (60, 60, 60))

    def test_case_41(self): self.run_case({"a": (255, 200, 150), "b": (150, 200, 255), "c": (200, 200, 200)}, (200, 200, 200))
    def test_case_42(self): self.run_case({"a": (17, 34, 51), "b": (51, 34, 17), "c": (34, 34, 34)}, (34, 34, 34))
    def test_case_43(self): self.run_case({"a": (0, 0, 0), "b": (50, 50, 50), "c": (100, 100, 100)}, (50, 50, 50))
    def test_case_44(self): self.run_case({"a": (100, 150, 200), "b": (150, 100, 50), "c": (125, 125, 125)}, (125, 125, 125))
    def test_case_45(self): self.run_case({"a": (64, 128, 192), "b": (192, 128, 64), "c": (128, 128, 128)}, (128, 128, 128))

    def test_case_46(self): self.run_case({"a": (10, 10, 255), "b": (10, 255, 10), "c": (255, 10, 10)}, (10, 10, 255))
    def test_case_47(self): self.run_case({"a": (250, 100, 100), "b": (100, 250, 100), "c": (100, 100, 250)}, (250, 100, 100))
    def test_case_48(self): self.run_case({"a": (60, 0, 0), "b": (0, 60, 0), "c": (0, 0, 60)}, (60, 0, 0))
    def test_case_49(self): self.run_case({"a": (200, 100, 0), "b": (0, 100, 200), "c": (100, 100, 100)}, (100, 100, 100))
    def test_case_50(self): self.run_case({"a": (0, 255, 128), "b": (128, 255, 0), "c": (64, 255, 64)}, (64, 255, 64))

if __name__ == "__main__":
    unittest.main()
