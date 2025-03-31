from enum import Enum

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

class BlockType(Enum):
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_blocktype(text):
    if text[0] == "#":
        return BlockType.HEAD
    if text[0:3] == "```" and text[-3:] == "```":
        return BlockType.CODE
    lines = text.split("\n")
    
    fail_counter = 0
    for line in lines:
        if line[0] != ">":
            fail_counter += 1
    if fail_counter == 0:
        return BlockType.QUOTE
    
    fail_counter = 0
    for line in lines:
        if line[0:2] != "- ":
            fail_counter += 1
    if fail_counter == 0:
        return BlockType.ULIST
    
    fail_counter = 0
    for i in range(len(lines)):
        if lines[i][0:3] != f"{str(i+1)}. ":
            fail_counter += 1
    if fail_counter == 0:
        return BlockType.OLIST
    
    return BlockType.PARA