import re

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