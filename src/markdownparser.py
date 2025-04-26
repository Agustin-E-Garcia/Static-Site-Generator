from htmlnode import ParentNode
from blocktype import BlockType
from nodeparser import *

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        blocks.append(block)
    return blocks

def block_to_block_type(block):    
    if block[0] == "#":
        return BlockType.HEADING
    
    if "```" in block[:3] and "```" in block[-3:]:
        return BlockType.CODE
    
    if ">" in block[0]:
        return BlockType.QUOTE
    
    if block[0] == "-":
        return BlockType.UNORDERED_LIST
    
    if block[0].isdigit() and block[1] == ".":
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_children(block):
    children_node = []
    for node in text_to_textnodes(block):
        children_node.append(text_node_to_html_node(node))
    return children_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    if len(blocks) <= 0:
        raise Exception("Parser: markdown text is empty")
    else:
        for block in blocks:
            block_type = block_to_block_type(block)
            block_spaced = " ".join(block.split("\n"))
        
            if block_type == BlockType.CODE:
                block_nodes.append(ParentNode("code", [text_node_to_html_node(TextNode(block, TextType.CODE))]))
        
            elif block_type == BlockType.PARAGRAPH:
                block_nodes.append(ParentNode("p", text_to_children(block_spaced)))
        
            elif block_type == BlockType.QUOTE:
                block_nodes.append(ParentNode("blockquote", text_to_children(block_spaced[1:])))
        
            elif block_type == BlockType.HEADING:
                heading_count = len(re.findall(r"^(#+)", block_spaced)[0])
                if heading_count > 6:
                    heading_count = 6
                block_nodes.append(ParentNode(f"h{heading_count}", text_to_children(block_spaced[heading_count:])))

            elif block_type == BlockType.ORDERED_LIST:
                block_nodes.append(ParentNode("ol", text_to_children(block)))

            elif block_type == BlockType.UNORDERED_LIST:
                block_nodes.append(ParentNode("ul", text_to_children(block)))

    return ParentNode("div", block_nodes)