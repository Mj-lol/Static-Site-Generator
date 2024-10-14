

class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:list =None, props:dict=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props)
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    def props_to_html(self):
        s = ""
        if self.props:
            for e in self.props:
                s+= f' {e}="{self.props[e]}"'
        return s

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
