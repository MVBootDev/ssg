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


class TestBlockToBlockType(unittest.TestCase):
    def test_code_block(self):
        block = "```\nprint('hello world')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_heading_block_h1(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_block_h6(self):
        block = "###### This is an h6 heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_quote_block_single_line(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_block_multi_line(self):
        block = "> This is a quote\n> with multiple lines\n> of text"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is just a regular paragraph with some text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_block_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_simple_paragraph(self):
        md = "This is a simple paragraph with **bold** text"
        node = markdown_to_html_node(md)
        
        # Check the structure: div containing a p with children
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        
        paragraph = node.children[0]
        self.assertEqual(paragraph.tag, "p")
        
        # Check that it has children (processed inline elements)
        self.assertIsNotNone(paragraph.children)
        self.assertGreater(len(paragraph.children), 1)  # Should have multiple text nodes
        
        # Test the HTML output if to_html() method works
        try:
            html = node.to_html()
            self.assertIn("<div>", html)
            self.assertIn("<p>", html)
            self.assertIn("<b>bold</b>", html)
            self.assertIn("</p>", html)
            self.assertIn("</div>", html)
        except NotImplementedError:
            # Skip HTML testing if to_html() not implemented yet
            print("Note: to_html() method not implemented yet, skipping HTML output test")
    
    def test_multiple_paragraphs(self):
        md = """This is the first paragraph.

This is the second paragraph with _italic_ text."""
        
        node = markdown_to_html_node(md)
        
        # Should have div containing 2 paragraphs
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 2)
        
        # Both children should be paragraphs
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[1].tag, "p")
    
    def test_code_block(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        
        # Should be pre containing code
        pre_node = node.children[0]
        self.assertEqual(pre_node.tag, "pre")
        self.assertEqual(len(pre_node.children), 1)
        
        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        
        # Content should be raw (no inline processing) with trailing newline preserved
        expected_content = "This is text that _should_ remain\nthe **same** even with inline stuff\n"
        self.assertEqual(code_node.value, expected_content)
        
        # Check HTML output matches expected (with trailing newline)
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, expected_html)

    def test_quote_single_line(self):
        md = "> This is a single line quote with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "blockquote")
        
        expected_html = "<div><blockquote>This is a single line quote with <b>bold</b> text</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_quote_multi_line(self):
        md = """> This is a multi-line quote
> with _italic_ text across
> multiple lines and `code` too"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected_html = "<div><blockquote>This is a multi-line quote\nwith <i>italic</i> text across\nmultiple lines and <code>code</code> too</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_unordered_list(self):
        md = """- First item with **bold** text
- Second item with _italic_ text
- Third item with `code`
- Fourth plain item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        ul_node = node.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 4)
        
        # All children should be li elements
        for child in ul_node.children:
            self.assertEqual(child.tag, "li")
        
        expected_html = "<div><ul><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code></li><li>Fourth plain item</li></ul></div>"
        self.assertEqual(html, expected_html)

    def test_ordered_list(self):
        md = """1. First numbered item with **bold**
2. Second numbered item with _italic_
3. Third numbered item with `code`
4. Fourth plain numbered item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        ol_node = node.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 4)
        
        # All children should be li elements
        for child in ol_node.children:
            self.assertEqual(child.tag, "li")
        
        expected_html = "<div><ol><li>First numbered item with <b>bold</b></li><li>Second numbered item with <i>italic</i></li><li>Third numbered item with <code>code</code></li><li>Fourth plain numbered item</li></ol></div>"
        self.assertEqual(html, expected_html)

    def test_headings_all_levels(self):
        md = """# H1 heading with **bold**

## H2 heading with _italic_

### H3 heading with `code`

#### H4 plain heading

##### H5 heading

###### H6 heading"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 6)
        
        # Check each heading level
        expected_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
        for i, child in enumerate(node.children):
            self.assertEqual(child.tag, expected_tags[i])
        
        expected_html = "<div><h1>H1 heading with <b>bold</b></h1><h2>H2 heading with <i>italic</i></h2><h3>H3 heading with <code>code</code></h3><h4>H4 plain heading</h4><h5>H5 heading</h5><h6>H6 heading</h6></div>"
        self.assertEqual(html, expected_html)

    def test_mixed_content(self):
        md = """# Main Heading

This is a paragraph with **bold** text.

> This is a quote block
> with multiple lines

- Unordered list item 1
- Unordered list item 2

1. Ordered list item 1
2. Ordered list item 2

```
Code block with _no_ processing
```

## Subheading

Final paragraph."""
        
        node = markdown_to_html_node(md)
        
        # Check structure - should have 8 blocks
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 8)
        
        # Check each block type
        self.assertEqual(node.children[0].tag, "h1")      # Main Heading
        self.assertEqual(node.children[1].tag, "p")       # Paragraph
        self.assertEqual(node.children[2].tag, "blockquote")  # Quote
        self.assertEqual(node.children[3].tag, "ul")      # Unordered list
        self.assertEqual(node.children[4].tag, "ol")      # Ordered list
        self.assertEqual(node.children[5].tag, "pre")     # Code block
        self.assertEqual(node.children[6].tag, "h2")      # Subheading
        self.assertEqual(node.children[7].tag, "p")       # Final paragraph

    def test_assignment_examples(self):
        # Test 1 from the assignment
        md1 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node1 = markdown_to_html_node(md1)
        html1 = node1.to_html()
        expected1 = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html1, expected1)

        # Test 2 from the assignment
        md2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node2 = markdown_to_html_node(md2)
        html2 = node2.to_html()
        expected2 = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html2, expected2)