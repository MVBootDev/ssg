from typing import List, Optional, Dict
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    """
    Represents a parent node in the HTML tree structure.
    
    A ParentNode is an HTML element that contains child nodes but no direct text content.
    This includes container elements like <div>, <section>, <ul>, <header>, etc.
    
    Examples:
        ParentNode("div", [LeafNode("p", "Hello")]) -> <div><p>Hello</p></div>
        ParentNode("ul", [LeafNode("li", "Item 1"), LeafNode("li", "Item 2")]) -> <ul><li>Item 1</li><li>Item 2</li></ul>
        ParentNode("section", [child1, child2], {"class": "container"}) -> <section class="container">...</section>
    """
    
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, str]] = None) -> None:
        """
        Initialize a ParentNode.
        
        Args:
            tag: HTML tag name (e.g., 'div', 'section', 'ul'). Required for parent nodes.
            children: List of child HTMLNode instances. Must not be empty.
            props: Optional dictionary of HTML attributes (e.g., {'class': 'container', 'id': 'main'})
        """
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """
        Convert this ParentNode to an HTML string representation.
        
        Returns:
            HTML string representation with all child nodes rendered inside the parent tag
            
        Raises:
            ValueError: If the node has no tag or no children
            
        Examples:
            ParentNode("div", [LeafNode("p", "text")]).to_html() -> "<div><p>text</p></div>"
            ParentNode("ul", [LeafNode("li", "item")], {"class": "list"}).to_html() -> '<ul class="list"><li>item</li></ul>'
        """
        # Parent nodes must have a tag
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
            
        # Parent nodes must have children
        if self.children is None or self.children == []:
            raise ValueError("ParentNode requires at least one child")
        
        # Generate HTML for all children
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
            
        # Generate complete HTML with tag, props, and children
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"