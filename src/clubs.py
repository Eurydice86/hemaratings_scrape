import requests
import sqlite3
from bs4 import BeautifulSoup

from src import club
from src import sql_helpers


def clubs():
    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("clubs"))
    cursor.execute(
        sql_helpers.create_table(
            "clubs",
            {
                "club_id": "INTEGER PRIMARY KEY",
                "club_name": "TEXT",
                "club_short_name": "TEXT",
                "country": "TEXT",
                "state": "TEXT",
                "city": "TEXT",
                "parent_club_id": "INTEGER",
            },
        )
    )

    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, features="lxml")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)

    print("Scraping club list")

    for i, d in enumerate(data):
        print(f"{100 * (i/len(data)):2.2f}% completed.", end="\r")
        link = d["href"]
        line = club.club(link)
        cursor.execute(sql_helpers.insert("clubs", line))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    clubs()
