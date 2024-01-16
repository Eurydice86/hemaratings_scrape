import os
import shutil

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
    print("and write the info into files in a 'data' directory.")
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print()

    if os.path.exists("data"):
        shutil.rmtree("data")

    os.mkdir("data")
    fighters_file = open("data/fighters.csv", "w")
    fighters_file.write("fighter_id,fighter_name,nationality,club_id\n")
    fighters_file.close()
    clubs_file = open("data/clubs.csv", "w")
    clubs_file.write("club_id,club_name,short_name,country,state,city\n")
    clubs_file.close()
    events_file = open("data/events.csv", "w")
    events_file.write("event_id,event_name,date,country,state,city\n")
    events_file.close()
    ratings_file = open("data/ratings.csv", "w")
    ratings_file.write("category_id,fighter,rating,ranking\n")
    ratings_file.close()

    clubs.clubs()
    print("Club scraping completed.")
    events.events()
    print("Event scraping completed.")
    fighters.fighters()
    print()
    print("Scrape complete.")


if __name__ == "__main__":
    main()
