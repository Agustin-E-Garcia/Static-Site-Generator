from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    new_node = None
    if text_node.text_type == TextType.TEXT:
        new_node = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        new_node = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        new_node = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        new_node = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        new_node = LeafNode("a", text_node.text, { "href": text_node.url })
    elif text_node.text_type == TextType.IMAGE:
        new_node = LeafNode("img", "", { "href": text_node.url, "alt": text_node.text })
    else:
        raise Exception(f"Text node type {text_node.text_type} is not a valid TextType")
    
    return new_node