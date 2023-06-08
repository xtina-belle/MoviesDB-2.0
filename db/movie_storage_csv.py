import csv

from db.movie_storage import MovieDB
from db.movie_dto import MovieDto

DB_CSV_FILE = "moviesDB.csv"


class MovieDBCsv(MovieDB):
    def setup(self):
        """Loading the DB data to memory"""
        with open(self._movie_db, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                name, rate, year, poster, trailer_id, note = row
                note = None if note == "" else note
                self._title_to_movie_dto[name] = MovieDto(
                    name, float(rate), int(year), poster, trailer_id, note
                )

    def _flush_data(self):
        """Flush self._title_to_movie_dto to the csv file"""
        with open(self._movie_db, "w") as file:
            writer = csv.writer(file)
            writer.writerows(self._title_to_movie_dto.values())
