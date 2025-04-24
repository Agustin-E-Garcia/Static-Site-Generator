from textnode import TextNode, TextType
from re import findall

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            temp = node.text.split(delimiter)
            if len(temp) < 3:
                raise Exception(f"Exception parsing line: \"{node.text}\" for {text_type}. Syntax error")
            else:
                new_nodes.append(TextNode(temp[0], TextType.TEXT))
                new_nodes.append(TextNode(temp[1], text_type))
                new_nodes.append(TextNode(temp[2], TextType.TEXT))
            
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.IMAGE:
            new_nodes.append(node)
        else:
            pass



def split_nodes_link(old_nodes):
    pass

def extract_markdown_images(text):
    return findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return findall(r"\[(.*?)\]\((.*?)\)", text)

def main():
    pass

if __name__ == "__main__":
    main()