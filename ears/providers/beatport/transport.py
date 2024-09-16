from ears.core.transport import TransportFactory
from httpx import Client

from .models import BeatportCredentials

BASE_URL = "https://www.beatport.com"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/15.1 Safari/605.1.15"
    ),
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/",
}

LOGIN_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
}


class BeatportTransportFactory(TransportFactory):
    """
    Authenticate to Beatport API with the given credentials,
    after performing some prior call to fill cookies and get a
    valid CSRF token first.
    """

    def __init__(self, credentials: BeatportCredentials) -> None:
        self._credentials = credentials

    def create(self) -> Client:
        transport = Client(
            base_url=BASE_URL,
            headers=DEFAULT_HEADERS,
        )
        transport.get("/api/my-beatport")
        transport.get("/api/account")
        transport.get("/api/csrfcheck")
        csrf_token = transport.cookies.get("_csrf_token")
        if csrf_token is None:
            raise ValueError("Missing CSRF token")
        headers = LOGIN_HEADERS.copy()
        headers["X-CSRFToken"] = csrf_token
        response = transport.post(
            "/api/account/login",
            headers=headers,
            json=self._credentials.model_dump(),
        )
        response.raise_for_status()
        return transport
