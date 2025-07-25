from typing import Optional, List, Dict, Any


class HTMLNode:
    """
    Base class for HTML node representation in the static site generator.
    
    This class represents an HTML element that can either be:
    - A leaf node (with a value but no children)
    - A parent node (with children but no direct value)
    
    Attributes:
        tag: HTML tag name (e.g., 'p', 'div', 'a')
        value: Text content for leaf nodes
        children: List of child HTMLNode instances for parent nodes
        props: Dictionary of HTML attributes (e.g., {'class': 'highlight', 'id': 'main'})
    """
    
    def __init__(
        self, 
        tag: Optional[str] = None, 
        value: Optional[str] = None, 
        children: Optional[List['HTMLNode']] = None, 
        props: Optional[Dict[str, str]] = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """
        Convert this HTMLNode to an HTML string representation.
        
        Returns:
            HTML string representation of this node and its children
            
        Raises:
            ValueError: If the node has no tag specified
        """
        if self.tag is None:
            raise ValueError("HTMLNode requires a tag to generate HTML")
            
        # Handle leaf nodes (no children)
        if self.children is None or self.children == []:
            content = self.value or ""
            return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"
        
        # Handle parent nodes (with children)
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    
    def props_to_html(self) -> str:
        """
        Convert the props dictionary to HTML attribute string.
        
        Returns:
            String representation of HTML attributes (e.g., ' class="highlight" id="main"')
            Returns empty string if no props exist
        """
        if self.props is None:
            return ""
            
        attrs = []
        for key, value in self.props.items():
            attrs.append(f'{key}="{value}"')
        return f" {' '.join(attrs)}"
    
    def __eq__(self, other: object) -> bool:
        """Check equality with another HTMLNode based on all attributes."""
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self) -> str:
        """Return a string representation of the HTMLNode for debugging."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
