from textnode import TextNode, TextType
import re

def process_text(text, delimiter, text_type):
    if delimiter not in text:
        return [TextNode(text, TextType.NORMAL)]
    start = text.index(delimiter)
    end = text.index(delimiter, start + len(delimiter))

    before = text[:start]
    between = text[start + len(delimiter): end]
    after = text[end + len(delimiter):]

    result = []
    if before:
        result.append(TextNode(before, TextType.NORMAL))

    result.append(TextNode(between, text_type))
    
    if after:
        result.extend(process_text(after, delimiter, text_type))
    return result

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        elif delimiter not in node.text:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("invalid markdown syntax")
        else:
            new_nodes.extend(process_text(node.text, delimiter, text_type))
            
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #return re.findall(r"!\[(.*?)\]\((.*?)\)", text) <--- pretty adequate but trips up on nested square brackets

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #return re.findall(r"\[(.*?)\]\((.*?)\)", text) <------- come back and replace these using a proper markdown module