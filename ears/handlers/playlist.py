from ..core.events import PlaylistAction, PlaylistEvent
from ..core.provider import BaseMusicProvider
from ..protocols.messaging import EventPublisherFactory, EventReceiver
from ..types import Event


def on_broadcast_playlist_event(
    event: Event,
    provider: BaseMusicProvider,
    event_publisher_factory: EventPublisherFactory,
    event_receiver: EventReceiver,
    destination: str,
) -> None:
    """ """
    event_publisher = event_publisher_factory.create(destination)
    playlist_event = event_receiver.receive(event, PlaylistEvent)
    if playlist_event.action != PlaylistAction.broadcast:
        raise ValueError(
            "Invalid playlist event type received, "
            f"expected 'broadcast', got '{playlist_event.action.value}'"
        )
    tracks = provider.get_playlist(playlist_event.playlist)
    for track in tracks:
        event_publisher.publish(track)


def on_update_playlist_event(
    event: Event,
    provider: BaseMusicProvider,
    event_receiver: EventReceiver,
) -> None:
    """ """
    playlist_event = event_receiver.receive(event, PlaylistEvent)
    if playlist_event.action == PlaylistAction.add:
        if playlist_event.track is None:
            raise ValueError("Missing track URN")
        provider.add_to_playlist(
            playlist_event.playlist,
            playlist_event.track,
        )
    elif playlist_event.action == PlaylistAction.remove:
        if playlist_event.track is None:
            raise ValueError("Missing track URN")
        provider.remove_from_playlist(
            playlist_event.playlist,
            playlist_event.track,
        )
    else:
        raise ValueError(
            "Invalid playlist event type received, "
            "expected 'add' or 'remove', "
            f"got '{playlist_event.action.value}'"
        )
