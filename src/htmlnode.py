class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        string_prop = ""
        if self.props != None:
            for prop in self.props:
                string_prop += f" {prop}=\"{self.props[prop]}\""
        return string_prop
    
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode.value cannot be none")
        
        if self.tag == None:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode.tag cannot be None")
        
        if self.children == None:
            raise ValueError("ParentNode.children cannot be None")
        
        html_string = f"<{self.tag}>"
        for node in self.children:
            html_string += node.to_html()
        html_string += f"</{self.tag}>"

        return html_string