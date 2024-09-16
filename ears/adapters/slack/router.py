import json
from typing import Callable, Dict, Optional
from urllib.parse import urlparse

from flask import Request, Response, jsonify
from httpx import post
from pydantic import AnyHttpUrl, BaseModel

from .blocks import MarkdownBlocks
from .interactions import BlockInteraction, InteractionDeleteResponse


class CommandSyntaxError(ValueError):
    def to_response(self) -> Response:
        return jsonify(MarkdownBlocks(":warning: invalid syntax\n" f"> {self}"))


def EmptyCommandResponse() -> Response:
    return jsonify(MarkdownBlocks(":warning: empty command received"))


def InvalidCommandResponse(command: str) -> Response:
    return jsonify(MarkdownBlocks(f":warning: unknown command {command}"))


def ExecutionErrorResponse(e: Exception) -> Response:
    return jsonify(MarkdownBlocks(f":x: unexpected error\n> {e}"))


class CommandRequestPayload(BaseModel):
    token: str
    team_id: str
    team_domain: str
    entreprise_id: str
    entreprise_name: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    text: str
    response_url: AnyHttpUrl
    trigger_id: str
    api_app_id: str


def CommandRequest(request: Request) -> CommandRequestPayload:
    body = request.get_data().decode("utf-8")
    return CommandRequestPayload(
        **dict(component.split("=") for component in body.split("&"))
    )


def InteractionRequest(request: Request) -> BlockInteraction:
    payload = request.form.get("payload")
    if payload is None:
        raise ValueError("Missing expected payload")
    return BlockInteraction(**json.loads(payload))


CommandHandlerType = Callable[[CommandRequestPayload], Optional[Response]]
InteractionHandlerType = Callable[[str], Optional[Response]]


class Router:
    COMMAND = "/ears"
    SCHEME = "ears"

    def __init__(
        self,
    ) -> None:
        self._command_handlers: Dict[str, CommandHandlerType] = {}
        self._interaction_handlers: Dict[str, InteractionHandlerType] = {}

    def register_command(
        self,
        action: str,
        handler: CommandHandlerType,
    ) -> None:
        self._command_handlers[action] = handler

    def register_interaction(
        self,
        domain: str,
        handler: InteractionHandlerType,
    ) -> None:
        self._interaction_handlers[domain] = handler

    def serve_command_request(
        self,
        request: Request,
    ) -> Optional[Response]:
        payload = CommandRequest(request)
        if payload.command != self.COMMAND:
            return InvalidCommandResponse(payload.command)
        args = payload.text.split()
        if len(args) == 0:
            return EmptyCommandResponse()
        subcommand = self._command_handlers.get(args[0])
        if subcommand is None:
            return InvalidCommandResponse(f"{payload.command} subcommand")
        try:
            subcommand(payload)
        except CommandSyntaxError as e:
            return e.to_response()
        except Exception as e:
            return ExecutionErrorResponse(e)
        return None

    def serve_interaction_request(
        self,
        request: Request,
    ) -> Optional[Response]:
        interaction = InteractionRequest(request)
        try:
            for action in interaction.actions:
                resource = urlparse(action.value)
                if resource.scheme != self.SCHEME:
                    raise ValueError(f"Invalid url scheme {resource.scheme}")
                if resource.netloc not in self._interaction_handlers:
                    raise ValueError(f"Invalid domain {resource.netloc}")
                handler = self._interaction_handlers[resource.netloc]
                handler(resource.path)
            response = post(
                interaction.response_url,
                json=InteractionDeleteResponse().model_dump(),
            )
            response.raise_for_status()
        except Exception:
            # TODO: process with feedback / log.
            # TODO: return error response.
            pass
        return None
