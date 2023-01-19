import unittest

from a2_test import A2Test, block_bfs


class A2TestStep5(A2Test):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()


class TestRotate(A2TestStep5):
    def test_rotate_1(self) -> None:
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        Expected Return Value: False
        """
        for i in range(100):
            direction = lambda: 1 if i % 2 == 0 else 3
            res = self.leaf_block.rotate(direction())
            self.assertFalse(res)
            self.assertBlock(self.leaf_block, [(10, 10), 10, (10, 10, 10), 0, 0, 0], True, True)

    def test_rotate_2(self):
        """
        Before:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
        (0, 0, (40， 40， 40))          (5, 0， (30, 30, 30))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
        (0, 5, (50, 50, 50))           (5, 5, (20, 20, 20))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        direction = 1
        res = self.one_level.rotate(direction)
        self.assertTrue(res, "Rotate can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (20, 20, 20), 1, 1, 0], True, True)

    def test_rotate_3(self):
        """
        Before:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
                After:
            (0, 0, (20， 20， 20))          (5, 0， (50, 50, 50))
                         ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
        (0, 5, (30, 30, 30))           (5, 5, (40, 40, 40))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """

        direction = 3
        res = self.one_level.rotate(direction)
        self.assertTrue(res, "Rotate can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (40, 40, 40), 1, 1, 0], True, True)

    def test_rotate_4(self):
        """
        Before:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
            (0, 0, (30， 30， 30))          (5, 0， (20, 20, 20))
                         ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
        (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        direction = 1
        self.one_level.rotate(direction)
        res = self.one_level.rotate(3)
        self.assertTrue(res, "Rotate can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (50, 50, 50), 1, 1, 0], True, True)

    def test_rotate_5(self):
        """
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
        Before:
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 50, (60, 60, 60))
        After:
            E_____________C_____B______
            |            |      |      |
            |            D______A______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 25, (40, 40, 40))
            B:(75, 0, (30, 30, 30))
            C:(50, 0, (20, 20, 20))
            D:(50, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        direction = 1
        res = self.one_internal.children[0].rotate(direction)
        self.assertTrue(res, "Rotation can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[0], [(75, 0), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[1], [(50, 0), 25, (20, 20, 20), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[2], [(50, 25), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[3], [(75, 25), 25, (40, 40, 40), 2, 2, 0], True, True)

    def test_rotate_6(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 50, (60, 60, 60))
        After:
            E____________A_____D_______
            |            |      |      |
            |            B______C______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(50, 0, (40, 40, 40))
            B:(50, 25, (30, 30, 30))
            C:(75, 25, (20, 20, 20))
            D:(75, 0, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        direction = 3
        res = self.one_internal.children[0].rotate(direction)
        self.assertTrue(res, "Rotation can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[0], [(75, 0), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[1], [(50, 0), 25, (40, 40, 40), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[2], [(50, 25), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[3], [(75, 25), 25, (20, 20, 20), 2, 2, 0], True, True)

    def test_rotate_7(self):
        """
        Before:
            E____________B_____A_______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 50, (60, 60, 60))
        After:
            F____________E____________
            |            |            |
            |            |            |
            |            |            |
            |            |            |
            G____________C______B_____
            |            |      |     |
            |            D______A_____|
            |            |      |     |
            |____________|______|_____|
            A:(75, 75, (40, 40, 40))
            B:(75, 50, (30, 30, 30))
            C:(50, 50, (20, 20, 20))
            D:(50, 75, (10, 10, 10)
            E:(50, 0, (80, 80, 80))
            F:(0, 0, (70, 70, 70))
            G:(0, 50, (60, 60, 60))
        """
        direction = 1
        res = self.one_internal.rotate(direction)
        self.assertTrue(res, "Rotation can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[3].children[0], [(75, 50), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[1], [(50, 50), 25, (20, 20, 20), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[2], [(50, 75), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[3], [(75, 75), 25, (40, 40, 40), 2, 2, 0], True, True)

    def test_rotate_8(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 50, (60, 60, 60))
        After:
            A______D_____G______________
            |      |     |              |
            B______C_____|              |
            |      |     |              |
          E |______|_____F______________|
            |            |              |
            |            |              |
            |            |              |
            |____________|______________|
        A:(0, 0, (40, 40, 40))
        B:(0, 25, (30, 30, 30))
        C:(25, 25, (20, 20, 20))
        D:(25, 0, (10, 10, 10))
        E:(0, 50, (80, 80, 80))
        F:(50, 50, (70, 70, 70))
        G:(50, 0, (60, 60, 60))
        """
        direction = 3
        res = self.one_internal.rotate(direction)
        self.assertTrue(res, "Rotation can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[0], [(25, 0), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[1], [(0, 0), 25, (40, 40, 40), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[2], [(0, 25), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[3], [(25, 25), 25, (20, 20, 20), 2, 2, 0], True, True)


class TestSwap(A2Test):
    def test_swap_1(self):
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        Expected Return Value: False
        """
        for i in range(100):
            direction = lambda: 0 if i % 2 == 0 else 1
            res = self.leaf_block.swap(direction())
            self.assertFalse(res)
            self.assertBlock(self.leaf_block, [(10, 10), 10, (10, 10, 10), 0, 0, 0], True, True)

    def test_swap_2(self):
        """
        Before:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
        (0, 0, (40， 40， 40))          (5, 0， (50, 50, 50))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
        (0, 5, (30, 30, 30))           (5, 5, (20, 20, 20))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        direction = 1
        res = self.one_level.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (20, 20, 20), 1, 1, 0], True, True)

    def test_swap_3(self):
        """
        Before:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
        (0, 0, (20， 20， 20))          (5, 0， (30, 30, 30))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
        (0, 5, (50, 50, 50))           (5, 5, (40, 40, 40))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        direction = 0
        res = self.one_level.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (40, 40, 40), 1, 1, 0], True, True)

    def test_swap_4(self):
        """
        Before:
            (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
            (0, 0, (50， 50， 50))      (5, 0， (40, 40, 40))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (20, 20, 20))           (5, 5, (30, 30, 30))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        direction = 0
        res = self.one_level.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        direction = 1
        res = self.one_level.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (30, 30, 30), 1, 1, 0], True, True)

    def test_swap_5(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 50, (60, 60, 60))
        After:
            E_____________C_____D______
            |            |      |      |
            |            B _____A______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 0, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        direction = 1
        res = self.one_internal.children[0].swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[0], [(75, 0), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[1], [(50, 0), 25, (20, 20, 20), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[2], [(50, 25), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[3], [(75, 25), 25, (40, 40, 40), 2, 2, 0], True, True)

    def test_swap_6(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        After:
            E_____________A_____B______
            |            |      |      |
            |            D _____C______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(50, 0, (40, 40, 40))
            B:(75, 0, (30, 30, 30))
            C:(75, 25, (20, 20, 20))
            D:(50, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        direction = 0
        res = self.one_internal.children[0].swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[0], [(75, 0), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[1], [(50, 0), 25, (40, 40, 40), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[2], [(50, 25), 25, (10, 10, 10), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[0].children[3], [(75, 25), 25, (20, 20, 20), 2, 2, 0], True, True)

    def test_swap_7(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        After:
            F____________G_____________
            |            |             |
            |            |             |
            |            |             |
            E____________B______A______|
            |            |      |      |
            |            C______D______|
            |            |      |      |
            |____________|______|______|
            A:(75, 50, (40, 40, 40))
            B:(50, 50, (30, 30, 30))
            C:(50, 75, (20, 20, 20))
            D:(75, 75, (10, 10, 10))
            E:(0, 50, (80, 80, 80))
            F:(0, 0, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        direction = 1
        res = self.one_internal.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[3].children[0], [(75, 50), 25, (40, 40, 40), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[1], [(50, 50), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[2], [(50, 75), 25, (20, 20, 20), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3].children[3], [(75, 75), 25, (10, 10, 10), 2, 2, 0], True, True)

    def test_swap_8(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        After:
            B_____A_____E____________
            |     |     |            |
            C_____D_____|            |
            |     |     |            |
            G_____|_____F____________|
            |           |            |
            |           |            |
            |           |            |
            |___________|____________|
            A:(25, 0, (40, 40, 40))
            B:(0, 0, (30, 30, 30))
            C:(0, 25, (20, 20, 20))
            D:(25, 25, (10, 10, 10))
            E:(50, 0, (80, 80, 80))
            F:(50, 50, (70, 70, 70))
            G:(0, 50, (60, 60, 60))
        """
        direction = 0
        res = self.one_internal.swap(direction)
        self.assertTrue(res, "Swap can be successfully performed")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, None, 1, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[0], [(25, 0), 25, (40, 40, 40), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[1], [(0, 0), 25, (30, 30, 30), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[2], [(0, 25), 25, (20, 20, 20), 2, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1].children[3], [(25, 25), 25, (10, 10, 10), 2, 2, 0], True, True)


class TestPaint(A2Test):
    def test_paint_1(self):
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        Expected Value = True
        """
        res = self.leaf_block.paint((0, 0, 0))
        self.assertTrue(res, "Paint should be successfully performed")
        res = self.leaf_block.paint((0, 0, 0))
        self.assertFalse(res, "You should not paint with the same color of the block")
        self.assertBlock(self.leaf_block, [(10, 10), 10, (0, 0, 0), 0, 0, 0], True, True)

    def test_paint_2(self):
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        Expected Value = False
        """
        self.leaf_block.max_depth = 1
        res = self.leaf_block.paint((0, 0, 0))
        self.assertFalse(res, "You should not paint a block which is not in the level of max_depth")
        self.assertBlock(self.leaf_block, [(10, 10), 10, (10, 10, 10), 0, 1, 0], True, True)

    def test_paint_3(self):
        """
        (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        self.one_level.max_depth = 2
        for child in self.one_level.children:
            child.max_depth = 2
        res = [child.paint((i, i, i))for i in range(100) for child in self.one_internal.children]
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (20, 20, 20), 1, 2, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (30, 30, 30), 1, 2, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (40, 40, 40), 1, 2, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (50, 50, 50), 1, 2, 0], True, True)
        self.assertFalse(any(res), "You should not paint a block which is not in the level of max_depth")

    def test_paint_4(self):
        """
        (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        for i in range(100):
            for j in range(4):
                child = self.one_level.children[j]
                res = child.paint((i, i, i))
                self.assertTrue(res)
                positions = [(5, 0), (0, 0), (0, 5), (5, 5)]
                self.assertBlock(child, [positions[j], 5, (i, i, i), 1, 1, 0], True, True)

    def test_paint_5(self):
        """
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        for i in range(100):
            for j in range(1, 4):
                child = self.one_internal.children[0].children[j]
                res = child.paint((i, i, i))
                self.assertTrue(res)
                positions = [(75, 0), (50, 0), (50, 25), (75, 25)]
                self.assertBlock(child, [positions[j], 25, (i, i, i), 2, 2, 0], True, True)
                self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
                self.assertBlock(self.one_internal.children[0], [(50, 0), 50, None, 1, 2, 4], True, False)
                self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
                self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
                self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)


class TestCombine(A2Test):
    def test_combine_1(self):
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        """
        res = self.leaf_block.combine()
        self.assertFalse(res, "You cannot combine a leaf")
        self.assertBlock(self.leaf_block, [(10, 10), 10, (10, 10, 10), 0, 0, 0], True, True)

    def test_combine_2(self):
        """
        Case1:
                (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        Case2:
            (0, 0, (20， 20， 20))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (40, 40, 40))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        """
        res = self.one_level.combine()
        self.assertFalse(res, "You cannot combine a internal without the majority color")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (30, 30, 30), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (50, 50, 50), 1, 1, 0], True, True)
        self.one_level.children[1].colour = (20, 20, 20)
        self.one_level.children[3].colour = (40, 40, 40)
        res = self.one_level.combine()
        self.assertFalse(res, "You cannot combine a internal without the majority color")
        self.assertBlock(self.one_level, [(0, 0), 10, None, 0, 1, 4], True, False)
        self.assertBlock(self.one_level.children[0], [(5, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[1], [(0, 0), 5, (20, 20, 20), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[2], [(0, 5), 5, (40, 40, 40), 1, 1, 0], True, True)
        self.assertBlock(self.one_level.children[3], [(5, 5), 5, (40, 40, 40), 1, 1, 0], True, True)

    def test_combine_3(self):
        """
        Before:
        (0, 0, (30， 30， 30))      (5, 0， (20, 20, 20))
                        ___________________________
                        |            |             |
                        |            |             |
                        |            |             |
            (0, 5, (40, 40, 40))           (5, 5, (50, 50, 50))
                        |____________|____________ |
                        |            |             |
                        |            |             |
                        |            |             |
                        |____________|_____________|
        After:
        ____________________________
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |                           |
        |___________________________|
        """
        self.one_level.children[3].colour = (20, 20, 20)
        res = self.one_level.combine()
        self.assertTrue(res, "You can combine the internal in the level of max depth - 1 with a majority color")
        self.assertBlock(self.one_level, [(0, 0), 10, (20, 20, 20), 0, 1, 0], True, True)

    def test_combine_4(self):
        """
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (40, 40, 40))
            B:(50, 0, (30, 30, 30))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        temp = [self.one_internal]
        while len(temp) != 0:
            block = temp.pop(0)
            block_position = block.position
            block_size = block.size
            block_colour = block.colour
            block_level = block.level
            block_depth = block.max_depth
            block_child = len(block.children)
            is_leaf = block_child == 0
            res = block.combine()
            self.assertFalse(res)
            self.assertBlock(block, [block_position, block_size, block_colour, block_level, block_depth, block_child], True, is_leaf)
            for child in block.children:
                temp.append(child)

    def test_combine_5(self):
        """
        Before:
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |      |      |
            F___________G|______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (60, 60, 60))
            B:(50, 0, (60, 60, 60))
            C:(50, 25, (20, 20, 20))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        After:
             E___________A______________
            |            |             |
            |            |             |
            |            |             |
            |            |             |
            F____________G|____________|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
        A:(50, 0, (60, 60, 60))
        E:(0, 0, (80, 80, 80))
        F:(0, 50, (70, 70, 70))
        G:(50, 0, (60, 60, 60))
        """
        self.one_internal.children[0].children[0].colour = (60, 60, 60)
        self.one_internal.children[0].children[1].colour = (60, 60, 60)
        res = self.one_internal.children[0].combine()
        self.assertTrue(res, "You should be able to combine the node in the level of max depth -1 with a majority colour")
        self.assertBlock(self.one_internal, [(0, 0), 100, None, 0, 2, 4], True, False)
        self.assertBlock(self.one_internal.children[0], [(50, 0), 50, (60, 60, 60), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[1], [(0, 0), 50, (80, 80, 80), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[2], [(0, 50), 50, (70, 70, 70), 1, 2, 0], True, True)
        self.assertBlock(self.one_internal.children[3], [(50, 50), 50, (60, 60, 60), 1, 2, 0], True, True)
        temp = [self.one_internal]
        while len(temp) != 0:
            block = temp.pop(0)
            block_position = block.position
            block_size = block.size
            block_colour = block.colour
            block_level = block.level
            block_depth = block.max_depth
            block_child = len(block.children)
            is_leaf = block_child == 0
            res = block.combine()
            self.assertFalse(res)
            self.assertBlock(block, [block_position, block_size, block_colour, block_level, block_depth, block_child],
                             True, is_leaf)
            for child in block.children:
                temp.append(child)
        self.one_internal.max_depth = 1
        for child in self.one_internal.children:
            child.max_depth = 1
        res = self.one_internal.combine()
        self.assertTrue(res)
        self.assertBlock(self.one_internal, [(0, 0), 100, (60, 60, 60), 0, 1, 0], True, True)


if __name__ == "__main__":
    unittest.main(exit=False)
