from enum import Enum
from htmlnode import *
import re

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
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new =[]
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new.append(node)
        else:
            parts = node.text.split(delimiter)
            is_delimited = False
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiter found in text.")
            for part in parts:
                if part:
                    if is_delimited:
                        new_node = TextNode(part, text_type)
                    else:
                        new_node = TextNode(part, TextType.TEXT)
                    new.append(new_node)
                is_delimited = not is_delimited

    return new
def extract_markdown_images(text):
    # Regex to match markdown image format ![alt](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    # Regex to match markdown link format [anchor](url), but exclude images
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
def split_nodes_image(old_nodes):
    new =[]
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new.append(node)
            continue

        for alt, url, in images:
            secs = text.split(f"![{alt}]({url})", 1)
            if len(secs) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if secs[0]:
                new.append(TextNode(secs[0], TextType.TEXT))
            new.append(TextNode(alt, TextType.IMAGE, url))
            text = secs[1] if len(secs)>1 else ""
        if text:
            new.append(TextNode(text, TextType.TEXT))
    return new
def split_nodes_link(old_nodes):
    new =[]
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new.append(node)
            continue

        for anchor, url, in links:
            secs = text.split(f"[{anchor}]({url})", 1)
            if len(secs) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if secs[0]:
                new.append(TextNode(secs[0], TextType.TEXT))
            new.append(TextNode(anchor, TextType.LINK, url))
            text = secs[1] if len(secs)>1 else ""
        if text:
            new.append(TextNode(text, TextType.TEXT))
    return new


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks
def block_to_block_type(block):
    if block.startswith('# '):
        return 'heading'
    if any(block.startswith(f'{"#"*i} ') for i in range(2, 7)):
        return 'heading'

    if block.startswith('```') and block.endswith('```'):
        return 'code'

    if all(line.strip().startswith('>') for line in block.split('\n')):
        return 'quote'

    if all(line.strip().startswith(('* ', '- ')) for line in block.split('\n')):
        return 'unordered_list'

    lines = block.split('\n')
    if all(line.strip().split('.')[0].isdigit() for line in lines):
        try:
            numbers = [int(line.split('.')[0].strip()) for line in lines]
            if numbers == list(range(1, len(numbers) + 1)):
                return 'ordered_list'
        except ValueError:
            pass

    return 'paragraph'

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes=[]
    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case "paragraph":
                text = text_to_textnodes(block)
                html= [text_node_to_html_node(tn) for tn in text]
                p = ParentNode('p', html)
                nodes.append(p)
            case "heading":
                lines = block.split('\n')
                head = lines[0]
                level = 0
                for char in head:
                    if char == '#':
                        level += 1
                    else:
                        break
                t = head[level:].strip()
                text_nodes = text_to_textnodes(t)
                html= [text_node_to_html_node(tn) for tn in text_nodes]
                tag = f"h{level}"
                hn = ParentNode(tag, html)
                nodes.append(hn)
            case "code":
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("Invalid code block")
                cl = block.split('\n')
                cc = '\n'.join(cl[1:-1])
                cn = LeafNode(None, cc)
                cpn = ParentNode('code', [cn])
                pn= ParentNode('pre', [cpn])
                nodes.append(pn)
            case "quote":
                lines = block.split('\n')
                ql = []
                for line in lines:
                    if not line.startswith('>'):
                        raise ValueError("Invalid quote block")
                    ql.append(line.lstrip('>').strip())
                qt = ' '.join(ql)
                tn = text_to_textnodes(qt)
                html = [text_node_to_html_node(t) for t in tn]
                qn = ParentNode('blockquote', html)
                nodes.append(qn)
            case "unordered_list":
                lines = block.split('\n')
                ln=[]
                for line in lines:
                    if not line.strip().startswith(('*', '-')):
                        raise ValueError("Invalid unordered list item")
                    line = line.lstrip('*- ').strip()
                    tn = text_to_textnodes(line)
                    html = [text_node_to_html_node(t) for t in tn]
                    li = ParentNode('li', html)
                    ln.append(li)
                un=ParentNode('ul', ln)
                nodes.append(un)
            case "ordered_list":
                lines = block.split('\n')
                ln=[]
                for line in lines:
                    line = re.sub(r'^\d+\.\s*', '', line).strip()
                    tn = text_to_textnodes(line)
                    html = [text_node_to_html_node(t) for t in tn]
                    li = ParentNode('li', html)
                    ln.append(li)
                ol=ParentNode('ol', ln)
                nodes.append(ol)

            case _:
                raise ValueError(f"Unknown block type: {block_type}")
    root_node = ParentNode('div', nodes)
    return root_node
