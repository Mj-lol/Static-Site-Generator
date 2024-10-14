import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(tag='a', props={'href': 'https://www.google.com', 'target': '_blank'})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_without_props(self):
        node = HTMLNode(tag='p')
        expected_output = ''
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(tag='img', props={'src': 'image.png'})
        expected_output = ' src="image.png"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_eq_method(self):
        node1 = HTMLNode(tag='div', value='Content', props={'class': 'container'})
        node2 = HTMLNode(tag='div', value='Content', props={'class': 'container'})
        self.assertEqual(node1, node2)

    def test_eq_method_with_different_props(self):
        node1 = HTMLNode(tag='div', value='Content', props={'class': 'container'})
        node2 = HTMLNode(tag='div', value='Content', props={'id': 'main'})
        self.assertNotEqual(node1, node2)

if __name__ == '__main__':
    unittest.main()
