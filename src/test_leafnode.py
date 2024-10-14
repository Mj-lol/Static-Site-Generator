import unittest
from leafnode import *
from textnode import *
class TestLeafNode(unittest.TestCase):

    def test_to_html_with_tag_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_no_tag(self):
        node = LeafNode(None, "Just some text")
        expected_html = 'Just some text'
        self.assertEqual(node.to_html(), expected_html)

    def test_init_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leafnode_equality(self):
        node1 = LeafNode("p", "Hello")
        node2 = LeafNode("p", "Hello")
        self.assertEqual(node1, node2)

    def test_leafnode_inequality_due_to_value(self):
        node1 = LeafNode("p", "Hello")
        node2 = LeafNode("p", "Goodbye")
        self.assertNotEqual(node1, node2)

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode("Sample text", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Sample text")

    def test_text_type_bold(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_type_italic(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_type_code(self):
        text_node = TextNode("Code snippet", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")

    def test_text_type_link(self):
        text_node = TextNode("Click here", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_text_type_link_no_url(self):
        text_node = TextNode("Click here", "link")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_text_type_image(self):
        text_node = TextNode("Image alt text", "image", "image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="image.png" alt="Image alt text" />')

    def test_text_type_image_no_url(self):
        text_node = TextNode("Image alt text", "image")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == '__main__':
    unittest.main()
