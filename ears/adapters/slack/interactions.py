from typing import List

from pydantic import BaseModel


class BlockAction(BaseModel):
    type: str
    block_id: str
    action_id: str
    value: str
    action_ts: str


class BlockInteraction(BaseModel):
    type: str
    actions: List[BlockAction]
    response_url: str


class InteractionDeleteResponse(BaseModel):
    delete_original: bool = True


class InteractionReplaceResponse(BaseModel):
    replace_original: bool = True
    text: str
