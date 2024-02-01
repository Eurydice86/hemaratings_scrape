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

    fighters_file = open("data/fighters.csv", "w")
    fighters_file.write("fighter_id;fighter_name;nationality;club_id\n")
    fighters_file.close()

    ratings_file = open("data/ratings.csv", "w")
    ratings_file.write("category_id;fighter_id;weighted_rating;deviation;active\n")
    ratings_file.close()

    clubs.clubs()
    print("Club scraping completed.")

    events.events()
    print("Event scraping completed.")

    fighters.fighters()
    print("Fighters scraping completed.")

    rankings.rankings()
    print()

    print("Scrape complete.")


if __name__ == "__main__":
    main()
