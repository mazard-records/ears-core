from typing import Any, Callable, Optional, TypeVar, Union

from pydantic import BaseModel

Event = dict[str, Any]
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
PydanticEvent = Union[Event, BaseModel]
EventPublisherType = Callable[[Union[dict[str, Any], PydanticEvent]], None]
URN = Optional[str]
