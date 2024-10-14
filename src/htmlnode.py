

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
