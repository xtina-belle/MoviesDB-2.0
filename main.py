from argparse import ArgumentParser
import os

from movie_app_client import MovieAppClient
from db.movie_storage_json import MovieDBJson
from db.movie_storage_csv import MovieDBCsv


def main():
    """A runner for the command-line and app"""
    directory = "db"
    file_list = [file for file in os.listdir(directory) if ".json" in file or ".csv" in file]

    parser = ArgumentParser()
    parser.add_argument("db", nargs='?', help='File to open')
    parser.add_argument('--add', metavar='DB_FILE', help='Specify a file to add')
    args = parser.parse_args()
    if args.db:
        if args.db in file_list:
            account = "db/" + args.db
            db = MovieDBCsv(account) if ".csv" in args.db else MovieDBJson(account)
            client = MovieAppClient(db)
            client.setup()
            client.run()
        else:
            print("Account doesn't exist!")
            print("To add a new account enter: --add DB_FILE")

    if args.add:
        account = "db/" + args.add
        if ".csv" in args.add or ".json" in args.add:
            db = MovieDBCsv(account) if ".csv" in args.add else MovieDBJson(account)
            client = MovieAppClient(db)
            client.run_new_account()
        else:
            print("Not supportable file extension!")


if __name__ == "__main__":
    main()
