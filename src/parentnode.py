from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("need a tag dude")
        if self.children is None or self.children == []:
            raise ValueError("parents need children")
        child_nodes = []
        for item in self.children:
            child_nodes.append(item.to_html())
        return f"<{self.tag}>{''.join(child_nodes)}</{self.tag}>"