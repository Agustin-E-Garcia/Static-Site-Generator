from htmlnode import ParentNode
from blocktype import BlockType
from nodeparser import *

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        blocks.append(block)
    return blocks

def block_to_block_type(block):    
    if block.startswith("#"):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        return BlockType.QUOTE
    
    if block.startswith("-"):
        return BlockType.UNORDERED_LIST
    
    if block[0].isdigit() and block[1] == ".":
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def text_to_children(block):
    children_node = []
    for node in text_to_textnodes(block):
        children_node.append(text_node_to_html_node(node))
    return children_node

def parse_to_paragraph(block):
    return ParentNode("p", text_to_children(block))

def parse_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def parse_to_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def parse_to_heading(block):
        heading_count = len(re.findall(r"^(#+)", block)[0])
        if heading_count > 6:
            heading_count = 6
        return ParentNode(f"h{heading_count}", text_to_children(block.strip("#").strip()))

def parse_to_ordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def parse_to_unordered_list(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

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
                block_nodes.append(parse_to_code(block))
        
            elif block_type == BlockType.PARAGRAPH:
                block_nodes.append(parse_to_paragraph(block))
        
            elif block_type == BlockType.QUOTE:
                block_nodes.append(parse_to_quote(block))
        
            elif block_type == BlockType.HEADING:
                block_nodes.append(parse_to_heading(block))

            elif block_type == BlockType.ORDERED_LIST:
                block_nodes.append(parse_to_ordered_list(block))

            elif block_type == BlockType.UNORDERED_LIST:
                block_nodes.append(parse_to_unordered_list(block))

    return ParentNode("div", block_nodes)