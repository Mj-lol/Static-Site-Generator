from htmlnode import *

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
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
