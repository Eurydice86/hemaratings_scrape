import requests
import sqlite3
from bs4 import BeautifulSoup

from src import fighter
from src import sql_helpers


def fighters():
    """Goes through the 'fighters' page on Hemaratings and calls the fighter
    function for each of the fighters on the list"""

    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("fighters"))
    cursor.execute(
        sql_helpers.create_table(
            "fighters",
            {
                "fighter_id": "INTEGER PRIMARY KEY",
                "name": "TEXT",
                "nationality": "TEXT",
                "club_id": "INTEGER",
            },
        )
    )

    page = requests.get("https://hemaratings.com/fighters/")
    sp = BeautifulSoup(page.text, "lxml")

    ftrs_table = sp.find("table", id="mainTable")
    ftrs = ftrs_table.find_all("a", href=True)
    print("Scraping fighter list")

    for i, f in enumerate(ftrs):
        fighter_id = f["href"]
        if fighter_id.split("/")[1] == "fighters":
            print(f"{100 * (i/len(ftrs)):2.2f}% completed.", end="\r")
            line = fighter.fighter(fighter_id)
            cursor.execute(sql_helpers.insert("fighters", line))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    fighters()
