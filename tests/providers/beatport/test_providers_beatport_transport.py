import json

from pytest_httpx import HTTPXMock

from ears.provider.beatport.models import BeatportCredentials
from ears.provider.beatport.transport import BASE_URL, BeatportTransportFactory


def before_create_transport(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/api/my-beatport",
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/api/account",
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{BASE_URL}/api/csrfcheck",
        headers={"set-cookie": "_csrf_token=hack"},
    )
    httpx_mock.add_response(
        method="POST",
        url=f"{BASE_URL}/api/account/login",
    )


def after_create_transport(httpx_mock: HTTPXMock) -> None:
    for prior in ("my-beatport", "account", "csrfcheck"):
        requests = httpx_mock.get_requests(
            url=f"{BASE_URL}/api/{prior}",
            method="GET",
        )
        assert len(requests) == 1
    requests = httpx_mock.get_requests(
        method="POST",
        url=f"{BASE_URL}/api/account/login",
    )
    assert len(requests) == 1
    assert requests[0].headers.get("X-CSRFToken") == "hack"
    payload = json.loads(requests[0].content.decode("utf-8"))
    assert payload.get("username") == "Faylixe"
    assert payload.get("password") == "You wish"
    assert not payload.get("remember")


def test_create_transport(httpx_mock: HTTPXMock) -> None:
    before_create_transport(httpx_mock)
    credentials = BeatportCredentials(username="Faylixe", password="You wish")
    transport_factory = BeatportTransportFactory(credentials)
    transport_factory.create()
    after_create_transport(httpx_mock)
