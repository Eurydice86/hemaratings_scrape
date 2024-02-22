import requests
import sqlite3
from bs4 import BeautifulSoup

from src import event
from src import sql_helpers


def events():
    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("events"))
    cursor.execute(sql_helpers.drop_table("competitions"))
    cursor.execute(sql_helpers.drop_table("fights"))
    cursor.execute(
        sql_helpers.create_table(
            "events",
            {
                "event_id": "TEXT PRIMARY KEY",
                "event_name": "TEXT",
                "date": "TEXT",
                "country": "TEXT",
                "state": "TEXT",
                "city": "TEXT",
            },
        )
    )

    cursor.execute(
        sql_helpers.create_table(
            "fights",
            {
                "fight_id": "TEXT PRIMARY KEY",
                "fighter_1_id": "INTEGER",
                "fighter_2_id": "INTEGER",
                "result": "INTEGER",
                "stage": "TEXT",
                "competition_id": "TEXT",
            },
        )
    )

    cursor.execute(
        sql_helpers.create_table(
            "competitions",
            {
                "competition_id": "TEXT PRIMARY KEY",
                "competition_name": "INTEGER",
                "event_id": "INTEGER",
            },
        )
    )

    events = requests.get("https://hemaratings.com/events/")
    sp = BeautifulSoup(events.text, features="lxml")

    rows = sp.find_all("div", class_="panel panel-default")
    print("Scraping events list")

    for i, r in enumerate(rows):
        print(f"{100 * (i/len(rows)):2.2f}% completed.", end="\r")
        year = r.find("div")["id"].split("_")[1]
        link = r.find("a", href=True)["href"]
        line = event.event(link, year, cursor)
        cursor.execute(sql_helpers.insert("events", line))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    events()
