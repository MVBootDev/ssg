import unittest

from htmlnode import *
from leafnode import *
from parentnode import *
from textnode import *

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("p", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node], None).to_html()

    def test_to_html_with_mixed_children(self):
        grandchild_node1 = LeafNode("h1", "site title")
        grandchild_node2 = LeafNode("button", "click me")
        child_node1 = ParentNode("header", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode("main", "main text")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><header><h1>site title</h1><button>click me</button></header><main>main text</main></div>",
        )