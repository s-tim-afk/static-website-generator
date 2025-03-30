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

def process_image_text(text):
    if not text:
        return []
    image_info = extract_markdown_images(text)
    if "![" in text:
        if not image_info:
            raise ValueError("invalid syntax")
    if not image_info:
        return [TextNode(text, TextType.NORMAL)]
    
    result = []
    tupl = image_info[0]
    sections = text.split(f"![{tupl[0]}]({tupl[1]})", 1)
    if len(sections) != 2:
        raise ValueError("invalid syntax, image section not closed")
    before = sections[0]
    after = sections[1]

    if before:
        result.append(TextNode(before, TextType.NORMAL))

    result.append(TextNode(tupl[0], TextType.IMAGE, tupl[1]))

    if after:
        result.extend(process_image_text(after))

    return result

def process_link_text(text):
    if not text:
        return []
    link_info = extract_markdown_links(text)
    if "[" in text or "](" in text:
        if not link_info:
            raise ValueError("invalid syntax")
    if not link_info:
        return [TextNode(text, TextType.NORMAL)]
    
    result = []
    tupl = link_info[0]
    sections = text.split(f"[{tupl[0]}]({tupl[1]})", 1)
    if len(sections) != 2:
        raise ValueError("invalid syntax, image section not closed")
    before = sections[0]
    after = sections[1]

    if before:
        result.append(TextNode(before, TextType.NORMAL))

    result.append(TextNode(tupl[0], TextType.LINK, tupl[1]))

    if after:
        result.extend(process_link_text(after))

    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            new_nodes.extend(process_image_text(node.text))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:    
            new_nodes.extend(process_link_text(node.text))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL)
    return split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_link(
                    split_nodes_image([node])
                ),
            "`", TextType.CODE),
        "_", TextType.ITALIC),
    "**", TextType.BOLD)


#def markdown_to_blocks(text):
#    stripped = list(map(lambda line: line.strip(), text.split("\n\n")))
#    blocks = []
#    for line in stripped:
#        if "\n" in line:
#            print(list(map(lambda x: x.translate({ord(c):None for c in ' \n\t\r'}), line.splitlines(True))))
#            print(blocks.extend("".join(map(lambda x: x.translate({ord(c):None for c in ' \n\t\r'}), line.splitlines(True)))))
#            blocks.extend("".join(map(lambda x: x.strip(), filter(None, re.split(r"\n", line))))) # tried some ish with the re module since its already imported! re.split confusing me though
#            #okay turns out .strip() strips newlines as well 
#        else:
#            blocks.append(line)

#    return blocks
#nah man i give up on doing this nicely

def markdown_to_blocks(text):
    raw_blocks = text.split("\n\n")
    
    cleaned_blocks = []
    for block in raw_blocks:
        lines = block.split("\n")
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block = "\n".join([line for line in cleaned_lines if line])
        if cleaned_block:
            cleaned_blocks.append(cleaned_block)
    
    return cleaned_blocks
