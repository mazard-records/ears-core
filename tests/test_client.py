from httpx import Client
from pydantic import BaseModel
from pytest_mock import MockerFixture

from ears.core.client import BaseClient, ClientModelProxy
from ears.protocols.transport import TransportFactory
from ears.types import TransportClass


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


class ModelMock(BaseModel):
    foo: str


class ClientModelProxyMock(ClientModelProxy[ModelMock]):
    pass


def test_attribute_proxy() -> None:
    model = ModelMock(foo="bar")
    transport = Client()
    proxy = ClientModelProxyMock(transport, model)
    assert proxy.model == model
    assert proxy.transport == transport
    assert proxy.foo == "bar"
