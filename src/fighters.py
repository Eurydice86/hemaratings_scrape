import requests
import sqlite3
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

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
    num_processes = cpu_count()

    fighters_list = []
    for f in ftrs:
        fighter_id = f["href"]
        if fighter_id.split("/")[1] == "fighters":
            fighters_list.append(fighter_id)
    with Pool(num_processes) as pool:
        results = pool.map(fighter.fighter, fighters_list)
    for f in results:
        cursor.execute(sql_helpers.insert("fighters", f))

        """
        print(f"{100 * (i/len(ftrs)):2.2f}% completed.", end="\r")
        line = fighter.fighter(fighter_id)
        cursor.execute(sql_helpers.insert("fighters", line))
        """

    conn.commit()
    conn.close()


if __name__ == "__main__":
    fighters()
