import unittest
from textnode import *
class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        text = "Here is an image: ![alt text](https://example.com/image.jpg)"
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_multiple(self):
        text = "Images: ![image1](https://example.com/img1.jpg) and ![image2](https://example.com/img2.jpg)"
        expected = [
            ("image1", "https://example.com/img1.jpg"),
            ("image2", "https://example.com/img2.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self):
        text = "There are no images in this text."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_mixed_content(self):
        text = "Some text ![alt1](https://example.com/img1.jpg) with a link [link](https://example.com)"
        expected = [("alt1", "https://example.com/img1.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links_single(self):
        text = "Here is a [link](https://example.com)."
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_multiple(self):
        text = "Links: [Google](https://www.google.com) and [GitHub](https://www.github.com)"
        expected = [
            ("Google", "https://www.google.com"),
            ("GitHub", "https://www.github.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self):
        text = "This is just text without any links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_mixed_content(self):
        text = "Some text with a [link](https://example.com) and an image ![alt](https://example.com/img.jpg)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_ignores_images(self):
        text = "This text has a ![alt](https://example.com/img.jpg) and a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):

    def test_single_paragraph(self):
        markdown = "This is a single paragraph."
        expected_blocks = ["This is a single paragraph."]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_multiple_paragraphs(self):
        markdown = """This is the first paragraph.

This is the second paragraph."""
        expected_blocks = [
            "This is the first paragraph.",
            "This is the second paragraph."
        ]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_heading_and_paragraph(self):
        markdown = """# Heading

This is a paragraph under a heading."""
        expected_blocks = [
            "# Heading",
            "This is a paragraph under a heading."
        ]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_list_block(self):
        markdown = """* Item 1
* Item 2
* Item 3"""
        expected_blocks = [
            "* Item 1\n* Item 2\n* Item 3"
        ]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_mixed_blocks(self):
        markdown = """# Heading

This is a paragraph.

* List item 1
* List item 2
* List item 3"""
        expected_blocks = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1\n* List item 2\n* List item 3"
        ]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)

    def test_empty_lines(self):
        markdown = """# Heading


This is a paragraph with extra blank lines.


* List item 1
* List item 2"""
        expected_blocks = [
            "# Heading",
            "This is a paragraph with extra blank lines.",
            "* List item 1\n* List item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertListEqual(expected_blocks, result)
class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")

        block = "## This is a level 2 heading"
        self.assertEqual(block_to_block_type(block), "heading")

        block = "###### This is a level 6 heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code_block(self):
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), "code")

        block = "```\nfunction test() {}\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_quote_block(self):
        block = "> This is a quote\n> It spans multiple lines"
        self.assertEqual(block_to_block_type(block), "quote")

        block = "> A single-line quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = "- Task 1\n- Task 2\n- Task 3"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

        block = "1. Step one\n2. Step two\n3. Step three"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), "paragraph")

        block = "Here is another paragraph\nwith multiple lines of text."
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_mixed_block(self):
        # Block containing both valid and invalid ordered list numbers
        block = "1. Item 1\n3. Item 3"
        self.assertEqual(block_to_block_type(block), "paragraph")

        # Block with unordered list style but missing the space after *
        block = "*Item 1\n*Item 2"
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()
