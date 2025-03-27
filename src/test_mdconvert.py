from mdconvert import split_nodes_delimiter
from textnode import TextType, TextNode
import unittest

class TestMDConvert(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.NORMAL),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.NORMAL),
])
        
    def test_missing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.NORMAL)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with no delimiter", TextType.NORMAL)])

    def test_non_texttype(self):
        node = TextNode("This is text with **bold** text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_multiple_delimiters(self):
        node = TextNode("Here is `code1` and here is `code2` in one line", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Here is ", TextType.NORMAL), 
                                     TextNode("code1", TextType.CODE),
                                     TextNode(" and here is ", TextType.NORMAL),
                                     TextNode("code2", TextType.CODE),
                                     TextNode(" in one line", TextType.NORMAL)])
        
    def test_delimiters_at_ends(self):
        node = TextNode("`code at start` and `code at end`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("code at start", TextType.CODE), 
                                     TextNode(" and ", TextType.NORMAL),
                                     TextNode("code at end", TextType.CODE),
                                        ]
                                        )
        
    def test_mixed_nodes(self):
        node = [
                TextNode("Text before", TextType.NORMAL),
                TextNode("already bold", TextType.BOLD),
                TextNode("Text with `code` inside", TextType.NORMAL)
                    ]
        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                            TextNode("Text before", TextType.NORMAL),
                            TextNode("already bold", TextType.BOLD),
                            TextNode("Text with ", TextType.NORMAL),
                            TextNode("code", TextType.CODE),
                            TextNode(" inside", TextType.NORMAL)
                                ]
                                    )
        
    def test_different_delimiter_types(self):
        node = TextNode("This has **bold** and `code` and _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter([node], "`", TextType.CODE), 
                                "_", TextType.ITALIC),
                                    "**", TextType.BOLD
                                    )
        self.assertEqual(new_nodes, [TextNode("This has ", TextType.NORMAL),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" and ", TextType.NORMAL),
                                     TextNode("code", TextType.CODE),
                                     TextNode(" and ", TextType.NORMAL),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" text", TextType.NORMAL)])