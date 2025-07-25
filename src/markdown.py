"""
Markdown to HTML conversion module.

This module provides functions to convert markdown text into HTMLNode structures
that can be rendered as HTML. Supports all major markdown block types including
paragraphs, headings, code blocks, quotes, and lists.
"""

import re
from enum import Enum
from typing import List
from htmlnode import HTMLNode
from textnode import *

# Constants
CODE_BLOCK_DELIMITER = "```"
HEADING_PATTERN = r'^(#{1,6}) (.+)'
CODE_BLOCK_PATTERN = r'^```[\s\S]*```$'

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    """Determine the type of markdown block."""
    if not block.strip():
        return BlockType.PARAGRAPH
        
    # Check for code block (starts and ends with ```)
    if re.match(CODE_BLOCK_PATTERN, block, re.DOTALL):
        return BlockType.CODE
    if re.match(HEADING_PATTERN, block):
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


def markdown_to_blocks(markdown: str) -> List[str]:
    """Split markdown text into blocks separated by double newlines."""
    if not markdown.strip():
        return []
        
    raw_blocks = markdown.split("\n\n")
    print("\nblocks split on two newlines:", raw_blocks)
    cleaned_blocks = list(map(_clean_block, raw_blocks))
    print("\ncleaned_blocks: ", cleaned_blocks)
    
    # Filter out empty blocks after cleaning
    non_empty_blocks = [block for block in cleaned_blocks if block]
    return non_empty_blocks


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Convert markdown text to an HTMLNode tree.
    
    Args:
        markdown: The markdown text to convert
        
    Returns:
        HTMLNode: A div element containing the converted markdown blocks
    """
    blocks = markdown_to_blocks(markdown)
    parent = HTMLNode("div", children=[])

    for block in blocks:
        type = block_to_block_type(block)
        child_node = None

        match type.name:
            case "PARAGRAPH":
                # Replace newlines with spaces in paragraph text
                paragraph_text = block.replace('\n', ' ')
                children = _text_to_children(paragraph_text)
                child_node = HTMLNode("p", children=children)
            case "CODE":
                # Remove the ``` markers but preserve internal whitespace/newlines
                delimiter_length = len(CODE_BLOCK_DELIMITER)
                code_content = block[delimiter_length:-delimiter_length]
                # Remove leading newline if present, but preserve trailing newlines
                if code_content.startswith('\n'):
                    code_content = code_content[1:]
                # Create nested structure: <pre><code>content</code></pre>
                code_node = HTMLNode("code", value=code_content)
                child_node = HTMLNode("pre", children=[code_node])
            case "QUOTE":
                lines = block.split('\n')
                content = list(map(lambda line: line.strip("> "), lines))
                cleaned_content = '\n'.join(content)
                
                # Process inline markdown within the quote
                children = _text_to_children(cleaned_content)
                child_node = HTMLNode("blockquote", children=children)
            case "UNORDERED_LIST":
                child_node = _create_list_node(block, "ul")
            case "ORDERED_LIST":
                child_node = _create_list_node(block, "ol")
            case "HEADING":
                # Count # symbols to determine heading level
                heading_match = re.match(HEADING_PATTERN, block)
                if heading_match:
                    hash_symbols = heading_match.group(1)
                    heading_level = len(hash_symbols)  # Number of # symbols
                    heading_text = heading_match.group(2)  # Text after the #'s
                    
                    # Process inline markdown in heading text
                    children = _text_to_children(heading_text)
                    
                    # Create heading tag (h1, h2, etc.)
                    heading_tag = f"h{heading_level}"
                    child_node = HTMLNode(heading_tag, children=children)

        parent.children.append(child_node)
        
    return parent 


def _text_to_children(text: str) -> List[HTMLNode]:
    """Convert text with inline markdown to a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def _create_list_node(block: str, list_type: str) -> HTMLNode:
    """Create a list HTMLNode (ul or ol) from a block of list items."""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove prefix based on list type
        if list_type == "ul":
            item_text = line.strip("- ").strip()
        else:  # ol
            item_text = re.sub(r'^\d+\. ', '', line).strip()
        
        # Process inline markdown for each list item
        children = _text_to_children(item_text)
        
        # Create li element for this item
        li_node = HTMLNode("li", children=children)
        list_items.append(li_node)
    
    # Create parent list node
    return HTMLNode(list_type, children=list_items)


def _clean_block(block: str) -> str:
    """
    Clean a markdown block by removing extra whitespace.
    
    Removes leading/trailing whitespace and normalizes internal spacing
    while preserving intentional line breaks.
    """
    # Strip leading/trailing newlines and whitespace
    cleaned = block.strip("\n").strip()
    
    # Normalize internal whitespace: replace newline + spaces with just newline
    return re.sub(r'\n\s+', '\n', cleaned)