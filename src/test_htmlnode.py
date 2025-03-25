import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("text", "value", None, {"href": "https://www.google.com", "target": "_blank"})
		node2 = HTMLNode("text", "value", None, {"href": "https://www.google.com", "target": "_blank"})
		self.assertEqual(node.tag, node2.tag)

	def test_default(self):
		node = HTMLNode()
		self.assertEqual((node.tag, node.value, node.children, node.props), (None, None, None, None))

	def test_props(self):
		node = HTMLNode("<h1>", "hello", None, {
    		"href": "https://www.google.com",
    		"target": "_blank",
			})
		self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

	def test_props_empty(self):
		node = HTMLNode("<h1>", "herro", None)
		self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_a(self):
		node = LeafNode("a", "click this link", {"href": "https://www.google.com", "target": "_blank",})
		self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">click this link</a>')

	def test_default(self):
		node = LeafNode()
		self.assertEqual((node.tag, node.value, node.props), (None, None, None))

	def test_children(self):
		with self.assertRaises(TypeError):
			LeafNode("p", "hello", ["child1"], {"href": "link"})
		#node = LeafNode("p", "hello world", [LeafNode("p", "come on in")], {"href": "https://www.google.com"})
		#node2 = LeafNode("p", "come on in")
		#self.assertRaises(TypeError, LeafNode("p", "hello world", [node2], {"href": "https://www.google.com"}))

	def test_none_value(self):
		node = LeafNode ("p", None, {"href": "https://www.google.com"})
		self.assertRaisesRegex(ValueError, "leaf node must have a value", node.to_html)


	if __name__ == "__main__":
		unittest.main()
