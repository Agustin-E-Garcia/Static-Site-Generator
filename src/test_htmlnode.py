import unittest

from htmlnode import HtmlNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHtmlNode(unittest.TestCase):
    
    def test_to_html_imp(self):
        node = HtmlNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "test": None,
            }
        expected_result = " href=\"https://www.google.com\" target=\"_blank\" test=\"None\""
        node = HtmlNode(props= props)
        self.assertEqual(node.props_to_html(), expected_result)

    def test_repr(self):
        node = HtmlNode("p", "This is a text", None, None)
        self.assertEqual(f"{node}", "HtmlNode(p, This is a text, None, None)")


class TestLeafNode(unittest.TestCase):

    def test_to_html(self):
        node = LeafNode(None, "This is a plain text")
        node1 = LeafNode("p", "This is a paragraph")
        node2 = LeafNode("a", "This is a link", { "href": "https://www.google.com" })
        node3 = LeafNode(None, None)
        self.assertEqual(node.to_html(), "This is a plain text")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph</p>")
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">This is a link</a>")
        self.assertRaises(ValueError, node3.to_html)


class TestParentNode(unittest.TestCase):
    
    def test_to_html_exceptions(self):
        node = ParentNode(None, 
                          [
                              LeafNode("b", "This is a bolded text"),
                              LeafNode("i", "This is an italic text")
                          ])
        node1 = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)
        self.assertRaises(ValueError, node1.to_html)

    def test_to_html_leaf_childs(self):
        node = ParentNode("p", [
                              LeafNode("b", "This is a bolded text"),
                              LeafNode("i", "This is an italic text")
                          ])
        expectedResult = "<p><b>This is a bolded text</b><i>This is an italic text</i></p>"
        self.assertEqual(node.to_html(), expectedResult)

    def test_to_html_parent_childs(self):
                node = ParentNode("p", [
                              LeafNode("b", "This is a bolded text"),
                              ParentNode("p", 
                                         [
                                              LeafNode("a", "This is a link", { "href": "https://www.google.com" }),
                                              LeafNode("b", "This is another bold text")
                                         ]),
                              LeafNode("i", "This is an italic text")
                          ])
                expectedResult = "<p><b>This is a bolded text</b><p><a href=\"https://www.google.com\">This is a link</a><b>This is another bold text</b></p><i>This is an italic text</i></p>"
                self.assertEqual(node.to_html(), expectedResult)



if __name__ == "__main__":
    unittest.main()