import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from j2v.generation.generator import Generator


class GeneratorTests(unittest.TestCase):
    def test_empty(self):
        """
        For empty JSON nothing should be created.
        :return:
        """
        g = Generator()
        g.collect_all_paths(current_dict={})
        self.assertFalse(g.views_dimensions_expr)
        self.assertFalse(g.explore_joins)

    def test_int_key(self):
        """
        Int key in JSON should be ignored
        :return:
        """
        g = Generator()
        g.collect_all_paths(current_dict={1: 2})
        self.assertFalse(g.views_dimensions_expr)
        self.assertFalse(g.explore_joins)

    def test_one_array(self):
        """
        Simple test exactly 1 view should be created with 1 dimension, and one LATERAL FLATTEN expression
        :return:
        """
        g = Generator()
        g.collect_all_paths(current_dict={"orders": [{"id": 3}, {"id": 334}]})
        self.assertIn("orders", g.views_dimensions_expr)
        self.assertEqual(1, len(g.views_dimensions_expr["orders"]))
        self.assertIn("id", list(g.views_dimensions_expr["orders"])[0])
        self.assertEqual(1, len(g.explore_joins))


def run_all():
    gt = GeneratorTests()
    gt.test_empty()
    gt.test_int_key()
    gt.test_one_array()


if __name__ == '__main__':
    run_all()
