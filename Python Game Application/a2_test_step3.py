from a2_test import A2Test
import unittest
from goal import generate_goals, BlobGoal, PerimeterGoal
from settings import COLOUR_LIST
import random


class A2TestStep3(A2Test):
    def test_generate_goal_1(self):
        res = generate_goals(0)
        self.assertTrue(res == [])

    def test_generate_goal_2(self):
        res = generate_goals(1)
        self.assertTrue(len(res) == 1)
        self.assertTrue(res[0].__class__ in [BlobGoal, PerimeterGoal])
        self.assertTrue(res[0].colour in COLOUR_LIST)

    def test_generate_goal_3(self):
        for i in range(1, 100):
            random_i = random.randint(1, len(COLOUR_LIST))
            res = generate_goals(random_i)
            self.assertTrue(len(res) == random_i)
            transformed_type = list(map(lambda x: x.__class__ in [BlobGoal, PerimeterGoal], res))
            transformed_count = list(map(lambda x: x.__class__, res)).count(res[0].__class__)
            transformed_colour = list(map(lambda x: x.colour, res))
            colour_counts = [transformed_colour.count(colour) for colour in transformed_colour]
            self.assertTrue(all(transformed_type), "All the goal have to in one of BolbGoal or PerimeterGoal")
            self.assertTrue(transformed_count == len(res), "Every goal has to be the same type")
            self.assertTrue(max(colour_counts) == 1, "Every colour should be different")

    def test_blob_description(self):
        blob = BlobGoal(COLOUR_LIST[0])
        self.assertTrue(str(blob) != 'DESCRIPTION')

    def test_perimeter_description(self):
        perimeter = PerimeterGoal(COLOUR_LIST[0])
        self.assertTrue(str(perimeter) != 'DESCRIPTION')


if __name__ == "__main__":
    unittest.main(exit=False)

