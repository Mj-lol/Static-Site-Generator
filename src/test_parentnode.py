import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parentnode_with_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Paragraph 1"),
                LeafNode("p", "Paragraph 2"),
            ],
        )
        expected_html = "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_parentnode_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(
                None,
                [
                    LeafNode("p", "Paragraph"),
                ],
            ).to_html()

    def test_parentnode_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_nested_parentnodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode("h1", "Title"),
                        LeafNode("p", "Content"),
                    ],
                ),
                LeafNode("p", "Footer"),
            ],
        )
        expected_html = "<div><section><h1>Title</h1><p>Content</p></section><p>Footer</p></div>"
        self.assertEqual(node.to_html(), expected_html)
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
if __name__ == '__main__':
    unittest.main()
