import unittest
from leafnode import LeafNode

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


if __name__ == '__main__':
    unittest.main()
