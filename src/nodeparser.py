from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

# This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

# This is 
# **text**
# with an _italic_ word and a `code block` and an 
# ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)
# and a 
# [link](https://boot.dev)

#[
#    TextNode("This is ", TextType.TEXT),
#    TextNode("text", TextType.BOLD),
#    TextNode(" with an ", TextType.TEXT),
#    TextNode("italic", TextType.ITALIC),
#    TextNode(" word and a ", TextType.TEXT),
#    TextNode("code block", TextType.CODE),
#    TextNode(" and an ", TextType.TEXT),
#    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
#    TextNode(" and a ", TextType.TEXT),
#    TextNode("link", TextType.LINK, "https://boot.dev"),
#]


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "'", TextType.CODE)
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