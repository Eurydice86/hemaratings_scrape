import csv
import requests
from bs4 import BeautifulSoup

from src import fighter


def fighters():
    """Goes through the 'fighters' page on Hemaratings and calls the fighter
    function for each of the fighters on the list"""
    events = requests.get("https://hemaratings.com/fighters/")
    # sp = BeautifulSoup(events.text, features="html.parser")
    sp = BeautifulSoup(events.text, "lxml")

    ftrs_table = sp.find("table", id="mainTable")
    ftrs = ftrs_table.find_all("a", href=True)
    print("Scraping fighter list")

    with open("data/fighters.csv", "w", newline="") as fighters_csv:
        fieldnames = ["fighter_id", "name", "nationality", "club_id"]

        writer = csv.DictWriter(fighters_csv, fieldnames=fieldnames)
        writer.writeheader()

        for i, f in enumerate(ftrs):
            fighter_id = f["href"]
            if fighter_id.split("/")[1] == "fighters":
                print(f"{100 * (i/len(ftrs)):2.2f}% completed.", end="\r")
                line = fighter.fighter(fighter_id)
                writer.writerow(line)


if __name__ == "__main__":
    fighters()
