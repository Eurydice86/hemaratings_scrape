import os
import shutil
import argparse
import sys

from src import clubs, events, fighters, rankings


def clear():
    # for windows
    if os.name == "nt":
        os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system("clear")


def main():
    parser = argparse.ArgumentParser(
        description="The program scrapes the lists of clubs, events,\
        fighters and rankings, and writes the info in a 'data' directory."
    )
    parser.add_argument("-f", "--fullhistory", action="store_true")
    hist_on = parser.parse_args().fullhistory

    clear()
    print(
        "The program scrapes the lists of clubs, events, fighters and rankings, and writes the info in a 'data' directory."
    )

    print("Reconstructing directory structure.")
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.mkdir("data")

    clubs.clubs()
    print("Club scraping completed.")

    events.events()
    print("Event scraping completed.")

    fighters.fighters()
    print("Fighters scraping completed.")

    rankings.rankings(history=hist_on)
    print("Rankings scraping completed.")
    print()

    print("Scrape complete.")


if __name__ == "__main__":
    main()
