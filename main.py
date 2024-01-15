import os

from src import clubs, events, fighters


def clear():
    # for windows
    if os.name == "nt":
        os.system("cls")

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system("clear")


def main():
    clear()
    print("The program will scrape the lists of clubs, events and fighters")
    print("and write the info into json files in a 'data' directory")
    print("(one file for each fighter, club and event).")
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print()

    if not os.path.exists("data"):
        os.mkdir("data")
        os.mkdir("data/fighters")
        os.mkdir("data/clubs")
        os.mkdir("data/events")

    clubs.clubs()
    print("Club scraping completed.")
    events.events()
    print("Event scraping completed.")
    fighters.fighters()
    print()
    print("Scrape complete.")


if __name__ == "__main__":
    main()
