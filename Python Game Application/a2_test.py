import unittest
from block import *
from blocky import *
from game import *
from player import *

from a2.block import Block

from typing import Optional, Tuple, List


def block_bfs(block):
    res = []
    acc = [block]
    while acc:
        temp = acc.pop(0)
        res.append(temp)
        for child in temp.children:
            acc.append(child)
    return res


class A2Test(unittest.TestCase):
    """
    This class is the top level class for all the tests in the a2.  This class is mainly used to set up data and tear down
    the data.  Also, we will encapsulate assertion functions build in the unittest into our own assertion Function.
    Write every test suites as a subclass of this TestClass to reuse the data.  For this assignment, we will write the
    test suites based on the steps denoted in the handout.  Also write down every test case as an method.  Every subclass
    should rewrite the import statements to only include necessary methods/functions
    Formalizations:
     i) Draw the tree of the question in the docstring.
     ii) Write down the expected return value.
     iii) Write the error message or segfault if students are not using debugger or you are too disappointed
     iv) For functions that using random do the followings
        i) Rewrite the import statement in the top level
            eg) Import random from <source> as customized random
        ii) Set up the seed
            eg) customized_random.seed(seed_number)
        iii) Write down the return value for the randomized function calls to make debug easier
     v) For every customized assertion function follow the format of following
        i) Every customized assertion function are passing three parameters
        ii) The first parameter is the self/The Test class
        iii) The second parameter is the test object to be verified(Normally this is going to be the attribute in the setUp)
        iv) The third parameter is an iterable collection to be used to verify the result
        v) The order for value in list of expected value should follow the same order as the docstring of the corresponding class
        A template is
        def assertFun(self, test_object, expected_result):
            act = test_object.attribute0
            exp = expected_result[0]
            self.assertEqual(act, exp, self.error_message(act, exp)
    === Attribute ===
    leaf_block: a block that itself is a leaf
    one_level: a block that contain one sub level
    one_internal: a block that whose upper right child contain 4 sub children
    """
    def setUp(self) -> None:
        # To set up data just initialize them as you do in any initializer
        # Like self.xxx = xxx
        # We also need to set up the error message format
        # You can also customize your own error message
        # This is actually a function you need to pass the parameter to call it
        self.block_attrs = ["position", "size", "colour", "level", "max_depth", "children"]
        self.leaf_block = Block((10, 10), 10, (10, 10, 10), 0, 0)
        self.one_level = Block((0, 0), 10, (10, 10, 10), 0, 1)
        self.set_children(self.one_level, [(i, i, i) for i in range(20, 60, 10)])
        self.one_internal = Block((0, 0), 100, None, 0, 2)
        self.set_children(self.one_internal, [(i, i, i) for i in range(90, 50, -10)])
        self.set_children(self.one_internal.children[0], [(i, i, i) for i in range(40, 0, -10)])
        self.error_message = "Expected value for {} is {} Actual value is {}".format

    def tearDown(self) -> None:
        self.block_attrs = ["position", "size", "colour", "level", "max_depth", "children"]
        self.leaf_block = Block((10, 10), 10, (10, 10, 10), 0, 0)
        self.one_level = Block((0, 0), 10, (10, 10, 10), 0, 1)
        self.set_children(self.one_level, [(i, i, i) for i in range(20, 60, 10)])
        self.one_internal = Block((0, 0), 100, None, 0, 2)
        self.set_children(self.one_internal, [(i, i, i) for i in range(90, 50, -10)])
        self.set_children(self.one_internal.children[0], [(i, i, i) for i in range(40, 0, -10)])

    """
    Space for the Customized Assertion Functions
    """

    def assertBlock(self, block, exps, color_check=False, is_leaf=False):
        """
        Color check is an optional parameter.  If we set color check to check then we will be given a specific color in
         the exps list to check.  Otherwise, we just need to check whether or not color in the COLOR_LIST
        """
        act_position, act_size, act_colour = block.position, block.size, block.colour
        act_level, act_depth, act_children = block.level, block.max_depth, len(block.children)
        exp_position, exp_size, exp_colour = exps[0], exps[1], exps[2]
        exp_level, exp_depth, exp_children = exps[3], exps[4], exps[5]
        self.assertEqual(exp_position, act_position, self.error_message("position", exp_position, act_position))
        self.assertEqual(exp_size, act_size, self.error_message("size", exp_size, act_size))
        if not is_leaf:
            self.assertIsNone(exp_colour)
        else:
            if color_check:
                self.assertEqual(exp_colour, act_colour, self.error_message("colour", exp_colour, act_colour))
            else:
                self.assertTrue(act_colour in COLOUR_LIST)
        self.assertEqual(exp_level, act_level, self.error_message("level", exp_level, act_level))
        self.assertEqual(exp_depth, act_depth, self.error_message("depth", exp_depth, act_depth))
        self.assertTrue(exp_children == act_children, self.error_message("Number of child", exp_children, act_children))

    def set_children(self, block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
            -> None:
        """Set the children at <level> for <block> using the given <colours>.

        Precondition:
            - len(colours) == 4
            - block.level + 1 <= block.max_depth
        """
        size = block._child_size()
        positions = block._children_positions()
        level = block.level + 1
        depth = block.max_depth
        children = [Block(None, None, None, None, None) for _ in range(4)]
        block.children = children
        attr_list = [positions, size, colours, level, depth]
        block.colour = None
        for i in range(4):
            attr_list[0] = positions[i]
            attr_list[2] = colours[i]
            block_child = block.children[i]
            for j in range(len(attr_list)):
                setattr(block_child, self.block_attrs[j], attr_list[j])


if __name__ == '__main__':
    unittest.main()
