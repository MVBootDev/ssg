from enum import Enum

class TextType(Enum):
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
        