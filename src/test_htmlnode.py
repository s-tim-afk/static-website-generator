import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
		node = LeafNode(None, "hello")
		self.assertEqual((node.tag, node.value, node.props), (None, "hello", None))

	def test_children(self):
		with self.assertRaises(TypeError):
			LeafNode("p", "hello", ["child1"], {"href": "link"})
		#node = LeafNode("p", "hello world", [LeafNode("p", "come on in")], {"href": "https://www.google.com"})
		#node2 = LeafNode("p", "come on in")
		#self.assertRaises(TypeError, LeafNode("p", "hello world", [node2], {"href": "https://www.google.com"}))

	def test_none_value(self):
		with self.assertRaises(ValueError):
			node = LeafNode ("p", None, {"href": "https://www.google.com"})


	if __name__ == "__main__":
		unittest.main()

class TestParentNode(unittest.TestCase):
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

	def test_to_html_with_props(self):
		child_node = LeafNode("a", "Link", {"href": "https://meatspin.gov", "target": "_blank"})
		parent_node = ParentNode("h1", [child_node])
		self.assertEqual(parent_node.to_html(), '<h1><a href="https://meatspin.gov" target="_blank">Link</a></h1>')

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