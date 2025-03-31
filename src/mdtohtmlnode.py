from blockhandling import markdown_to_blocks, block_to_blocktype, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextType, TextNode, text_node_to_html_node
from mdconvert import text_to_textnodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def heading_to_HTML(heading):
    count = heading[0 : 6].count("#")
    if count + 1 >= len(heading):
        raise ValueError("invalid heading level")
    text = heading[count + 1 :]
    return ParentNode(f"h{str(count)}", text_to_children(text))

def code_to_HTML(text):
    return ParentNode("pre", 
                      [ParentNode("code", 
                                  [text_node_to_html_node(TextNode(text[4:-3], TextType.NORMAL))])])

def ulist_to_HTML(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        html_items.append(ParentNode("li", text_to_children(item[2:])))
    return ParentNode("ul", html_items)

def olist_to_HTML(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        html_items.append(ParentNode("li", text_to_children(item[3:])))
    return ParentNode("ol", html_items)

def quote_to_HTML(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    return ParentNode("blockquote", text_to_children(" ".join(new_lines)))

def block_to_htmlnode(block):
    blocktype = block_to_blocktype(block)
    if blocktype == BlockType.PARA:
        return ParentNode("p", text_to_children(" ".join(block.split("\n"))))
    if blocktype == BlockType.QUOTE:
        return quote_to_HTML(block)
    if blocktype == BlockType.ULIST:
        return ulist_to_HTML(block)
    if blocktype == BlockType.OLIST:
        return olist_to_HTML(block)
    if blocktype == BlockType.HEAD:
        return heading_to_HTML(block)
    if blocktype == BlockType.CODE:
        return code_to_HTML(block)

def markdown_to_html_node(mdtext):
    blocks = markdown_to_blocks(mdtext)
    children_blocks = []
    for block in blocks:
        children_blocks.append(block_to_htmlnode(block))
    
    return ParentNode("div", children_blocks, None)