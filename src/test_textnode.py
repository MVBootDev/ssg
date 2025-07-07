import unittest

from textnode import *


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

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")
    
    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic_text(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code_text(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        
    def test_link(self):
        node = TextNode("This is an anchor text node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "google.com")
        self.assertEqual(html_node.value, "This is an anchor text node")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "s3bucket.com/img.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "s3bucket.com/img.jpg")


class TestSplitNodesDelimeter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_code(self):
        node = TextNode("This is text with `code` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_delimiter_found(self):
        node = TextNode("This is plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is plain text with no delimiters", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start(self):
        node = TextNode("**bold** text at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        node = TextNode("text at end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("text at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters(self):
        node = TextNode("**first** and **second** bold", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_text_between_delimiters(self):
        node = TextNode("text with **** empty", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_unmatched_opening_delimiter(self):
        node = TextNode("text with **unmatched bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_non_text_nodes_preserved(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("text with **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, text_node], "**", TextType.BOLD)
        expected = [
            TextNode("already bold", TextType.BOLD),  # preserved as-is
            TextNode("text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_only_delimiters(self):
        node = TextNode("**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_delimiter_with_spaces(self):
        node = TextNode("text with ** bold ** spaces", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode(" bold ", TextType.BOLD),
            TextNode(" spaces", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_images_found(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is plain text with no images", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_image_at_start(self):
        node = TextNode("![start image](https://example.com/start.png) text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_image_at_end(self):
        node = TextNode("text before ![end image](https://example.com/end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("text before ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_consecutive_images(self):
        node = TextNode("![first](https://example.com/1.png)![second](https://example.com/2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_image_with_spaces_in_alt_text(self):
        node = TextNode("![alt text with spaces](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("alt text with spaces", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_non_text_nodes_preserved(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("text with ![image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([bold_node, text_node])
        expected = [
            TextNode("already bold", TextType.BOLD),  # preserved as-is
            TextNode("text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_image_with_complex_url(self):
        node = TextNode("![complex](https://example.com/path/to/image.jpg?param=value&other=123)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("complex", TextType.IMAGE, "https://example.com/path/to/image.jpg?param=value&other=123"),
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_no_links_found(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is plain text with no links", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_link_at_start(self):
        node = TextNode("[start link](https://example.com/start) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://example.com/start"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_link_at_end(self):
        node = TextNode("text before [end link](https://example.com/end)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("text before ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://example.com/end"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_consecutive_links(self):
        node = TextNode("[first](https://example.com/1)[second](https://example.com/2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode("second", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_link_with_spaces_in_text(self):
        node = TextNode("[link text with spaces](https://example.com/link)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link text with spaces", TextType.LINK, "https://example.com/link"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_non_text_nodes_preserved(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("text with [link](https://example.com/link)", TextType.TEXT)
        new_nodes = split_nodes_link([bold_node, text_node])
        expected = [
            TextNode("already bold", TextType.BOLD),  # preserved as-is
            TextNode("text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/link"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_link_with_complex_url(self):
        node = TextNode("[complex](https://example.com/path/to/page.html?param=value&other=123#fragment)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("complex", TextType.LINK, "https://example.com/path/to/page.html?param=value&other=123#fragment"),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_link_does_not_match_image(self):
        # This test ensures that the link regex doesn't match image syntax
        node = TextNode("![image](https://example.com/image.png) [link](https://example.com/link)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("![image](https://example.com/image.png) ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/link"),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()