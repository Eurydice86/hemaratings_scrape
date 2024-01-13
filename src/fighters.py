import requests
from bs4 import BeautifulSoup

from src import fighter


def fighters():
    """Goes through the 'fighters' page on Hemaratings and calls the fighter
    function for each of the fighters on the list"""
    events = requests.get("https://hemaratings.com/fighters/")
    sp = BeautifulSoup(events.text, features="html.parser")

    ftrs_table = sp.find("table", id="mainTable")
    ftrs = ftrs_table.find_all("a", href=True)
    print("Scraping fighter list")
    for i, f in enumerate(ftrs):
        fighter_id = f["href"]
        if fighter_id.split("/")[1] == "fighters":
            print(f"{100 * (i/len(ftrs)):2.2f}% completed.", end="\r")
            fighter.fighter(fighter_id)


if __name__ == "__main__":
    fighters()
