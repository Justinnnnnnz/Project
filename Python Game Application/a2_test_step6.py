import unittest

from a2_test import A2Test
from goal import _flatten, PerimeterGoal


class A2TestStep6(A2Test):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()


class TestFlatten(A2TestStep6):
    def test_flatten_1(self):
        """
        (10, 10)        (19, 10)
            ____________
            |           |
            |           |
            |___________|
        (10, 19)        (19, 19)
        Expected Return Value
        [[(10, 10, 10)] * 2^{max depth}] * 2 ^ {max depth})
        """
        res = _flatten(self.leaf_block)
        self.assertEqual(res, [[(10, 10, 10)]])
        for i in range(1, 10):
            self.leaf_block.max_depth = i
            res = _flatten(self.leaf_block)
            self.assertEqual([[(10, 10, 10)] * pow(2, i)] * pow(2, i), res)

        self.one_level.max_depth = 2

    def test_flatten_2(self):
        """
        Case 1:
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
        Expected Return Value
        [[(30, 30, 30), (40, 40, 40)],
        [(20, 20, 20), (50, 50, 50)]]
        """
        res = _flatten(self.one_level)
        self.assertEqual([[(30, 30, 30), (40, 40, 40)],
                               [(20, 20, 20), (50, 50, 50)]], res)

    def test_flatten_3(self):
        """
                        A_____B______C_______D______
                        |     |      |       |      |
                        E_____F______G_______H______|
                        |     |      |       |      |
                        I_____J______K_______L______|
                        |     |      |       |      |
                        M_____N______O_______P______|
                        |     |      |       |      |
                        |_____|______|_______|______|
        A:(30, 30, 30)
        B:(30, 30, 30)
        C:(20, 20, 20)
        D:(20, 20, 20)
        E:(30, 30, 30)
        F:(30, 30, 30)
        G:(20, 20, 20)
        H:(20, 20, 20)
        I:(40, 40, 40)
        J:(40, 40, 40)
        K:(50, 50, 50)
        L:(50, 50, 50)
        M:(40, 40, 40)
        N:(40, 40, 40)
        O:(50, 50, 50)
        P:(50, 50, 50)
        Expected Return Value:
        [[(30, 30, 30), (30, 30, 30), (40, 40, 40), (40, 40, 40)],
        [(30, 30, 30), (30, 30, 30), (40, 40, 40), (40, 40, 40)],
        [(20, 20, 20), (20, 20, 20), (50, 50, 50), (50, 50, 50)],
        [(20, 20, 20), (20, 20, 20), (50, 50, 50), (50, 50, 50)]]
        """
        self.one_level.max_depth = 2
        for child in self.one_level.children:
            child.max_depth = 2
        res = _flatten(self.one_level)
        exp = [[(30, 30, 30), (30, 30, 30), (40, 40, 40), (40, 40, 40)],
                                [(30, 30, 30), (30, 30, 30), (40, 40, 40), (40, 40, 40)],
                                [(20, 20, 20), (20, 20, 20), (50, 50, 50), (50, 50, 50)],
                                [(20, 20, 20), (20, 20, 20), (50, 50, 50), (50, 50, 50)]]
        self.assertEqual(exp, res)

    def test_flatten_4(self):
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
        Expected Return Value
        [[(80, 80, 80), (80, 80, 80), (70, 70, 70), (70, 70, 70)],
        [(80, 80, 80), (80, 80, 80), (70, 70, 70), (70, 70, 70)],
        [(30, 30, 30), (20, 20, 20), (60, 60, 60), (60, 60, 60)],
        [(40, 40, 40), (10, 10, 10), (60, 60, 60), (60, 60, 60)]]
        """
        res = _flatten(self.one_internal)
        exp = [[(80, 80, 80), (80, 80, 80), (70, 70, 70), (70, 70, 70)],
                          [(80, 80, 80), (80, 80, 80), (70, 70, 70), (70, 70, 70)],
                          [(30, 30, 30), (20, 20, 20), (60, 60, 60), (60, 60, 60)],
                          [(40, 40, 40), (10, 10, 10), (60, 60, 60), (60, 60, 60)]]
        self.assertEqual(exp, res)

    def test_flatten_5(self):
        """
        Case 1:
            F______E_____B______A______
            |     |      |      |      |
            G_____H______C _____D______|
            |     |      |      |      |
            I_____|______J______|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
        A:(75, 0, (40, 40, 40))
        B:(50, 0, (30, 30, 30))
        C:(50, 25, (20, 20, 20))
        D:(75, 25, (10, 10, 10))
        E:(25, 0, (110, 110, 110))
        F:(0, 0, (120, 120, 120))
        G:(0, 25, (130, 130, 130))
        H:(25, 25, (140, 140, 140))
        I:(0, 50, (70, 70, 70))
        J:(50, 50, (60, 60, 60))
        """
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(110, 150, 10)])
        res = _flatten(self.one_internal)
        exp = [[(120, 120, 120), (130, 130, 130), (70, 70, 70), (70, 70, 70)],
               [(110, 110, 110), (140, 140, 140), (70, 70, 70), (70, 70, 70)],
               [(30, 30, 30), (20, 20, 20), (60, 60, 60), (60, 60, 60)],
               [(40, 40, 40), (10, 10, 10), (60, 60, 60), (60, 60, 60)]]
        self.assertEqual(exp, res)
        bfs = [self.one_internal]
        while len(bfs) != 0:
            child = bfs.pop(0)
            child.max_depth = 3
            for temp in child.children:
                bfs.append(temp)
        res2 = _flatten(self.one_internal)
        exp2 = [[(120, 120, 120), (120, 120, 120), (130, 130, 130), (130, 130, 130), (70, 70, 70), (70, 70, 70), (70, 70, 70), (70, 70, 70)],
                [(120, 120, 120), (120, 120, 120), (130, 130, 130), (130, 130, 130), (70, 70, 70), (70, 70, 70), (70, 70, 70), (70, 70, 70)],
                [(110, 110, 110), (110, 110, 110), (140, 140, 140), (140, 140, 140), (70, 70, 70), (70, 70, 70), (70, 70, 70), (70, 70, 70)],
                [(110, 110, 110), (110, 110, 110), (140, 140, 140), (140, 140, 140), (70, 70, 70), (70, 70, 70), (70, 70, 70), (70, 70, 70)],
                [(30, 30, 30), (30, 30, 30), (20, 20, 20), (20, 20, 20), (60, 60, 60), (60, 60, 60), (60, 60, 60), (60, 60, 60)],
                [(30, 30, 30), (30, 30, 30), (20, 20, 20), (20, 20, 20), (60, 60, 60), (60, 60, 60), (60, 60, 60), (60, 60, 60)],
                [(40, 40, 40), (40, 40, 40), (10, 10, 10), (10, 10, 10), (60, 60, 60), (60, 60, 60), (60, 60, 60), (60, 60, 60)],
                [(40, 40, 40), (40, 40, 40), (10, 10, 10), (10, 10, 10), (60, 60, 60), (60, 60, 60), (60, 60, 60), (60, 60, 60)]]
        self.assertEqual(exp2, res2)


class TestPerimeterGoal(A2TestStep6):
    def setUp(self) -> None:
        super().setUp()
        self.goal_colour = None
        self.goal = PerimeterGoal(self.goal_colour)
        self.set_colour = lambda colour: setattr(self.goal, "colour", colour)

    def tearDown(self) -> None:
        super().tearDown()
        self.goal_colour = None
        self.goal = PerimeterGoal(self.goal_colour)
        self.set_colour = lambda colour: setattr(self.goal, "colour", colour)

    def test_goal_1(self):
        """
             ____________
            |           |
            |           |
            |___________|
        colour:(10, 10, 10)
        """
        for i in range(100, 200):
            self.goal_colour = (i, i, i)
            self.goal.colour = self.goal_colour
            res = self.goal.score(self.leaf_block)
            self.assertEqual(0, res, "You shoud return 0 since the colour of the block is not equal to the colour of the parameter")

    def test_goal_2(self):
        """
            ____________
            |           |
            |           |
            |___________|
        colour:(10, 10, 10)
        Expected Return Value 4
        Piazza Id:1780
        """
        self.set_colour((10, 10, 10))
        res = self.goal.score(self.leaf_block)
        self.assertEqual(4, res, "You should return 4 since every corner is touched and every corner has the same colour of the target colour")

    def test_goal_3(self):
        """
            ____________
            |           |
            |           |
            |___________|
        colour:(10, 10, 10)
        """

        self.set_colour((10, 10, 10))
        exps = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        res = []
        for i in range(1, 10):
            self.leaf_block.max_depth = i
            res.append(self.goal.score(self.leaf_block))
        self.assertEqual(exps, res)

    def test_goal_4(self):
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
        corner_colours = [(i, i, i) for i in range(20, 60, 10)]
        for colour in corner_colours:
            self.set_colour(colour)
            res = self.goal.score(self.one_level)
            exp = 2
            self.assertEqual(exp, res, "Every corner count twice so you should return 2")
        self.set_colour((20, 20, 20))
        for i in range(4):
            self.one_level.children[i].colour = (20, 20, 20)
            res = self.goal.score(self.one_level)
            exp = 2 * (i + 1)
            self.assertEqual(exp, res, "You should accumulate the count of the corner")
        self.one_level.combine()
        res = self.goal.score(self.one_level)
        exp = 8
        self.assertEqual(exp, res)

    def test_goal_5(self):
        """
            E_____________B_____A______
            |            |      |      |
            |            C _____D______|
            |            |/ /  /|      |
            F___________G|/_/_/_|______|
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
        """
        self.set_colour((20, 20, 20))
        exp = 0
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "The block not in the outside of the board does not count to the score")

    def test_goal_6(self):
        """
            E____________B_____A______
            |/  /  /   / |/ / / |/ / / |
            |/  /  /   / C/ /_/_D______|
            |/  /  /  /  |/ / / |      |
            F/__/__/__/__G/_/_/_|______|
            |            |             |
            |            |             |
            |            |             |
            |____________|_____________|
            A:(75, 0, (80, 80, 80))
            B:(50, 0, (80, 80, 80))
            C:(50, 25, (80, 80, 80))
            D:(75, 25, (10, 10, 10))
            E:(0, 0, (80, 80, 80))
            F:(0, 50, (70, 70, 70))
            G:(50, 0, (60, 60, 60))
        """
        self.set_colour((80, 80, 80))
        for i in range(3):
            self.one_internal.children[0].children[i].colour = (80, 80, 80)
        res = self.goal.score(self.one_internal)
        exp = 7
        self.assertEqual(exp, res, "score of E = 4, B = 1, A = 2")

    def test_goal_7(self):
        """
                        F_____E______B_______A______
                        |     |      |       |      |
                        G_____H______C_______D______|
                        |     |/ / / |/ / / /|      |
                        J_____I/_/_/_N/__/__/M______|
                        |     |/ / / |/ / /  |      |
                        K_____L/_/_/_O/_/_/__P______|
                        |     |      |       |      |
                        |_____|______|_______|______|
        A:(40, 40, 40)
        B:(30, 30, 30)
        C:(20, 20, 20)
        D:(10, 10, 10)
        E:(50, 50, 50)
        F:(40, 40, 40)
        G:(30, 30, 30)
        H:(20, 20, 20)
        I:(20, 20, 20)
        J:(30, 30, 30)
        K:(40, 40, 40)
        L:(50, 50, 50)
        M:(10, 10, 10)
        N:(20, 20, 20)
        O:(30, 30, 30)
        P:(40, 40, 40)
        """
        self.set_colour((20, 20, 20))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(50, 10, -10)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(20, 60, 10)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(10, 50, 10)])
        exp = 0
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "The blocks not in the outside of the board does not count")

    def test_goal_8(self):
        """
                        F_____E______B_______A______
                        |     |      |/ / / /|      |
                        G_____H______C_______D______|
                        |     |/ / / |       |      |
                        J_____I/_/_/_N_______M______|
                        |     |      |/ / /  |      |
                        K_____L______O/_/_/__P______|
                        |     |/ / / |       |      |
                        |_____|/_/_/_|_______|______|
        A:(40, 40, 40)
        B:(30, 30, 30)
        C:(20, 20, 20)
        D:(10, 10, 10)
        E:(60, 60, 60)
        F:(50, 50, 50)
        G:(40, 40, 40)
        H:(30, 30, 30)
        I:(60, 60, 60)
        J:(50, 50, 50)
        K:(40, 40, 40)
        L:(30, 30, 30)
        M:(40, 40, 40)
        N:(30, 30, 30)
        O:(20, 20, 20)
        P:(10, 10, 10)
        """
        self.set_colour((30, 30, 30))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(40, 0, -10)])
        exp = 2
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "B = 1, L  = 1")

    def test_score_9(self):
        """
                                F_____E______B_______A______
                                |     |      |       |      |
                                G_____H______C_______D______|
                                |     |      |       |      |
                                J_____I______N_______M______|
                                |     |/ / / |/ / /  |      |
                                K_____L/_/_/_O/_/_/__P______|
                                |/ / /|      |       |/ / / |
                                |/ /_/|______|_______|/_/_/_|
                A:(40, 40, 40)
                B:(30, 30, 30)
                C:(20, 20, 20)
                D:(10, 10, 10)
                E:(60, 60, 60)
                F:(50, 50, 50)
                G:(40, 40, 40)
                H:(30, 30, 30)
                I:(100, 100, 100)
                J:(200, 200, 200)
                K:(100, 100, 100)
                L:(200, 200, 200)
                M:(200, 200, 200)
                N:(100, 100, 100)
                O:(200, 200, 200)
                P:(100, 100, 100)
                """
        self.set_colour((100, 100, 100))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(100, 500, 100)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(100, 500, 100)])
        self.one_internal.children[2].children[2].colour = (100, 100, 100)
        self.one_internal.children[2].children[3].colour = (200, 200, 200)
        self.one_internal.children[3].children[0].colour = (200, 200, 200)
        self.one_internal.children[3].children[1].colour = (100, 100, 100)
        self.one_internal.children[3].children[2].colour = (200, 200, 200)
        self.one_internal.children[3].children[3].colour = (100, 100, 100)
        exp = 4
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "K = 2, P  = 2")

    def test_score_10(self):
        """
                                F_____E______B_______A______
                                |     |      |       |      |
                                G_____H______C_______D______|
                                |     |      |       |      |
                                J_____I______N_______M______|
                                |     |/ / / |       |/ / / |
                                K_____L/_/_/_O_______P/_/_/_|
                                |/ / /|      |/ / /  |      |
                                |/ /_/|______|/_/_/__|______|
                A:(40, 40, 40)
                B:(30, 30, 30)
                C:(20, 20, 20)
                D:(10, 10, 10)
                E:(60, 60, 60)
                F:(50, 50, 50)
                G:(40, 40, 40)
                H:(30, 30, 30)
                I:(100, 100, 100)
                J:(200, 200, 200)
                K:(100, 100, 100)
                L:(200, 200, 200)
                M:(100, 100, 100)
                N:(200, 200, 200)
                O:(100, 100, 100)
                P:(200, 200, 200)
        """
        self.set_colour((100, 100, 100))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(100, 500, 100)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(100, 500, 100)])
        self.one_internal.children[2].children[2].colour = (100, 100, 100)
        self.one_internal.children[2].children[3].colour = (200, 200, 200)
        self.one_internal.children[3].children[2].colour = (100, 100, 100)
        self.one_internal.children[3].children[3].colour = (200, 200, 200)
        exp = 4
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "K = 2, M  = 1, O = 1")

    def test_goal_11(self):
        """
                        F_____E______B_______A______
                        |/ / /|      |       |      |
                        G/_/_/H______C_______D______|
                        |     |/ / / |       |      |
                        J_____I/_/_/_N_______M______|
                        |     |      |/ / /  |      |
                        K_____L______O/_/_/__P______|
                        |     |      |       |/ / / |
                        |_____|______|_______|/_/_/_|
        A:(40, 40, 40)
        B:(30, 30, 30)
        C:(20, 20, 20)
        D:(10, 10, 10)
        E:(100, 100, 100)
        F:(200, 200, 200)
        G:(100, 100, 100)
        H:(200, 200, 200)
        I:(60, 60, 60)
        J:(50, 50, 50)
        K:(40, 40, 40)
        L:(30, 30, 30)
        M:(100, 100, 100)
        N:(200, 200, 200)
        O:(100, 100, 100)
        P:(200, 200, 200)
        """
        self.set_colour((200, 200, 200))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(100, 500, 100)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(100, 500, 100)])
        self.one_internal.children[1].children[0].colour = (100, 100, 100)
        self.one_internal.children[1].children[1].colour = (200, 200, 200)
        self.one_internal.children[1].children[2].colour = (100, 100, 100)
        self.one_internal.children[1].children[3].colour = (200, 200, 200)
        self.one_internal.children[3].children[0].colour = (100, 100, 100)
        self.one_internal.children[3].children[1].colour = (200, 200, 200)
        self.one_internal.children[3].children[2].colour = (100, 100, 100)
        self.one_internal.children[3].children[3].colour = (200, 200, 200)
        exp = 4
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "F = 2, P = 2")

    def test_goal_12(self):
        """
                                F_____E______B_______A______
                                |/ / /|      |       |/ / / |
                                G/_/_/H______C_______D/_/_/_|
                                |     |      |       |      |
                                J_____I______N_______M______|
                                |     |      |       |      |
                                K_____L______O_______P______|
                                |/ / /|      |       |/ / / |
                                |/ /_/|______|_______|/_/_/_|
                A:(40, 40, 40)
                B:(30, 30, 30)
                C:(20, 20, 20)
                D:(10, 10, 10)
                E:(50, 50, 50)
                F:(40, 40, 40)
                G:(30, 30, 30)
                H:(20, 20, 20)
                I:(60, 60, 60)
                J:(50, 50, 50)
                K:(40, 40, 40)
                L:(30, 30, 30)
                M:(70, 70, 70)
                N:(60, 60, 60)
                O:(50, 50, 50)
                P:(40, 40, 40)
        """
        self.set_colour((40, 40, 40))
        self.set_children(self.one_internal.children[1], [(i, i, i) for i in range(50, 10, -10)])
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[3], [(i, i, i) for i in range(70, 30, -10)])
        exp = 8
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "Every corner counts twice so in total you need to have 4 * 2 = 8")


if __name__ == "__main__":
    unittest.main(exit=False)
