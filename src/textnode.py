from enum import Enum

class TextType(Enum):
    PLAIN = "plain text"
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