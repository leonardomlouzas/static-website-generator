import re
from enum import Enum

from inline_markdown import text_to_textnodes
from textnode import leaf_node_to_html, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    return lines


def block_to_block_type(block):
    lines = block.split("\n")
    num_lines = len(lines)

    if block.startswith("#"):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if num_lines == 1:
        if block.startswith(">"):
            return BlockType.QUOTE

        if block.startswith("- "):
            return BlockType.UNORDERED_LIST

        if block.startswith("1. "):
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH

    if lines[0].startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        raise ValueError("Invalid quote block")

    if lines[0].startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
        raise ValueError("Invalid unordered list block")

    if lines[0].startswith("1. "):
        if all(re.match(r"^\d+\. ", line) for line in lines):
            return BlockType.ORDERED_LIST
        raise ValueError("Invalid ordered list block")

    if lines[0].startswith("```") and not lines[-1].endswith("```\n"):
        raise ValueError("Invalid code block")

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block)
            nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            nodes = [leaf_node_to_html(node) for node in nodes]
            nodes = "<p>" + "".join(nodes) + "</p>"
            all_nodes.append(nodes)

        if block_type == BlockType.CODE:
            all_nodes.append(
                f"<pre><code>{block.replace('```\n', '').replace('```', '')}</code></pre>"
            )

    return f"<div>{''.join(all_nodes)}</div>"
