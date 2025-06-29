from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        if self.value is None:
            raise ValueError("value is required")
        return f"<{self.tag}>{self.value}</{self.tag}>"