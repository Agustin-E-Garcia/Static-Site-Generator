import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from main import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

    def test_split_nodes_delimeter_italic(self):
        node = TextNode("This is a text with an _italic_ word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), 
                         [
                            TextNode("This is a text with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT)
                         ])
        
    def test_split_nodes_delimeter_bold(self):
        node = TextNode("This is a text with a **bold** word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
                         [
                            TextNode("This is a text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.TEXT)
                         ])
        
    def test_split_nodes_delimeter_code(self):
        node = TextNode("This is a text with a 'code' word", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "'", TextType.CODE), 
                         [
                            TextNode("This is a text with a ", TextType.TEXT),
                            TextNode("code", TextType.CODE),
                            TextNode(" word", TextType.TEXT)
                         ])
        
    def test_split_nodes_delimeter_single_word(self):
        node = TextNode("'code'", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "'", TextType.CODE), 
                         [
                            TextNode("", TextType.TEXT),
                            TextNode("code", TextType.CODE),
                            TextNode("", TextType.TEXT)
                         ])
        
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

if __name__ == "__main__":
    unittest.main()