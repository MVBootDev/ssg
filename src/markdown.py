import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    # Check for code block (starts and ends with ```)
    if re.match(r'^```[\s\S]*```$', block, re.DOTALL):
        return BlockType.CODE
    if re.match(r'^#{1,6} .+', block):
        return BlockType.HEADING
    lines = block.split("\n")
    if all(re.match(r'^> ', line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r'^- ', line) for line in lines):
        return BlockType.UNORDERED_LIST
    # Alternative for full markdown spec (supports -, *, +):
    # if all(re.match(r'^[-*+] ', line) for line in lines):
    #     return BlockType.UNORDERED_LIST
    is_ordered_list = []
    for i in range(1, len(lines) + 1):
        if re.match(f'^{i}\\. ', lines[i-1]):  # f-string with escaped dot
            is_ordered_list.append(True)
        else:
            is_ordered_list.append(False)
            break
    if all(is_ordered_list):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def extract_markdown_images(text):
    seek = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(seek, text)

def extract_markdown_links(text):
    seek = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(seek, text)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    print("\nblocks split on two newlines:", blocks)
    cleaned_blocks = list(map(_clean_block, blocks))
    print("\ncleaned_blocks: ", cleaned_blocks)
    # After cleaning, filter out empty blocks
    cleaned_blocks = [block for block in cleaned_blocks if block]
    return cleaned_blocks


def _clean_block(block):
    # Step 1: Strip leading/trailing newlines and whitespace
    cleaned = block.strip("\n").strip()
    
    # Step 2: Add your regex processing here
    # cleaned = re.sub(r'\n\s+', '\n', cleaned)
    return re.sub(r'\n\s+', '\n', cleaned)