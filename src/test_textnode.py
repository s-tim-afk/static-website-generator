import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		node2 = TextNode("This is a DIFFERENT text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_not_eq2(self):
		node = TextNode("This is a text node",  TextType.NORMAL)
		node2 = TextNode("This is a text node", TextType.CODE)
		self.assertNotEqual(node, node2)

	def test_url(self):
		with self.assertRaises(Exception):
			node = TextNode("link", TextType.LINK)

	def test_repr(self):
		node = TextNode("hello", TextType.BOLD)
		self.assertEqual('TextNode(hello, bold, None)', node.__repr__())

class TestTextNodeToHTMLNode(unittest.TestCase):

	def test_text_to_html(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_link(self):
		node = TextNode("link", TextType.LINK, "https://meatspin.gov")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.props, {"href": "https://meatspin.gov"})

	def test_image(self):
		node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(
			html_node.props,
			{"src": "https://www.boot.dev", "alt": "This is an image"},
        )

if __name__ == "__main__":
	unittest.main()
