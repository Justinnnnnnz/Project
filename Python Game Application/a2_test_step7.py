import unittest
from a2_test import A2Test
from goal import BlobGoal


class A2TestStep7(A2Test):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()


class TestBlobGoal(A2TestStep7):
    def setUp(self) -> None:
        super().setUp()
        self.goal_colour = None
        self.goal = BlobGoal(self.goal_colour)
        self.set_colour = lambda colour: setattr(self.goal, "colour", colour)

    def tearDown(self) -> None:
        super().tearDown()
        self.goal_colour = None
        self.goal = BlobGoal(self.goal_colour)
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
        self.assertEqual(1, res, "Since there is only 1 block in the board you should return 1")

    def test_goal_3(self):
        """
            ____________
            |           |
            |           |
            |___________|
        colour:(10, 10, 10)
        """

        self.set_colour((10, 10, 10))
        exps = [4, 16, 64, 256]
        res = []
        for i in range(1, 5):
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
            exp = 1
            self.assertEqual(exp, res, "Every block only connect to itself, so you should always return 1")
        self.set_colour((20, 20, 20))
        for i in range(4):
            self.one_level.children[i].colour = (20, 20, 20)
            res = self.goal.score(self.one_level)
            exp = i + 1
            self.assertEqual(exp, res, "You should accumulate the count of the corner")
        self.one_level.combine()
        res = self.goal.score(self.one_level)
        exp = 4
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
        exp = 1
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "The block only connects to itself")

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
        self.assertEqual(exp, res, "You have one fully connected blob of size 7")

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
        exp = 4
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "You have a connected blob of size 4")

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
        exp = 1
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "Diagonal connections do not count")

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
        exp = 2
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "Two diagonal connections each counts as one so the longest connected blob is I N which is 2")

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
        exp = 1
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "Diagonal connections do not count")

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
        exp = 1
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "Diagonal connections do not count")

    def test_goal_12(self):
        """
                        F_____E______B_______A______
                        |/ / /|      |       |/ / / |
                        G/_/_/H______C_______D/_/_/_|
                        |/ / /|/ / / |       |/ / / |
                        J/_/_/I/_/_/_N_______M/_/_/_|
                        |     |      |/ / /  |/ / / |
                        K_____L______O/_/_/__P/_/_/_|
                        |/ / /|      |       |/ / / |
                        |/_/_/|______|_______|/_/_/_|
        A:(40, 40, 40)
        B:(30, 30, 30)
        C:(20, 20, 20)
        D:(40, 40, 40)
        E:(10, 10, 10)
        F:(40, 40, 40)
        G:(40, 40, 40)
        H:(40, 40, 40)
        I:(60, 60, 60)
        J:(50, 50, 50)
        K:(40, 40, 40)
        L:(30, 30, 30)
        M:(40, 40, 40)
        N:(40, 40, 40)
        O:(20, 20, 20)
        P:(40, 40, 40)
        """
        self.set_colour((40, 40, 40))
        self.one_internal.children[0].children[3].colour = (40, 40, 40)
        self.set_children(self.one_internal.children[1], [(40, 40, 40) for i in range(4)])
        self.one_internal.children[1].children[0].colour = (10, 10, 10)
        self.set_children(self.one_internal.children[2], [(i, i, i) for i in range(60, 20, -10)])
        self.set_children(self.one_internal.children[3], [(40, 40, 40) for i in range(4)])
        self.one_internal.children[3].children[2].colour = (20, 20, 20)
        exp = 5
        res = self.goal.score(self.one_internal)
        self.assertEqual(exp, res, "The largest connected blob is ADMNP")

if __name__ == "__main__":
    unittest.main(exit=False)
