import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_nodes_with_identical_properties_are_equal(self):
        # Arrange
        text = 'Sample text'
        text_type = 'bold'
        url = 'http://example.com'

        node1 = TextNode(text, text_type, url)
        node2 = TextNode(text, text_type, url)

        # Act & Assert
        self.assertEqual(node1, node2)

    def test_nodes_with_different_url_are_not_equal(self):
        # Arrange
        text = 'Sample text'
        text_type = 'bold'
        url1 = 'http://example.com'
        url2 = 'http://different.com'

        node1 = TextNode(text, text_type, url1)
        node2 = TextNode(text, text_type, url2)

        # Act & Assert
        self.assertNotEqual(node1, node2)

    def test_nodes_with_url_none(self):
        # Arrange
        text = 'Sample text'
        text_type = 'italic'

        node1 = TextNode(text, text_type)
        node2 = TextNode(text, text_type, None)

        # Act & Assert
        self.assertEqual(node1, node2)

    def test_nodes_with_different_text_type_are_not_equal(self):
        # Arrange
        text = 'Sample text'
        url = 'http://example.com'

        node1 = TextNode(text, 'bold', url)
        node2 = TextNode(text, 'italic', url)

        # Act & Assert
        self.assertNotEqual(node1, node2)

    def test_repr_method_returns_correct_string(self):
        # Arrange
        text = 'Sample text'
        text_type = 'code'
        url = 'http://example.com'

        node = TextNode(text, text_type, url)
        expected_repr = f"TextNode({text}, {text_type}, {url})"

        # Act
        actual_repr = repr(node)

        # Assert
        self.assertEqual(actual_repr, expected_repr)
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
if __name__ == "__main__":
    unittest.main()
