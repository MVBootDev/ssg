from enum import Enum
from leafnode import *
from typing import List

# 2. Constants
TEXT_TYPE_NAME = "TEXT"
INVALID_MARKDOWN_MSG = "invalid Markdown"

class TextType(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "anchor links"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError("text type error")
        else:
            self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        test1 = self.text == other.text
        test2 = self.text_type == other.text_type
        test3 = self.url == other.url
        return test1 and test2 and test3
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
# 4. Public functions (main API)
def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("not a text node dude!")
    name, text, url = text_node.text_type.name, text_node.text, text_node.url
    match name:
        case "TEXT":
            return LeafNode(None, text)
        case "BOLD":
            return LeafNode("b", text)
        case "ITALIC":
            return LeafNode("i", text)
        case "CODE":
            return LeafNode("code", text)
        case "LINK":
            return LeafNode("a", text, {"href": url})
        case "IMAGE":
            return LeafNode("img", text, {"src": url})
        
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """
    Split TextNodes by delimiter and convert matching text to specified type.
    
    Args:
        old_nodes: List of TextNodes to process
        delimiter: String delimiter to split by (e.g., "**", "_", "`")
        text_type: TextType enum for the matched content
        
    Returns:
        List of TextNodes with matching content converted to specified type
        
    Raises:
        Exception: If invalid Markdown syntax (unmatched delimiters)
    """
    new_list = []
    for node in old_nodes:
        if node.text_type.name != TEXT_TYPE_NAME:
            new_list.append(node)
            continue
        
        split_nodes = _split_text_by_delimiter(node.text, delimiter, text_type)
        new_list.extend(split_nodes)
    
    return new_list

# 5. Private helper functions (implementation details)
def _split_text_by_delimiter(text, delimiter, text_type):
    """Split a single text string by delimiter and return list of TextNodes."""
    delimiter_length = len(delimiter)
    start_pos = text.find(delimiter)
    
    if start_pos == -1:
        return [TextNode(text, TextType.TEXT)]
    
    end_pos = text.find(delimiter, start_pos + delimiter_length)
    if end_pos == -1 or (end_pos - start_pos == delimiter_length):
        raise Exception("invalid Markdown")
    
    before_text = text[:start_pos]
    between_text = text[start_pos + delimiter_length:end_pos]
    after_text = text[end_pos + delimiter_length:]
    
    result = []
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))
    result.append(TextNode(between_text, text_type))
    
    # Recursively process the remaining text
    if after_text:
        result.extend(_split_text_by_delimiter(after_text, delimiter, text_type))
    
    return result
