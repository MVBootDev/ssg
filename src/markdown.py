import re

def extract_markdown_images(text):
    seek = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(seek, text)

def extract_markdown_links(text):
    seek = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(seek, text)