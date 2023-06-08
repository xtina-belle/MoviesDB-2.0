import dataclasses


@dataclasses.dataclass
class OMDBMovieDto:
    """Represents a OMDB movie"""
    name: str
    rating: float
    year: int
    poster: str
