from functools import wraps
from hashlib import sha256
from hmac import new as hmac
from time import time
from typing import Any, Callable, Mapping, Protocol, Union, cast


class RequestProtocol(Protocol):
    """A headers provider interface for duck typing."""

    @property
    def headers(self) -> Mapping[str, Any]:
        pass

    def get_data(self) -> bytes:
        pass


Endpoint = Callable[[RequestProtocol], Any]
StringProvider = Callable[..., str]


class SlackHeaders(object):
    X_SLACK_SIGNATURE = "X-Slack-Signature"
    X_SLACK_REQUEST_TIMESTAMP = "X-Slack-Request-Timestamp"


class InvalidSignatureError(ValueError):
    pass


class ExpiredTimestampError(ValueError):
    pass


def compute_slack_signature(
    request: RequestProtocol,
    signing_secret: str,
    version: str,
) -> str:
    """Compute a Slack signature from the given request."""
    timestamp = request.headers.get(SlackHeaders.X_SLACK_REQUEST_TIMESTAMP)
    if abs(time() - float(cast(int, timestamp))) > 60 * 5:
        raise ExpiredTimestampError()
    body = request.get_data().decode("utf-8")
    message = f"{version}:{timestamp}:{body}"
    signature = hmac(
        signing_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=sha256,
    )
    return f"{version}={signature.hexdigest()}"


def verify_slack_signature(
    signing_secret: Union[str, StringProvider],
    version: str = "v0",
) -> Callable[[Endpoint], Endpoint]:
    """
    Decorator that acts as middleware to ensure that an
    incoming HTTP request is a valid issued Slack request.

    See https://api.slack.com/authentication/verifying-requests-from-slack
    """

    def wrapper(endpoint: Endpoint) -> Endpoint:
        @wraps(endpoint)
        def middleware(request: RequestProtocol) -> Any:
            if isinstance(signing_secret, str):
                secret = signing_secret
            else:
                secret = signing_secret()
            expected = request.headers.get(SlackHeaders.X_SLACK_SIGNATURE)
            actual = compute_slack_signature(
                request,
                secret,
                version,
            )
            if actual != expected:
                raise InvalidSignatureError()
            return endpoint(request)

        return middleware

    return wrapper
