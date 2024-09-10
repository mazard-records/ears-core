from typing import Any, Callable, TypeVar, Union

from httpx import AsyncClient, Client
from pydantic import BaseModel

Event = dict[str, Any]

# TODO: bound to base type.
ModelClass = TypeVar("ModelClass", bound=...)

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)

PydanticEvent = Union[Event, BaseModel]

TransportClass = TypeVar("_TransportClass", AsyncClient, Client)

URN = str

EventPublisherType = Callable[[Union[dict[str, Any], PydanticEvent]], None]
