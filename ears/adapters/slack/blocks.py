from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ElementType(str, Enum):
    actions = "actions"
    button = "button"
    context = "context"
    divider = "divider"
    image = "image"
    markdown = "mrkdwn"
    plain_text = "plain_text"
    section = "section"


class Style(str, Enum):
    danger = "danger"
    primary = "primary"


class Block(BaseModel):
    type: str


class Blocks(BaseModel):
    blocks: List[Block]


class Element(BaseModel):
    pass


class Divider(Block):
    type: str = ElementType.divider.value


class PlainText(Block):
    type: str = ElementType.plain_text.value
    emoji: bool = True
    text: str


class Button(Block):
    type: str = ElementType.button.value
    style: str = Style.primary.value
    text: PlainText
    value: str


class Image(Block, Element):
    type: str = ElementType.image.value
    alt_text: str = ""
    image_url: str


class Markdown(Block, Element):
    type: str = ElementType.markdown.value
    text: str


class Context(Block):
    type: str = ElementType.context.value
    elements: List[Element]


class Section(Block):
    type: str = ElementType.section.value
    text: Markdown
    accessory: Optional[Image] = None


class Actions(Block):
    type: str = ElementType.actions.value
    elements: List[Button]


def MarkdownBlocks(text: str) -> Blocks:
    return Blocks(
        blocks=[
            Section(
                text=Markdown(
                    text=text,
                )
            )
        ]
    )
