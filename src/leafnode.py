from htmlnode import *
from textnode import *
class LeafNode(HTMLNode):
    def __init__(self, tag:str,value:str, props:dict=None) -> None:
        if value is None:
            raise ValueError("value is required")
        super().__init__(tag=tag, value=value, children=None, props=props)



    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")

        if self.tag is None:
            return self.value
        elif self.tag in ["img", "br", "hr", "meta", "link"]:
            return f"<{self.tag}{self.props_to_html()} />"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


    # class TextNode:
    # def __init__(self, TEXT, TEXT_TYPE, URL=None)
def text_node_to_html_node(text_node: TextNode):

    match text_node.text_type:
        case "text":
            return LeafNode(tag=None, value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            if text_node.url is None:
                raise ValueError("URL is required for link text type")

            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case "image":
            if text_node.url is None:
                raise ValueError("URL is required for image text type")

            return LeafNode(tag="img", value="", props= {"src": text_node.url,"alt":text_node.text})
        case _:
            raise ValueError("invalid node type")
