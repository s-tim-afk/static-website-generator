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