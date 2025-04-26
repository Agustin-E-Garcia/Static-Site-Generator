import unittest
from markdownparser import markdown_to_blocks, block_to_block_type, markdown_to_html_node, text_to_children
from blocktype import BlockType
from htmlnode import LeafNode

class TestMarkdownPaerser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertListEqual
        (
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_paragrahp(self):
        block = ["This is a paragraph"]
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        blocks = [ "``` this is a code block ```", "`` this is a code block ``", "this is a code block", "this is a code block ```", "``````" ]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.CODE)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.CODE)

    def test_block_to_block_type_unordered_list(self):
        blocks = [ "- item 1\n - item 2\n", "item 1\n item 2", "-" ]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        blocks = [ "1. item 1\n 2. item 2", "1- item 1\n 2- item 2" ]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)

    def test_block_to_block_Type_heading(self):
        blocks = [ "# title", "## title", "##### title", "title" ]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        blocks = [ "> quote", ">> quote", ">quote", "quote>", ">"]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.QUOTE)

    def test_text_to_children_unordered_lists(self):
        block = "- This is a list\n- with items"
        children = text_to_children(block)
        self.assertListEqual(
            [
                LeafNode("li", "This is a list"),
                LeafNode("li", "with items")
            ],
            children
            )
        
    def test_text_to_children_ordered_lists(self):
        block = "1. This is a list\n 2. with items"
        children = text_to_children(block)
        self.assertListEqual(
            [
                LeafNode("li", "This is a list"),
                LeafNode("li", "with items")
            ],
            children
            )
        
    def test_text_to_children_extra_lists(self):
        block = "1. This is a list\n - with items\n and more"
        children = text_to_children(block)
        self.assertListEqual(
            [
                LeafNode("li", "This is a list"),
                LeafNode("li", "with items")
            ],
            children
            )
        
    def test_markdown_to_html_node(self):
        markdown = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node(self):
        self.maxDiff = None
        markdown = """# This is the title\n\n## This is a subtitle\n\n- point 1\n - point 2\n -point 3\n\n>Remember me, remember me"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1> This is the title</h1><h2> This is a subtitle</h2><ul><li>point 1</li><li>point 2</li><li>point 3</li></ul><blockquote>Remember me, remember me</blockquote></div>"
        )