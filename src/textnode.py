from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None) -> None:
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url ==value.url
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
def text_node_to_html_node(text_node: TextNode):

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL is required for link text type")

            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL is required for image text type")

            return LeafNode(tag="img", value="", props= {"src": text_node.url,"alt":text_node.text})
        case _:
            raise ValueError("invalid node type")
