import dataclasses


@dataclasses.dataclass
class YoutubeTrailerDto:
    """Represents a youtube trailer"""
    trailer_id: str
