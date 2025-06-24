# Chatbot/tests/extractors/color/llm/test_is_within_rgb_margin.py

import unittest
from Chatbot.extractors.color.llm.llm_rgb import is_within_rgb_margin

class TestIsWithinRgbMargin(unittest.TestCase):

    def run_case(self, rgb1, rgb2, margin, expected):
        result = is_within_rgb_margin(rgb1, rgb2, margin)
        self.assertEqual(expected, result, msg=f"\nExpected : {expected}\nActual   : {result}")

    def test_case_01(self): self.run_case((0, 0, 0), (0, 0, 0), 0, True)
    def test_case_02(self): self.run_case((0, 0, 0), (1, 1, 1), 2.0, True)
    def test_case_03(self): self.run_case((0, 0, 0), (10, 10, 10), 17.5, True)
    def test_case_04(self): self.run_case((0, 0, 0), (10, 10, 10), 15.0, False)
    def test_case_05(self): self.run_case((255, 255, 255), (255, 255, 255), 60.0, True)
    def test_case_06(self): self.run_case((0, 0, 0), (255, 255, 255), 441.0, False)
    def test_case_07(self): self.run_case((0, 0, 0), (255, 255, 255), 440.0, False)
    def test_case_08(self): self.run_case((100, 100, 100), (110, 110, 110), 18.0, True)
    def test_case_09(self): self.run_case((100, 100, 100), (110, 110, 110), 15.0, False)
    def test_case_10(self): self.run_case((10, 20, 30), (30, 20, 10), 28.3, True)

    def test_case_11(self): self.run_case((255, 0, 0), (0, 255, 0), 360, False)
    def test_case_12(self): self.run_case((255, 0, 0), (0, 255, 0), 359, False)
    def test_case_13(self): self.run_case((0, 128, 255), (128, 255, 0), 312.5, True)
    def test_case_14(self): self.run_case((0, 128, 255), (128, 255, 0), 300.0, False)
    def test_case_15(self): self.run_case((50, 50, 50), (60, 60, 60), 18.0, True)
    def test_case_16(self): self.run_case((50, 50, 50), (70, 70, 70), 34.0, False)
    def test_case_17(self): self.run_case((50, 50, 50), (80, 80, 80), 52.0, True)
    def test_case_18(self): self.run_case((50, 50, 50), (90, 90, 90), 70.0, True)
    def test_case_19(self): self.run_case((50, 50, 50), (100, 100, 100), 90.0, True)
    def test_case_20(self): self.run_case((50, 50, 50), (100, 100, 100), 85.0, False)

    def test_case_21(self): self.run_case((123, 234, 45), (67, 89, 210), 200.0, False)
    def test_case_22(self): self.run_case((123, 234, 45), (67, 89, 210), 230.0, True)
    def test_case_23(self): self.run_case((0, 123, 200), (100, 111, 150), 110.0, False)
    def test_case_24(self): self.run_case((0, 123, 200), (100, 111, 150), 113.0, True)
    def test_case_25(self): self.run_case((45, 67, 89), (98, 76, 54), 64.2, True)

    def test_case_26(self): self.run_case((250, 250, 250), (0, 0, 0), 433.0, False)
    def test_case_27(self): self.run_case((250, 250, 250), (0, 0, 0), 434.0, True)
    def test_case_28(self): self.run_case((255, 128, 64), (64, 128, 255), 270.1, False)
    def test_case_29(self): self.run_case((75, 50, 25), (25, 75, 50), 62.0, True)
    def test_case_30(self): self.run_case((75, 50, 25), (25, 75, 50), 60.0, False)

    def test_case_31(self): self.run_case((111, 222, 123), (123, 111, 222), 149.0, False)
    def test_case_32(self): self.run_case((111, 222, 123), (123, 111, 222), 140.0, False)
    def test_case_33(self): self.run_case((33, 66, 99), (99, 66, 33), 93.3, False)
    def test_case_34(self): self.run_case((33, 66, 99), (99, 66, 33), 93.2, False)
    def test_case_35(self): self.run_case((45, 85, 125), (125, 45, 85), 97.9, False)

    def test_case_36(self): self.run_case((99, 88, 77), (77, 99, 88), 27.0, True)
    def test_case_37(self): self.run_case((123, 0, 255), (255, 0, 123), 186.7, True)
    def test_case_38(self): self.run_case((11, 22, 33), (33, 22, 11), 31.2, True)
    def test_case_39(self): self.run_case((11, 22, 33), (33, 22, 11), 31.1, False)
    def test_case_40(self): self.run_case((17, 34, 51), (51, 34, 17), 48.1, True)

    def test_case_41(self): self.run_case((200, 100, 0), (0, 100, 200), 282.9, True)
    def test_case_42(self): self.run_case((200, 100, 0), (0, 100, 200), 280.0, False)
    def test_case_43(self): self.run_case((10, 10, 10), (20, 20, 20), 17.4, True)
    def test_case_44(self): self.run_case((10, 10, 10), (20, 20, 20), 17.2, False)
    def test_case_45(self): self.run_case((100, 200, 50), (50, 100, 200), 190.0, True)

    def test_case_46(self): self.run_case((240, 240, 240), (255, 255, 255), 26.0, True)
    def test_case_47(self): self.run_case((240, 240, 240), (255, 255, 255), 25.0, False)
    def test_case_48(self): self.run_case((0, 0, 0), (60, 0, 0), 60.0, True)
    def test_case_49(self): self.run_case((0, 0, 0), (61, 0, 0), 60.0, False)
    def test_case_50(self): self.run_case((100, 100, 100), (100, 100, 160), 60.0, True)

if __name__ == "__main__":
    unittest.main()
