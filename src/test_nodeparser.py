import unittest
from nodeparser import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, text_to_textnodes
from textnode import TextNode, TextType

class TestNodeParser(unittest.TestCase):
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

    def test_extract_markdown_images_no_images(self):
        text = "This is text with a rick roll and obi wan"
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_no_links(self):
        text = "This is text with a link to boot dev and to youtube"
        self.assertListEqual(extract_markdown_links(text), [])    

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes
        )

    def test_split_images_trailing(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes
        )

    def test_split_links_trailing(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_text_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual
        (
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )