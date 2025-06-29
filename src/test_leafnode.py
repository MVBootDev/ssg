import unittest

from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")
    
    def test_leaf_to_html_no_value_raises(self):
        with self.assertRaises(ValueError):
            node = LeafNode("h1", None).to_html()





if __name__ == "__main__":
    unittest.main()