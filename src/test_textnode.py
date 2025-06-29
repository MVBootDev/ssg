import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_link(self):
        node = TextNode("Link text", TextType.LINK)
        node2 = TextNode("Link text", TextType.LINK, "www.dang.com")
        self.assertNotEqual(node, node2)
    
    def test_type(self):
        node = TextNode("Foxtrot Charlie", TextType.ITALIC)
        node2 = TextNode("Foxtrot Charlie", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()