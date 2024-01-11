import requests
from bs4 import BeautifulSoup

import fighter


def fighters():
    """Goes through the 'fighters' page on Hemaratings and calls the fighter
    function for each of the fighters on the list"""
    events = requests.get("https://hemaratings.com/fighters/")
    sp = BeautifulSoup(events.text, "lxml")

    ftrs_table = sp.find("table", id="mainTable")
    ftrs = ftrs_table.find_all("a", href=True)
    for i, f in enumerate(ftrs):
        fighter_id = f["href"]
        if fighter_id.split("/")[1] == "fighters":
            print(int(i / 2) + 1, int(len(ftrs) / 2))
            # print(f.text.strip(), fighter_id)
            fighter.fighter(fighter_id)


if __name__ == "__main__":
    fighters()
