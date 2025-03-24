import unittest

from textnode import TextNode, TextType

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
		node = TextNode("this is a link", TextType.LINK)
		self.assertEqual(node.url, None)

	def test_repr(self):
		node = TextNode("hello", TextType.BOLD)
		self.assertEqual('TextNode(hello, bold, None)', node.__repr__())

if __name__ == "__main__":
	unittest.main()
