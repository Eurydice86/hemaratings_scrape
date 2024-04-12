import argparse
import os

from src import clubs, events, fighters, ratings


def clear():
    # for windows
    if os.name == "nt":
        os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system("clear")


def main():
    parser = argparse.ArgumentParser(
        description="The program scrapes the lists of clubs, events, fighters and ratings, and writes the info in a SQLite database in a 'data' directory. If no flags are given, nothing will be scraped."
    )
    parser.add_argument("-f", "--fighters", action="store_true", help="scrape fighters")
    parser.add_argument("-c", "--clubs", action="store_true", help="scrape clubs")
    parser.add_argument("-e", "--events", action="store_true", help="scrape events")
    parser.add_argument("-r", "--ratings", action="store_true", help="scrape ratings")
    parser.add_argument(
        "--history",
        action="store_true",
        help="scrape the full history of ratings (only works if -r is active)",
    )

    fighters_on = parser.parse_args().fighters
    clubs_on = parser.parse_args().clubs
    events_on = parser.parse_args().events
    ratings_on = parser.parse_args().ratings
    history_on = parser.parse_args().history

    clear()
    print("Initialising...")

    if not os.path.exists("data"):
        os.mkdir("data")

    if clubs_on:
        # process_clubs = Process(target=clubs.clubs)
        # process_clubs.start()
        clubs.clubs()
        print("Club scraping completed.")

    if events_on:
        # process_events = Process(target=events.events)
        # process_events.start()
        events.events()
        print("Event scraping completed.")

    if fighters_on:
        fighters.fighters()
        print("Fighters scraping completed.")

    if ratings_on:
        ratings.ratings(history=history_on)
        print("Ratings scraping completed.")

    print()
    print("Scrape complete.")


if __name__ == "__main__":
    main()
