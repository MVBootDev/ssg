import re
from enum import Enum
from typing import List, Tuple, Optional, Union
from leafnode import LeafNode

# Constants
INVALID_MARKDOWN_MSG = "invalid Markdown"


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown image syntax from text.
    
    Args:
        text: String to search for markdown images
        
    Returns:
        List of tuples containing (alt_text, url) for each image found
        
    Examples:
        extract_markdown_images("![alt](url)") -> [("alt", "url")]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extract all markdown link syntax from text (excluding images).
    
    Args:
        text: String to search for markdown links
        
    Returns:
        List of tuples containing (link_text, url) for each link found
        
    Examples:
        extract_markdown_links("[text](url)") -> [("text", "url")]
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


class TextType(Enum):
    """
    Enumeration of supported text formatting types.
    
    Used to categorize different types of inline text elements
    that can be converted to HTML nodes.
    """
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "anchor links"
    IMAGE = "image"


class TextNode:
    """
    Represents a node of inline text with a specific formatting type.
    
    TextNodes are intermediate representations that get converted to HTMLNodes.
    They represent different types of inline text like plain text, bold, italic,
    code, links, and images.
    
    Attributes:
        text: The text content of the node
        text_type: The type of formatting (from TextType enum)
        url: Optional URL for links and images
        
    Examples:
        TextNode("Hello", TextType.TEXT) -> Plain text
        TextNode("Bold", TextType.BOLD) -> Bold text
        TextNode("Link", TextType.LINK, "https://example.com") -> Link with URL
        TextNode("Alt text", TextType.IMAGE, "image.png") -> Image with URL
    """
    
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None) -> None:
        """
        Initialize a TextNode.
        
        Args:
            text: The text content
            text_type: The formatting type (must be a TextType enum value)
            url: Optional URL for links and images
            
        Raises:
            TypeError: If text_type is not a TextType enum value
        """
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError(f"text_type must be a TextType enum value, got {type(text_type)}")
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other: object) -> bool:
        """Check equality with another TextNode based on all attributes."""
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self) -> str:
        """Return a string representation of the TextNode for debugging."""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Convert a string with markdown formatting to a list of TextNodes.
    
    This function processes text in order: bold -> italic -> code -> links -> images.
    Each step splits existing TEXT nodes while preserving already-formatted nodes.
    
    Args:
        text: String containing markdown formatting
        
    Returns:
        List of TextNodes representing the parsed markdown
        
    Examples:
        text_to_textnodes("**bold** and _italic_") -> 
        [TextNode("bold", BOLD), TextNode(" and ", TEXT), TextNode("italic", ITALIC)]
    """
    # Start with a single TEXT node and progressively split it
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process in order: bold, italic, code, links, images
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    
    return nodes


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Convert a TextNode to an HTMLNode (specifically a LeafNode).
    
    Args:
        text_node: TextNode to convert
        
    Returns:
        LeafNode representing the HTML equivalent of the text node
        
    Raises:
        ValueError: If text_node is not a TextNode instance
        ValueError: If text_node has an unsupported text_type
        
    Examples:
        text_node_to_html_node(TextNode("text", TextType.BOLD)) -> LeafNode("b", "text")
        text_node_to_html_node(TextNode("link", TextType.LINK, "url")) -> LeafNode("a", "link", {"href": "url"})
    """
    if not isinstance(text_node, TextNode):
        raise ValueError(f"Expected TextNode, got {type(text_node)}")
    
    text_type_name = text_node.text_type.name
    text = text_node.text
    url = text_node.url
    
    match text_type_name:
        case "TEXT":
            return LeafNode(None, text)
        case "BOLD":
            return LeafNode("b", text)
        case "ITALIC":
            return LeafNode("i", text)
        case "CODE":
            return LeafNode("code", text)
        case "LINK":
            if url is None:
                raise ValueError("LINK TextNode requires a URL")
            return LeafNode("a", text, {"href": url})
        case "IMAGE":
            if url is None:
                raise ValueError("IMAGE TextNode requires a URL")
            return LeafNode("img", text, {"src": url})
        case _:
            raise ValueError(f"Unsupported text type: {text_type_name}")


