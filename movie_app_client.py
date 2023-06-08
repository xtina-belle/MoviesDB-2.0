import random

from db.movie_storage import MovieDB
from db.movie_dto import MovieDto
from omdb.omdb_api_client import OMDBAPIClient
from youtube.youtube_api_client import YoutubeAPIClient
import web_generator


class MovieAppClient:
    """class to run the movie app"""
    def __init__(self, movie_db: MovieDB):
        self._movie_db = movie_db
        self._omdb_api_client = OMDBAPIClient()
        self._youtube_api_client = YoutubeAPIClient()
        self._website_generator = web_generator.WebGenerator()

    def setup(self):
        """Setting up the movie app client resources"""
        self._movie_db.setup()

    def run_new_account(self):
        print("Your Movie DataBase is empty./nLet's add your first movie!")
        while True:
            self._add_movie()
            if self._movie_db.get_movies():
                break
        self.run()

    def run(self):
        """Prints a menu and display user's choice result"""
        print("** My Movies Database **\n")
        while True:
            print("Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Generate website\n")

            user_answer = input("Enter choice (0-9): ")
            print("\n")
            if user_answer == "0":
                print("Bye!")
                break
            if user_answer == "1":
                self._read_movies()
            elif user_answer == "2":
                self._add_movie()
            elif user_answer == "3":
                self._delete_movie()
            elif user_answer == "4":
                self._update_movie()
            elif user_answer == "5":
                self._stats()
            elif user_answer == "6":
                self._random_movie()
            elif user_answer == "7":
                self._search_movie()
            elif user_answer == "8":
                self._sorted_by_rating()
            elif user_answer == "9":
                self._generate_website()
                print("Website was generated successfully.")
            else:
                print("Invalid choice")
                continue

            input("\nPress enter to continue")

    def _add_movie(self):
        """Ask movie name which user want to add.
        If it's not in database, adds it from API loaded data"""
        name = input("Enter new movie name: ").capitalize()
        if not self._movie_db.is_movie_exist(name):
            omdb_movie_dto = self._omdb_api_client.get_omdb_movie(name)
            trailer_dto = self._youtube_api_client.get_trailer(name)
            if omdb_movie_dto and trailer_dto:
                self._movie_db.upsert(MovieDto(
                    name=omdb_movie_dto.name,
                    rating=omdb_movie_dto.rating,
                    year=omdb_movie_dto.year,
                    poster=omdb_movie_dto.poster,
                    trailer_id=trailer_dto.trailer_id,
                ))
                print(f"Movie {name} successfully added")
        else:
            print(f"Movie {name} already exist!")

    def _read_movies(self):
        """prints all movie's in database"""
        print(self._movie_db)

    def _delete_movie(self):
        """Ask movie name from user and delete it if exists"""
        name = input("Enter movie name to delete: ")
        if self._movie_db.is_movie_exist(name):
            self._movie_db.delete(name.title())
            print(f"Movie {name} successfully deleted")
        else:
            print(f"Movie {name} doesn't exist!")

    def _update_movie(self):
        """Ask movie name from user and add user's description if movie exists"""
        name = input("Enter movie name: ").capitalize()
        movie = self._movie_db.get_movie(name)
        if movie:
            movie.note = input("Enter movie notes: ")
            self._movie_db.upsert(movie)
            print(f"Movie {name} successfully updated")
        else:
            print(f"Movie {name} doesn't exist!")

    def _stats(self):
        """Print database statistics"""
        print(f"Average rating: {self._movie_db.get_average_rating()}")
        print(f"Median rating: {self._movie_db.get_median_rating()}")
        print("Best movie: ")
        for best in self._movie_db.get_best_movies():
            print(f"\t{best}")
        print("Worst movie: ")
        for worst in self._movie_db.get_worst_movies():
            print(f"\t{worst}")

    def _random_movie(self):
        """Prints a random movie from database"""
        title_to_movie_dto = self._movie_db.get_movies()
        name = random.choice(list(title_to_movie_dto.keys()))
        print(f"Your movie for tonight: {name}, it's rated {title_to_movie_dto[name].rating}")

    def _search_movie(self):
        """Search for movie in database by its partial name"""
        part_name = input("Enter part of movie name: ")
        search_result = self._movie_db.search_movie(part_name)
        if search_result:
            for movie_dto in search_result:
                print(movie_dto)
        else:
            print(f"Movie {part_name} not found")

    def _sorted_by_rating(self):
        """Prints all movies in database ordered by descending rating"""
        for _, movie_dto in self._movie_db.sort_by_rating().items():
            print(movie_dto)

    def _generate_website(self):
        """generates the html for the movie web application"""
        title_to_movie_dto = self._movie_db.get_movies()
        content = self._website_generator.get_html_content(title_to_movie_dto)
        self._website_generator.fill_template_html(content)
