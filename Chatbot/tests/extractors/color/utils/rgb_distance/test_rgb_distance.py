# Chatbot/tests/extractors/color/llm/test_rgb_distance.py

import unittest
from Chatbot.extractors.color.utils.rgb_distance import rgb_distance

class TestRgbDistance(unittest.TestCase):

    def run_case(self, rgb1, rgb2, expected):
        result = rgb_distance(rgb1, rgb2)
        self.assertAlmostEqual(expected, result, places=4)

    def test_case_01(self): self.run_case((0, 0, 0), (0, 0, 0), 0.0)
    def test_case_02(self): self.run_case((255, 255, 255), (255, 255, 255), 0.0)
    def test_case_03(self): self.run_case((0, 0, 0), (255, 255, 255), 441.6729559300637)
    def test_case_04(self): self.run_case((255, 0, 0), (0, 255, 0), 360.62445840513925)
    def test_case_05(self): self.run_case((0, 255, 0), (0, 0, 255), 360.62445840513925)
    def test_case_06(self): self.run_case((0, 0, 255), (255, 0, 0), 360.62445840513925)
    def test_case_07(self): self.run_case((128, 128, 128), (128, 128, 128), 0.0)
    def test_case_08(self): self.run_case((128, 0, 0), (128, 128, 0), 128.0)
    def test_case_09(self): self.run_case((128, 128, 0), (0, 128, 0), 128.0)
    def test_case_10(self): self.run_case((0, 128, 128), (128, 128, 0), 181.01933598375618)

    def test_case_11(self): self.run_case((10, 20, 30), (30, 20, 10), 28.284271247461902)
    def test_case_12(self): self.run_case((50, 50, 50), (100, 100, 100), 86.60254037844386)
    def test_case_13(self): self.run_case((0, 0, 0), (0, 100, 0), 100.0)
    def test_case_14(self): self.run_case((0, 0, 0), (100, 0, 0), 100.0)
    def test_case_15(self): self.run_case((0, 0, 0), (0, 0, 100), 100.0)
    def test_case_16(self): self.run_case((10, 10, 10), (20, 20, 20), 17.320508075688775)
    def test_case_17(self): self.run_case((0, 128, 255), (128, 255, 0), 312.31073310000826)
    def test_case_18(self): self.run_case((200, 200, 200), (100, 100, 100), 173.20508075688772)
    def test_case_19(self): self.run_case((100, 0, 0), (0, 100, 100), 173.20508075688772)
    def test_case_20(self): self.run_case((255, 100, 50), (50, 100, 255), 289.9137802864845)

    def test_case_21(self): self.run_case((5, 5, 5), (10, 10, 10), 8.660254037844387)
    def test_case_22(self): self.run_case((0, 10, 0), (10, 0, 10), 17.320508075688775)
    def test_case_23(self): self.run_case((240, 240, 240), (255, 255, 255), 25.98076211353316)
    def test_case_24(self): self.run_case((100, 150, 200), (150, 100, 50), 165.83123951777)
    def test_case_25(self): self.run_case((30, 60, 90), (60, 30, 90), 42.42640687119285)
    def test_case_26(self): self.run_case((50, 25, 0), (0, 25, 50), 70.71067811865476)
    def test_case_27(self): self.run_case((123, 234, 45), (67, 89, 210), 226.68480319597958)
    def test_case_28(self): self.run_case((0, 123, 200), (100, 111, 150), 112.44554237496477)
    def test_case_29(self): self.run_case((45, 67, 89), (98, 76, 54), 64.1482657598785)
    def test_case_30(self): self.run_case((250, 250, 250), (0, 0, 0), 433.0127018922193)

    def test_case_31(self): self.run_case((255, 128, 64), (64, 128, 255), 270.1147904132612)
    def test_case_32(self): self.run_case((75, 50, 25), (25, 75, 50), 61.237243569579455)
    def test_case_33(self): self.run_case((100, 200, 50), (50, 100, 200), 187.08287276509395)
    def test_case_34(self): self.run_case((111, 222, 123), (123, 111, 222), 149.21796138535066)
    def test_case_35(self): self.run_case((33, 66, 99), (99, 66, 33), 93.33809511662427)
    def test_case_36(self): self.run_case((80, 90, 100), (100, 80, 90), 24.49489742783178)
    def test_case_37(self): self.run_case((200, 150, 100), (100, 200, 150), 122.47448713915891)
    def test_case_38(self): self.run_case((45, 85, 125), (125, 45, 85), 97.97958971132712)
    def test_case_39(self): self.run_case((55, 155, 255), (255, 155, 55), 282.842712474619)
    def test_case_40(self): self.run_case((99, 88, 77), (77, 99, 88), 26.94438717061496)

    def test_case_41(self): self.run_case((5, 10, 15), (15, 10, 5), 14.142135623730951)
    def test_case_42(self): self.run_case((123, 0, 255), (255, 0, 123), 186.67619023324855)
    def test_case_43(self): self.run_case((200, 100, 50), (50, 200, 100), 187.08287276509395)
    def test_case_44(self): self.run_case((0, 10, 20), (20, 10, 0), 28.284271247461902)
    def test_case_45(self): self.run_case((20, 40, 60), (60, 40, 20), 56.568542494923804)
    def test_case_46(self): self.run_case((210, 210, 210), (220, 220, 220), 17.320508075688775)
    def test_case_47(self): self.run_case((11, 22, 33), (33, 22, 11), 31.11269837220809)
    def test_case_48(self): self.run_case((17, 34, 51), (51, 34, 17), 48.08326112068523)
    def test_case_49(self): self.run_case((0, 255, 128), (128, 255, 0), 181.01933598375618)
    def test_case_50(self): self.run_case((200, 100, 0), (0, 100, 200), 282.842712474619)

if __name__ == "__main__":
    unittest.main()
