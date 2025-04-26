import unittest

from textnode import TextNode, TextType
from nodeparser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_node_to_html_node


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.IMAGE, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        htmlnode = text_node_to_html_node(node)
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, "This is a text node")

    def test_text_node_to_html_node_with_tag(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node1 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        htmlnode = text_node_to_html_node(node)
        htmlnode1 = text_node_to_html_node(node1)
        self.assertEqual(htmlnode.tag, "b")
        self.assertEqual(htmlnode.value, "This is a text node")
        self.assertEqual(htmlnode1.to_html(), "<a href=\"https://www.google.com\">This is a link</a>")