from ..core.models import Track, TrackMatching
from ..core.provider import BaseMusicProvider
from ..protocols.messaging import EventPublisherFactory, EventReceiver
from ..types import Event


def on_search_track_event(
    event: Event,
    provider: BaseMusicProvider,
    event_publisher_factory: EventPublisherFactory,
    event_receiver: EventReceiver,
    destination: str,
) -> None:
    """ """
    event_publisher = event_publisher_factory.create(destination)
    query = event_receiver.receive(event, Track)
    results = provider.search_track(query.metadata)
    if len(results) == 0:
        # TODO: figure out what to do here ?
        return
    event_publisher.publish(
        TrackMatching(
            origin=query.resource,
            destination=results[0].resource,
            metadata=results[0].metadata,
        )
    )
