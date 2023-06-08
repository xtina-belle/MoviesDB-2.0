import dataclasses
import typing


@dataclasses.dataclass
class MovieDto:
    """Represents a Movie"""
    name: str
    rating: float
    year: int
    poster: str
    trailer_id: str
    note: typing.Optional[str] = None

    @classmethod
    def get_instance(cls, title, movie_data: dict):
        """Gets movie title and movie data and returns an instance of the class"""
        return cls(
            name=title,
            rating=movie_data["rate"],
            year=movie_data["year"],
            poster=movie_data["poster"],
            trailer_id=movie_data["trailer_id"],
            note=movie_data.get("note"),
        )

    def to_dict(self) -> dict:
        """returns a dictionary that represents the movie data object"""
        data = {
            "rate": self.rating,
            "year": self.year,
            "poster": self.poster,
            "trailer_id": self.trailer_id,
        }
        if self.note:
            data["note"] = self.note
        return data

    def __iter__(self):
        return iter([self.name, self.rating, self.year, self.poster, self.trailer_id, self.note])

    def __str__(self):
        return f"{self.name} ({self.year}): {self.rating}"
