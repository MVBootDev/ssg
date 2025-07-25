from typing import Optional, Dict
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    Represents a leaf node in the HTML tree structure.
    
    A LeafNode is an HTML element that contains only text content and has no children.
    This includes elements like <p>, <b>, <i>, <a>, and raw text nodes.
    
    Examples:
        LeafNode("p", "Hello world") -> <p>Hello world</p>
        LeafNode("b", "Bold text") -> <b>Bold text</b>
        LeafNode(None, "Raw text") -> Raw text
        LeafNode("a", "Link", {"href": "http://example.com"}) -> <a href="http://example.com">Link</a>
    """
    
    def __init__(self, tag: Optional[str], value: str, props: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize a LeafNode.
        
        Args:
            tag: HTML tag name (e.g., 'p', 'b', 'i', 'a'). None for raw text nodes.
            value: Text content of the node. Required for all leaf nodes.
            props: Optional dictionary of HTML attributes (e.g., {'href': 'url', 'class': 'highlight'})
        """
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """
        Convert this LeafNode to an HTML string representation.
        
        Returns:
            HTML string representation. If no tag is specified, returns raw value.
            If tag is specified, returns value wrapped in the tag with any props.
            
        Raises:
            ValueError: If the node has a tag but no value
            
        Examples:
            LeafNode("p", "text").to_html() -> "<p>text</p>"
            LeafNode(None, "text").to_html() -> "text"
            LeafNode("a", "link", {"href": "url"}).to_html() -> '<a href="url">link</a>'
        """
        # Handle raw text nodes (no HTML tag)
        if not self.tag:
            return self.value
            
        # Leaf nodes with tags must have values
        if self.value is None:
            raise ValueError("LeafNode with a tag requires a value")
            
        # Generate HTML with tag and props
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"