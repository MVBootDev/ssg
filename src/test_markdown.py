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