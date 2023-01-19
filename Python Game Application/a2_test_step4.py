from a2_test import A2Test
import unittest
from player import _get_block


class A2TestStep4(A2Test):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_get_block_1(self):
        """
    (10, 10)        (19, 10)
        ____________
        |           |
        |           |
        |___________|
    (10, 19)        (19, 19)
        """
        block = self.leaf_block
        corners = [(10, 10), (19, 10), (10, 19), (19, 19)]
        for corner in corners:
            act = _get_block(block, corner, 0)
            self.assertBlock(act, [(10, 10), 10, (10, 10, 10), 0, 0, 0], True, True)
        outbounds = [9, 20, 20, 100]
        for outbound in outbounds:
            for i in range(100):
                act = _get_block(block, (outbound, i), 0)
                self.assertIsNone(act, "The coordinates are out of bound you should return None")

    def test_get_block_2(self):
        """
        (0, 0)      (50, 0) (75, 0) (99, 0)
            ___________________________
            |            |      |      |
            |    (50, 25)|______|______| (99, 25)
            |            |      |      |
  (0, 50)   |____________|______|______| (99, 50)
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________| (99, 99)
        """
        for i in range(50):
            for j in range(50):
                temp = _get_block(self.one_internal, (i, j), 1)
                self.assertBlock(temp, [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        for i in range(50, 100):
            for j in range(0, 50):
                temp = _get_block(self.one_internal, (i, j), 1)
                self.assertBlock(temp, [(50, 0), 50, None, 1, 2, 4], False, False)
        for i in range(50):
            for j in range(50, 100):
                temp = _get_block(self.one_internal, (i, j), 1)
                self.assertBlock(temp, [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        for i in range(50, 100):
            for j in range(50, 100):
                temp = _get_block(self.one_internal, (i, j), 1)
                self.assertBlock(temp, [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)

    def test_get_block_3(self):
        """
        (0, 0)      (50, 0) (75, 0) (99, 0)
            ___________________________
            |            |      |      |
            |    (50, 25)|______|______| (99, 25)
            |            |      |      |
  (0, 50)   |____________|______|______| (99, 50)
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________| (99, 99)
        """
        act = _get_block(self.one_internal, (50, 0), 0)
        self.assertBlock(act, [(0, 0), 100, None, 0, 2, 4], False, False)
        act1 = _get_block(self.one_internal, (50, 0), 1)
        self.assertBlock(act1, [(50, 0), 50, None, 1, 2, 4], False, False)
        act2 = _get_block(self.one_internal, (49, 0), 1)
        self.assertBlock(act2, [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        act3 = _get_block(self.one_internal, (49, 50), 1)
        self.assertBlock(act3, [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        act4 = _get_block(self.one_internal, (50, 50), 1)
        self.assertBlock(act4, [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        act5 = _get_block(self.one_internal, (75, 0), 2)
        self.assertBlock(act5, [(75, 0), 25, (40, 40, 40), 2, 2, 0], True, True)
        act6 = _get_block(self.one_internal, (75, 25), 2)
        self.assertBlock(act6, [(75, 25), 25, (10, 10, 10), 2, 2, 0], True, True)
        act7 = _get_block(self.one_internal, (99, 25), 2)
        self.assertBlock(act7, [(75, 25), 25, (10, 10, 10), 2, 2, 0], True, True)
        act8 = _get_block(self.one_internal, (74, 25), 2)
        self.assertBlock(act8, [(50, 25), 25, (20, 20, 20), 2, 2, 0], True, True)
        act9 = _get_block(self.one_internal, (50, 0), 2)
        self.assertBlock(act9, [(50, 0), 25, (30, 30, 30), 2, 2, 0], True, True)
        act10 = _get_block(self.one_internal, (50, 50), 2)
        self.assertBlock(act10, [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        act11 = _get_block(self.one_internal, (75, 25), 1)
        self.assertBlock(act11, [(50, 0), 50, None, 1, 2, 4], False, False)


if __name__ == "__main__":
    unittest.main(exit=False)