import unittest

from markdown import *

class TestExtractImages(unittest.TestCase):
    def test_extract_one_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        value = extract_markdown_images(text)
        self.assertListEqual(value, expected)

    def test_extract_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        value = extract_markdown_images(text)
        self.assertListEqual(value, expected)

    def test_extract_image_without_exclamation_mark(self):
        text = "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        expected = []
        value = extract_markdown_images(text)
        self.assertListEqual(value, expected)


class TestExtractLinks(unittest.TestCase):
    def test_extract_one_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        value = extract_markdown_links(text)
        self.assertListEqual(value, expected)

    def test_extract_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        value = extract_markdown_links(text)
        self.assertListEqual(value, expected)

    def test_extract_link_with_exclamation_mark(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev)"
        expected = []
        value = extract_markdown_links(text)
        self.assertListEqual(value, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block with no separators"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block with no separators"])

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
Block 1


Block 2



Block 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks_heavy_indentation(self):
        md = """
        # Heading with spaces

                This paragraph has heavy indentation
                on multiple lines

        - List item with indentation
            - Nested item
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "This paragraph has heavy indentation\non multiple lines",
                "- List item with indentation\n- Nested item",
            ],
        )

    def test_markdown_to_blocks_mixed_indentation(self):
        md = """
	Tab indented paragraph
	with tab characters

        Space indented paragraph
        with space characters
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Tab indented paragraph\nwith tab characters",
                "Space indented paragraph\nwith space characters",
            ],
        )

    def test_markdown_to_blocks_only_whitespace(self):
        md = """


        

        
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_preserve_single_newlines(self):
        md = """
First line
Second line
Third line

Another block
With more lines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First line\nSecond line\nThird line",
                "Another block\nWith more lines",
            ],
        )