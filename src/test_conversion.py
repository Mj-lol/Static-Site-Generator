import unittest
from textnode import *
class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is plain text"
        expected_nodes = [
            TextNode("This is plain text", TextType.TEXT)
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_bold_text(self):
        text = "This is **bold** text"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_italic_text(self):
        text = "This is *italic* text"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_code_text(self):
        text = "This is `code` text"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_image(self):
        text = "Here is an image ![alt text](https://example.com/image.jpg)"
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_link(self):
        text = "Here is a [link](https://example.com)"
        expected_nodes = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_mixed_formatting(self):
        text = (
            "This is **bold**, *italic*, and `code` with an image "
            "![image](https://example.com/image.jpg) and a [link](https://example.com)"
        )
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_no_formatting(self):
        text = "Just plain text without any formatting."
        expected_nodes = [
            TextNode("Just plain text without any formatting.", TextType.TEXT)
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)

    def test_multiple_bold_and_italic(self):
        text = "Text with **bold** and *italic* and more **bold** here."
        expected_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" here.", TextType.TEXT),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, result_nodes)






block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


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

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)







if __name__ == "__main__":
    unittest.main()
