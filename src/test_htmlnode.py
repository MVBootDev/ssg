import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a paragraph", None, None)
        node2 = HTMLNode("p", "this is a paragraph", None, None)
        self.assertEqual(node, node2)

    def test_children_not_eq(self):
        child_p = HTMLNode("p", "paragraph text", None, None)
        child_h1 = HTMLNode("h1", "heading text", None, None)
        node = HTMLNode("section", None, [child_p])
        node2 = HTMLNode("section", None, [child_h1])
        self.assertNotEqual(node, node2)

    def test_children_eq(self):
        h1 = HTMLNode("h1", "heading text", None, {"class": "text-red"})
        h2 = HTMLNode("h1", "heading text", None, {"class": "text-red"})
        child_h1 = HTMLNode("heading", None, [h1], {"class": "p-8"})
        child_h2 = HTMLNode("heading", None, [h2], {"class": "p-8"})
        node = HTMLNode("section", None, [child_h1])
        node2 = HTMLNode("section", None, [child_h2])
        self.assertEqual(node, node2)
    
    def test_props(self):
        props = {"class": "bg-blue", "id": "bam"}
        node = HTMLNode("aside", None, None, props)
        node2 = HTMLNode("aside", None, None, props)
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        html1 = HTMLNode(None, None, None, {"class": "p-8", "target": "_blank"}).props_to_html()
        html2 = HTMLNode(None, None, None, {"class": "p-8", "target": "_blank"}).props_to_html()
        self.assertEqual(html1, html2)


if __name__ == "__main__":
    unittest.main()