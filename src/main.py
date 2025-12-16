from textnode import *
from make_public import *

def main():
    sampleNode = TextNode("hello", TextType.TEXT, "http://www.boot.dev")
    print(sampleNode)
    distribute("static", "public")

main()
