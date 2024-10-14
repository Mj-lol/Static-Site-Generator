from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list,props:dict=None) -> None:
        if children is None:
            raise ValueError("children is required")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("children are required")

        html_output = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html_output += child.to_html()

        html_output += f"</{self.tag}>"
        return html_output
