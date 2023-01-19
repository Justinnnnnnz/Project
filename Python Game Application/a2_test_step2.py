import unittest
from block import random as a2_random
from block import *
from blocky import _block_to_squares
from game import *
from player import *
from a2_test import A2Test, block_bfs
SEED_NUMBER = 1214


class A2TestStep2(A2Test):
    """
    We can choose to override any existing methods we have defined in the A2Test to make our life easier
    """

    def setUp(self) -> None:
        random.seed(SEED_NUMBER)
        a2_random.seed(SEED_NUMBER)
        super().setUp()

    def tearDown(self) -> None:
        random.seed(SEED_NUMBER)
        a2_random.seed(SEED_NUMBER)
        super().tearDown()

    def test_get_block_1(self):
        """
        Test for a single block
                root((10, 10), 10, (10, 10, 10), 0, 0, [])
        Expected Return Value [((10, 10, 10), (10, 10), 10)]
        """
        leaf_block = self.leaf_block
        exp_list = [getattr(leaf_block, attr_name) for attr_name in self.block_attrs]
        exp_list[-1] = 0
        act = _block_to_squares(leaf_block)
        self.assertTrue(isinstance(act, list))
        self.assertTrue(len(act) == 1)
        self.assertEqual([((10, 10, 10), (10, 10), 10)], act)
        self.assertBlock(leaf_block, exp_list, color_check=True, is_leaf=True)

    def test_get_block_2(self):
        """
        Test for a nested Block
            Level 0: root([i1, l1, l2, l3])
            /               |               |               \
        Level1: i1([l4, l5, l6, l7]), l1([]), l2([]), l3([]))
            /                                       |                           |                               \
        Level2: l4([]), l5([]), l6 ([]), l7([])

        root: (0, 0), 100, None, 0, 2
        i1:(50, 0), 50, None, 1, 2
        l1:(0, 0), 50, (80, 80, 80), 1, 2
        l2:(0, 50), 50, (70, 70, 70), 1, 2
        l3:(50, 50), 50, (60, 60, 60), 1, 2
        l4:(75, 0), 25, (40, 40, 40), 2, 2
        l5:(50, 0), 25, (30, 30, 30), 2, 2
        l6:(50, 25), 25, (20, 20, 20), 2, 2
        l7:(75, 25), 25, (10, 10, 10),2, 2

        Expected return value:
        [((10, 10, 10), (75, 25), 25),
        ((20, 20, 20), (50, 25), 25),
        ((30, 30, 30), (50, 0), 25),
        ((40, 40, 40), (75, 0), 25),
        ((80, 80, 80), (0, 0), 50),
        ((70, 70, 70), (0, 50), 50),
        ((60, 60, 60), (50, 50), 50)]
        """
        act1 = _block_to_squares(self.one_internal.children[0])
        exp1 = [((10, 10, 10), (75, 25), 25),
                               ((20, 20, 20), (50, 25), 25),
                               ((30, 30, 30), (50, 0), 25),
                               ((40, 40, 40), (75, 0), 25)]
        self.assertCountEqual(exp1, act1)
        act2 = _block_to_squares(self.one_internal)
        exp2 = exp1 + [((80, 80, 80), (0, 0), 50),
                       ((70, 70, 70), (0, 50), 50),
                       ((60, 60, 60), (50, 50), 50)]
        self.assertCountEqual(exp2, act2)

    def test_smash_1(self):
        self.assertFalse(self.leaf_block.smash())
        self.assertFalse(all(leaf.smash() for leaf in self.one_internal.children[0].children))

    def test_smash_2(self):
        """
        Before:
            Level 0: root([i1, l1, l2, l3])
            /               |               |               \
        Level1: i1([l4, l5, l6, l7]), l1([]), l2([]), l3([]))
            /                                       |                           |                               \
        Level2: l4([]), l5([]), l6 ([]), l7([])

        root: (0, 0), 100, None, 0, 2
        i1:(50, 0), 50, None, 1, 2
        l1:(0, 0), 50, (80, 80, 80), 1, 2
        l2:(0, 50), 50, (70, 70, 70), 1, 2
        l3:(50, 50), 50, (60, 60, 60), 1, 2
        l4:(75, 0), 25, (40, 40, 40), 2, 2
        l5:(50, 0), 25, (30, 30, 30), 2, 2
        l6:(50, 25), 25, (20, 20, 20), 2, 2
        l7:(75, 25), 25, (10, 10, 10),2, 2
        After:
            Level 0: root([i1, l1, l2, l3])
            /               |               |               \
        Level1: i1([l4, l5, l6, l7]), l1([l8, l9, l10, l11]), l2([]), l3([]))
            /                                       |                           |                               \
        Level2: l4([]), l5([]), l6 ([]), l7([])     l8([]), l9([]), i10([]), l11([])

        root: (0, 0), 100, None, 0, 2
        i1:(50, 0), 50, None, 1, 2
        l1:(0, 0), 50, (80, 80, 80), 1, 2
        l2:(0, 50), 50, (70, 70, 70), 1, 2
        l3:(50, 50), 50, (60, 60, 60), 1, 2
        l4:(75, 0), 25, (40, 40, 40), 2, 2
        l5:(50, 0), 25, (30, 30, 30), 2, 2
        l6:(50, 25), 25, (20, 20, 20), 2, 2
        l7:(75, 25), 25, (10, 10, 10),2, 2
        l8:(25, 0), 25, XXX, 2, 2
        l9: (0, 0), 25, XXX, 2, 2
        l10: (0, 25), 25, XXX, 2, 2
        l11: (25, 25), 25, XXX, 2, 2
        """
        temp = self.one_internal.children[1]
        temp.smash()
        self.assertBlock(temp, [(0, 0), 50, None, 1, 2, 4], is_leaf=False)
        self.assertBlock(temp.children[0], [(25, 0), 25, COLOUR_LIST, 2, 2, 0], color_check=False, is_leaf=True)
        self.assertBlock(temp.children[1], [(0, 0), 25, COLOUR_LIST, 2, 2, 0], color_check=False, is_leaf=True)
        self.assertBlock(temp.children[2], [(0, 25), 25, COLOUR_LIST, 2, 2, 0], color_check=False, is_leaf=True)
        self.assertBlock(temp.children[3], [(25, 25), 25, COLOUR_LIST, 2, 2, 0], color_check=False, is_leaf=True)

    def test_smash_3(self):
        """
        Before:
                Level 0: root([])
        After:
            Level 0: root([i1, l1, l2, l3])
                    /               |               |               \
            Level1: i1([l5, l6, l7, l8]), i2([l9, l10, l11, l12]), i3([l13, l14, l15, l16]), i4([l17, l18, l19, l20]))
                    /                                       |                                   |                               \
            Level2: l5([]), l6([]), l7([]), l8([])        l9([]),l10([]), l11([]), l12([])      l13([]), l14([]), l15([]), l16)([]).    l17([]), l18([]), l19([]), l20([])                                  l9                              l10, l11
        root:(0, 0), 100, None, 0, 2
        i1:(50, 0), 50, None, 1, 2
        i2:(0, 0), 50, None, 1, 2
        i3:(0, 50), 50, None, 1, 2
        i4:(50, 50), 50, None, 1, 2
        l5:(75, 0), 25, XXX, 2, 2
        l6:(50, 0), 25, XXX, 2, 2
        l7:(50, 25), 25, XXX, 2, 2
        l8:(75, 25), 25, XXX, 2, 2
        l9:(25, 0), 25, XXX, 2, 2
        l10:(0, 0), 25, XXX, 2, 2
        l11:(0, 25), 25, XXX, 2, 2
        l12:(25, 25), 25, XXX, 2, 2
        l13:(25, 50), 25, XXX, 2, 2
        l14:(0, 50), 25, XXX, 2, 2
        l15:(0, 75), 25, XXX, 2, 2
        l16:(25, 75), 25, XXX, 2, 2
        l17:(75, 50), 25, XXX, 2, 2
        l18:(50, 50), 25, XXX, 2, 2
        l19:(50, 75), 25, XXX, 2, 2
        l20:(75, 75), 25, XXX, 2, 2
        """
        temp = Block((0, 0), 100, None, 0, 2)
        self.assertTrue(temp.smash())
        bfs = block_bfs(temp)
        self.assertTrue(len(bfs) == 21, "You should have exactly 21 nodes after smashing")
        check_color = True
        is_leaf = True
        parameter_list = [[[(0, 0), 100, None, 0, 2, 4], not check_color, not is_leaf],
                          [[(50, 0), 50, None, 1, 2, 4], not check_color, not is_leaf],
                          [[(0, 0), 50, None, 1, 2, 4], not check_color, not is_leaf],
                          [[(0, 50), 50, None, 1, 2, 4], not check_color, not is_leaf],
                          [[(50, 50), 50, None, 1, 2, 4], not check_color, not is_leaf],
                          [[(75, 0), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(50, 0), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(50, 25), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(75, 25), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(25, 0), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(0, 0), 25, COLOUR_LIST, 2, 2, 0], not check_color,  is_leaf],
                          [[(0, 25), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(25, 25), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(25, 50), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(0, 50), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(0, 75), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(25, 75), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(75, 50), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(50, 50), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(50, 75), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf],
                          [[(75, 75), 25, COLOUR_LIST, 2, 2, 0], not check_color, is_leaf]
                          ]
        for i in range(len(bfs)):
            block = bfs[i]
            parameters = parameter_list[i]
            self.assertBlock(block, parameters[0], parameters[1], parameters[2])

        for j in range(5, 21):
            block = bfs[j]
            block.colour = (j * 10, j * 10, j * 10)
        squares = _block_to_squares(temp)
        squares.sort(key=lambda x: x[0][0])
        exp_squares = [((50, 50, 50), (75, 0), 25), ((60, 60, 60), (50, 0), 25), ((70, 70, 70), (50, 25), 25),
         ((80, 80, 80), (75, 25), 25), ((90, 90, 90), (25, 0), 25), ((100, 100, 100), (0, 0), 25),
         ((110, 110, 110), (0, 25), 25), ((120, 120, 120), (25, 25), 25), ((130, 130, 130), (25, 50), 25),
         ((140, 140, 140), (0, 50), 25), ((150, 150, 150), (0, 75), 25), ((160, 160, 160), (25, 75), 25),
         ((170, 170, 170), (75, 50), 25), ((180, 180, 180), (50, 50), 25), ((190, 190, 190), (50, 75), 25),
         ((200, 200, 200), (75, 75), 25)]
        self.assertCountEqual(squares, exp_squares)

if __name__ == "__main__":
    unittest.main(exit=False)