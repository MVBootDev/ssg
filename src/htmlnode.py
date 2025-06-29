class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not done")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        attrs = []
        for k, v in self.props.items():
            attrs.append(f'{k}="{v}"')
        return f" {' '.join(attrs)} "
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        test1 = self.tag == other.tag
        test2 = self.value == other.value
        test3 = self.children == other.children
        test4 = self.props == other.props
        return test1 and test2 and test3 and test4

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