def split_nodes_delimiter(
    old_nodes: List[TextNode], 
    delimiter: str, 
    text_type: TextType
) -> List[TextNode]:
    """
    Split TextNodes by delimiter and convert matching text to specified type.
    
    Only processes nodes with TextType.TEXT. Other node types are preserved as-is.
    
    Args:
        old_nodes: List of TextNodes to process
        delimiter: String delimiter to split by (e.g., "**", "_", "`")
        text_type: TextType enum for the matched content
        
    Returns:
        List of TextNodes with matching content converted to specified type
        
    Raises:
        ValueError: If invalid Markdown syntax (unmatched delimiters)
        
    Examples:
        split_nodes_delimiter([TextNode("**bold**", TEXT)], "**", BOLD) ->
        [TextNode("bold", BOLD)]
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT nodes, preserve others
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_nodes = _split_text_by_delimiter(node.text, delimiter, text_type)
        new_nodes.extend(split_nodes)
    
    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split TextNodes by markdown image syntax and create IMAGE nodes.
    
    Args:
        old_nodes: List of TextNodes to process
        
    Returns:
        List of TextNodes with images converted to IMAGE type nodes
    """
    return split_nodes_image_or_link(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    """
    Split TextNodes by markdown link syntax and create LINK nodes.
    
    Args:
        old_nodes: List of TextNodes to process
        
    Returns:
        List of TextNodes with links converted to LINK type nodes
    """
    return split_nodes_image_or_link(old_nodes, TextType.LINK)


def split_nodes_image_or_link(
    old_nodes: List[TextNode], 
    node_type: TextType
) -> List[TextNode]:
    """
    Split TextNodes by markdown image or link syntax.
    
    Args:
        old_nodes: List of TextNodes to process
        node_type: Either TextType.IMAGE or TextType.LINK
        
    Returns:
        List of TextNodes with images/links converted to appropriate type nodes
        
    Raises:
        ValueError: If node_type is not IMAGE or LINK
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only process TEXT nodes, preserve others
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = _split_text_by_image_or_link(node.text, node_type)
        new_nodes.extend(split_nodes)

    return new_nodes


# Private helper functions
def _split_text_by_image_or_link(text: str, node_type: TextType) -> List[TextNode]:
    """
    Split a single text string by image or link markdown syntax.
    
    Args:
        text: Text to split
        node_type: Either TextType.IMAGE or TextType.LINK
        
    Returns:
        List of TextNodes with the first found image/link converted
        
    Raises:
        ValueError: If node_type is not IMAGE or LINK
    """
    # Extract images or links based on node type
    if node_type == TextType.IMAGE:
        extracts = extract_markdown_images(text)
    elif node_type == TextType.LINK:
        extracts = extract_markdown_links(text)
    else:
        raise ValueError("Can only extract images or links")
    
    # If no images/links found, return original text as TEXT node
    if not extracts:
        return [TextNode(text, TextType.TEXT)]
    
    # Process the first found image/link
    extract_text, url = extracts[0]
    prefix = "!" if node_type == TextType.IMAGE else ""
    markdown_syntax = f"{prefix}[{extract_text}]({url})"
    
    # Find the position of the markdown syntax
    start_pos = text.find(markdown_syntax)
    end_pos = start_pos + len(markdown_syntax)

    # Split the text into before, during, and after
    before_text = text[:start_pos]
    after_text = text[end_pos:]
    
    result = []
    
    # Add before text if it exists
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))
    
    # Add the image/link node
    result.append(TextNode(extract_text, node_type, url))

    # Recursively process remaining text
    if after_text:
        result.extend(_split_text_by_image_or_link(after_text, node_type))

    return result


def _split_text_by_delimiter(
    text: str, 
    delimiter: str, 
    text_type: TextType
) -> List[TextNode]:
    """
    Split a single text string by delimiter and return list of TextNodes.
    
    Args:
        text: Text to split
        delimiter: Delimiter to split by
        text_type: Type for text between delimiters
        
    Returns:
        List of TextNodes with delimited content converted to text_type
        
    Raises:
        ValueError: If invalid Markdown syntax (unmatched delimiters)
    """
    delimiter_length = len(delimiter)
    start_pos = text.find(delimiter)
    
    # If no delimiter found, return original text
    if start_pos == -1:
        return [TextNode(text, TextType.TEXT)]
    
    # Find closing delimiter
    end_pos = text.find(delimiter, start_pos + delimiter_length)
    if end_pos == -1 or (end_pos - start_pos == delimiter_length):
        raise ValueError("Invalid Markdown: unmatched or empty delimiters")
    
    # Split text into parts
    before_text = text[:start_pos]
    between_text = text[start_pos + delimiter_length:end_pos]
    after_text = text[end_pos + delimiter_length:]
    
    result = []
    
    # Add before text if it exists
    if before_text:
        result.append(TextNode(before_text, TextType.TEXT))
    
    # Add the formatted text
    result.append(TextNode(between_text, text_type))
    
    # Recursively process remaining text
    if after_text:
        result.extend(_split_text_by_delimiter(after_text, delimiter, text_type))
    
    return result
