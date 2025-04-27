from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    return text_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            temp = node.text.split(delimiter)
            if len(temp) == 1:
                new_nodes.append(TextNode(temp[0], TextType.TEXT))
            elif len(temp) < 3:
                raise Exception(f"Exception parsing line: \"{node.text}\" for {text_type}. Syntax error")
            else:
                new_nodes.append(TextNode(temp[0], TextType.TEXT))
                new_nodes.append(TextNode(temp[1], text_type))
                new_nodes.append(TextNode(temp[2], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) <= 0:
            new_nodes.append(node)
        else:
            text = node.text
            for alt, link in images:
                text = text.split(f"![{alt}]({link})", 1)
                if len(text[0]) > 0:
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, link))
                text = text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) <= 0:
            new_nodes.append(node)
        else:
            text = node.text
            for alt, link in links:
                text = text.split(f"[{alt}]({link})", 1)
                if len(text[0]) > 0:
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, link))
                text = text[1]
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

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
    elif text_node.text_type == TextType.LIST_ITEM:
        new_node = LeafNode("li", text_node.text)
    else:
        raise Exception(f"Text node type {text_node.text_type} is not a valid TextType")
    
    return new_node