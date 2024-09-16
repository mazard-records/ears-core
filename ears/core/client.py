from typing import Any, Generic

from ..protocols.client import ClientProtocol
from ..protocols.transport import TransportFactory
from ..types import PydanticModelType, TransportClass


class BaseClient(ClientProtocol):
    """
    A base implementation of client protocol
    """

    def __init__(
        self,
        transport_or_factory: TransportClass | TransportFactory,
    ) -> None:
        """
        A default constructor that handles transport managment.

        Args
        ----
            transport_or_factory (TransportClass | TransportFactory):
                Either a ready to use transport instance, or a factory
                instance that can be used to create the delegate transport.
        """
        if isinstance(transport_or_factory, TransportFactory):
            self.transport = transport_or_factory.create()
        else:
            self.transport = transport_or_factory


class ClientModelProxy(Generic[PydanticModelType]):
    """Base proxy class for client extension object."""

    transport: TransportClass

    def __init__(
        self,
        transport: TransportClass,
        model: PydanticModelType,
    ) -> None:
        self.model = model
        self.transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self.model, attr)
