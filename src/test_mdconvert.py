from mdconvert import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link)
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
        self.assertEqual(new_nodes, [
                                        TextNode("This has ", TextType.NORMAL),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" and ", TextType.NORMAL),
                                     TextNode("code", TextType.CODE),
                                     TextNode(" and ", TextType.NORMAL),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" text", TextType.NORMAL)
                                        ]
                                            )
        
    def test_order(self):
        node = TextNode("This has **bold** and `code` and _italic_ text", TextType.NORMAL)
        new_nodes_1 = split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter([node], "`", TextType.CODE), 
                                "_", TextType.ITALIC),
                                    "**", TextType.BOLD
                                    )
        new_nodes_2 = split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter([node], "**", TextType.BOLD),
                                "`", TextType.CODE),
                                    "_", TextType.ITALIC
                                        )
        new_nodes_3 = split_nodes_delimiter(
                        split_nodes_delimiter(
                            split_nodes_delimiter([node], "_", TextType.ITALIC),
                                "**", TextType.BOLD),
                                    "`", TextType.CODE
                                        )
        self.assertEqual(new_nodes_1, new_nodes_2, new_nodes_3)

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_split_no_image(self):
        node = TextNode("hands across the water, heads across the sky", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("hands across the water, heads across the sky", TextType.NORMAL)], 
            new_nodes
            )

    def test_split_image_beginning(self):
        node = TextNode(
            "![IMAGE!!!](https://imgur.com/gallery/elon-musk-with-ghislaine-maxwell-ebyXoAD) Did you see that?", 
                        TextType.NORMAL
                        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("IMAGE!!!", TextType.IMAGE, "https://imgur.com/gallery/elon-musk-with-ghislaine-maxwell-ebyXoAD"),
                              TextNode(" Did you see that?", TextType.NORMAL)], new_nodes)
        
    def test_split_invalid_syntax(self):
        node = TextNode(
            "hey look at this ![image(https://imgur.com/gallery/elon-musk-with-ghislaine-maxwell-ebyXoAD)", 
                        TextType.NORMAL
                        )
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_image([node])

    def test_invalid_texttype(self):
        pass


class TestExtractFromMD(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
        "This is text with not one ![image](https://i.imgur.com/zjjcJKZ.png), but TWO ![images](https://uploads.dailydot.com/2024/12/Screen-Shot-2024-12-10-at-9.51.42-AM.png?q=65&auto=format&w=1240)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("images", "https://uploads.dailydot.com/2024/12/Screen-Shot-2024-12-10-at-9.51.42-AM.png?q=65&auto=format&w=1240")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to github](https://github.com/s-tim-afk) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("to github", "https://github.com/s-tim-afk"), ("to youtube", "https://www.youtube.com")], matches)

    def test_mixed_link_image(self):
        matches = extract_markdown_links(
            "This is text with a link [to github](https://github.com/s-tim-afk) and a funny ![png](https://uploads.dailydot.com/2024/12/Screen-Shot-2024-12-10-at-9.51.42-AM.png?q=65&auto=format&w=1240)"
        )
        self.assertListEqual([("to github", "https://github.com/s-tim-afk")], matches)

    def test_mixed_image_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to github](https://github.com/s-tim-afk) and a funny ![png](https://uploads.dailydot.com/2024/12/Screen-Shot-2024-12-10-at-9.51.42-AM.png?q=65&auto=format&w=1240)"
            )
        self.assertListEqual([("png", "https://uploads.dailydot.com/2024/12/Screen-Shot-2024-12-10-at-9.51.42-AM.png?q=65&auto=format&w=1240")], matches)

    def test_no_image(self):
        matches = extract_markdown_images(
            "This is just text, no images no link no nothin' bub"
        )
        self.assertListEqual([], matches)

    def test_no_link(self):
        matches = extract_markdown_links(
            "This is just text, no images no link no nothin' bub"
        )
        self.assertListEqual([], matches)