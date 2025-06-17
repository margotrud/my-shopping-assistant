# tests/extractors/color/test_rgb_distance.py

import unittest
from math import isclose
from Chatbot.extractors.color.utils.rgb_distance import rgb_distance

class TestRgbDistance(unittest.TestCase):

    def test_case_01(self): self.assertTrue(isclose(0.0, rgb_distance((0, 0, 0), (0, 0, 0))))
    def test_case_02(self): self.assertTrue(isclose(255.0, rgb_distance((0, 0, 0), (255, 0, 0))))
    def test_case_03(self): self.assertTrue(isclose(255.0, rgb_distance((0, 0, 0), (0, 255, 0))))
    def test_case_04(self): self.assertTrue(isclose(255.0, rgb_distance((0, 0, 0), (0, 0, 255))))
    def test_case_05(self): self.assertTrue(isclose(0.0, rgb_distance((255, 255, 255), (255, 255, 255))))

    def test_case_06(self): self.assertTrue(isclose(441.6729, rgb_distance((0, 0, 0), (255, 255, 255)), rel_tol=1e-4))
    def test_case_07(self): self.assertTrue(isclose(219.989, rgb_distance((128, 128, 128), (255, 255, 255)), rel_tol=1e-3))
    def test_case_08(self): self.assertTrue(isclose(173.205, rgb_distance((100, 50, 25), (200, 150, 125)), rel_tol=1e-3))
    def test_case_09(self): self.assertTrue(isclose(100.0, rgb_distance((50, 50, 50), (50, 50, 150))))
    def test_case_10(self): self.assertTrue(isclose(173.205, rgb_distance((0, 0, 0), (100, 100, 100)), rel_tol=1e-3))

    def test_case_11(self): self.assertTrue(isclose(86.6025, rgb_distance((50, 50, 50), (100, 100, 100)), rel_tol=1e-3))
    def test_case_12(self): self.assertTrue(isclose(50.0, rgb_distance((0, 0, 0), (50, 0, 0))))
    def test_case_13(self): self.assertTrue(isclose(70.7106, rgb_distance((10, 10, 10), (60, 60, 10)), rel_tol=1e-3))
    def test_case_14(self): self.assertTrue(isclose(17.3205, rgb_distance((10, 10, 10), (20, 20, 20)), rel_tol=1e-3))
    def test_case_15(self): self.assertTrue(isclose(10.0, rgb_distance((10, 10, 10), (10, 10, 20))))

    def test_case_16(self): self.assertTrue(isclose(422.561, rgb_distance((0, 0, 0), (244, 244, 244)), rel_tol=1e-3))
    def test_case_17(self): self.assertTrue(isclose(173.205, rgb_distance((255, 255, 255), (155, 155, 155)), rel_tol=1e-3))
    def test_case_18(self): self.assertTrue(isclose(20.0, rgb_distance((255, 200, 100), (255, 180, 100)), rel_tol=1e-3))
    def test_case_19(self): self.assertTrue(isclose(141.421, rgb_distance((0, 0, 0), (100, 100, 0)), rel_tol=1e-3))
    def test_case_20(self): self.assertTrue(isclose(139.282, rgb_distance((10, 20, 30), (100, 100, 100)), rel_tol=1e-3))

    def test_case_21(self): self.assertTrue(isclose(50.0, rgb_distance((120, 200, 90), (120, 200, 140)), rel_tol=1e-3))
    def test_case_22(self): self.assertTrue(isclose(51.9615, rgb_distance((130, 130, 130), (100, 100, 100)), rel_tol=1e-3))
    def test_case_23(self): self.assertTrue(isclose(50.0, rgb_distance((30, 60, 90), (80, 60, 90)), rel_tol=1e-3))
    def test_case_24(self): self.assertTrue(isclose(34.641, rgb_distance((0, 0, 0), (20, 20, 20)), rel_tol=1e-3))
    def test_case_25(self): self.assertTrue(isclose(77.928, rgb_distance((5, 5, 5), (50, 50, 50)), rel_tol=1e-3))

    def test_case_26(self): self.assertTrue(isclose(14.1421, rgb_distance((200, 200, 200), (210, 210, 200)), rel_tol=1e-3))
    def test_case_27(self): self.assertTrue(isclose(0.0, rgb_distance((123, 45, 67), (123, 45, 67))))
    def test_case_28(self): self.assertTrue(isclose(208.378, rgb_distance((0, 0, 255), (90, 90, 90)), rel_tol=1e-3))
    def test_case_29(self): self.assertTrue(isclose(330.739, rgb_distance((64, 64, 64), (255, 255, 255)), rel_tol=1e-3))
    def test_case_30(self): self.assertTrue(isclose(346.482, rgb_distance((10, 10, 10), (250, 250, 250)), rel_tol=1e-3))

    def test_case_31(self): self.assertTrue(isclose(232.379, rgb_distance((15, 100, 200), (250, 80, 90)), rel_tol=1e-3))
    def test_case_32(self): self.assertTrue(isclose(107.703, rgb_distance((20, 30, 40), (50, 100, 150)), rel_tol=1e-3))
    def test_case_33(self): self.assertTrue(isclose(173.205, rgb_distance((255, 0, 0), (0, 255, 0)), rel_tol=1e-3))
    def test_case_34(self): self.assertTrue(isclose(360.624, rgb_distance((10, 10, 10), (200, 200, 200)), rel_tol=1e-3))
    def test_case_35(self): self.assertTrue(isclose(255.0, rgb_distance((255, 0, 0), (0, 0, 255))))

    def test_case_36(self): self.assertTrue(isclose(212.132, rgb_distance((20, 40, 60), (160, 180, 200)), rel_tol=1e-3))
    def test_case_37(self): self.assertTrue(isclose(94.868, rgb_distance((255, 255, 255), (200, 200, 200)), rel_tol=1e-3))
    def test_case_38(self): self.assertTrue(isclose(0.0, rgb_distance((111, 222, 123), (111, 222, 123))))
    def test_case_39(self): self.assertTrue(isclose(123.693, rgb_distance((0, 0, 0), (50, 100, 50)), rel_tol=1e-3))
    def test_case_40(self): self.assertTrue(isclose(223.607, rgb_distance((10, 20, 30), (200, 200, 200)), rel_tol=1e-3))

    def test_case_41(self): self.assertTrue(isclose(60.8276, rgb_distance((30, 60, 90), (70, 90, 120)), rel_tol=1e-3))
    def test_case_42(self): self.assertTrue(isclose(79.0569, rgb_distance((123, 234, 111), (100, 200, 90)), rel_tol=1e-3))
    def test_case_43(self): self.assertTrue(isclose(23.2594, rgb_distance((60, 60, 60), (50, 70, 50)), rel_tol=1e-3))
    def test_case_44(self): self.assertTrue(isclose(265.637, rgb_distance((0, 255, 0), (255, 0, 255)), rel_tol=1e-3))
    def test_case_45(self): self.assertTrue(isclose(104.403, rgb_distance((123, 123, 123), (200, 100, 50)), rel_tol=1e-3))

    def test_case_46(self): self.assertTrue(isclose(173.205, rgb_distance((0, 0, 255), (255, 0, 0)), rel_tol=1e-3))
    def test_case_47(self): self.assertTrue(isclose(83.666, rgb_distance((70, 80, 90), (100, 110, 130)), rel_tol=1e-3))
    def test_case_48(self): self.assertTrue(isclose(63.2456, rgb_distance((10, 20, 30), (20, 40, 60)), rel_tol=1e-3))
    def test_case_49(self): self.assertTrue(isclose(100.0, rgb_distance((100, 100, 100), (200, 100, 100))))
    def test_case_50(self): self.assertTrue(isclose(216.334, rgb_distance((45, 89, 123), (200, 150, 250)), rel_tol=1e-3))
