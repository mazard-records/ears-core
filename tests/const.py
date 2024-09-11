from ears.core.models import MusicResourceType

TEST_INVALID_URNS = (None, "a:b:c:d:e", "ftp:a:b:c")
TEST_INVALID_PROVIDER_URNS = ("urn:apple:track:12", "urn:deezer:movie:23")

TEST_VALID_URN = "urn:spotify:track:69"
TEST_VALID_URN_ID = "69"
TEST_VALID_URN_PROVIDER = "spotify"
TEST_VALID_URN_TYPE = MusicResourceType.track
