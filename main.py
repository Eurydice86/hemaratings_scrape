import os
import shutil

from src import clubs, events, fighters, rankings


def clear():
    # for windows
    if os.name == "nt":
        os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system("clear")


def main():
    clear()
    print("The program will scrape the lists of clubs, events, fighters and rankings")
    print("and write the info into files in a 'data' directory.")
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print()

    if os.path.exists("data"):
        shutil.rmtree("data")
    os.mkdir("data")

    clubs.clubs()
    print("Club scraping completed.")

    events.events()
    print("Event scraping completed.")

    fighters.fighters()
    print("Fighters scraping completed.")

    rankings.rankings()
    print("Rankings scraping completed.")
    print()

    print("Scrape complete.")


if __name__ == "__main__":
    main()
