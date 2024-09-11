from httpx import Client
from pytest_mock import MockerFixture

from ears.core.client import BaseClient
from ears.core.transport import TransportFactory
from ears.core.types import TransportClass


def test_base_client_init_with_transport() -> None:
    transport = Client()
    client = BaseClient(transport)
    assert client.transport == transport


def test_base_client_init_with_transport_factory(mocker: MockerFixture) -> None:
    transport = Client()

    class TransportFactoryMock(TransportFactory):
        def create(self) -> TransportClass:
            return transport

    transport_factory = TransportFactoryMock()
    transport_factory_spy = mocker.spy(transport_factory, "create")
    client = BaseClient(transport_factory)
    transport_factory_spy.assert_called_once()
    assert client.transport == transport
