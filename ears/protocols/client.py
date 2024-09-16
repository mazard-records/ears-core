from typing import Protocol

from ..types import TransportClass


class ClientProtocol(Protocol):
    """
    A protocol for class that carries a transport to interact
    with an external API.
    """

    transport: TransportClass
