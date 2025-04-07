import requests
import sqlite3
import uuid
import re

from datetime import datetime
from bs4 import BeautifulSoup

from src import sql_helpers


def events():
    """Generates a list of all the events from the Hemaratings 'events' page and calls the event function for each."""

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
        line = event(link, year, cursor)
        if line:
            cursor.execute(sql_helpers.insert("events", line))
    conn.commit()
    conn.close()


def event(link, year, cursor=None):
    """Extracts the event info given its Hemaratings link, returns a dictionary for the event and writes the competitions info into the database."""

    event_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    page = requests.get(full_url)

    soup = BeautifulSoup(page.text, features="lxml")

    if soup.find("h1"):
        if soup.find("h1").text.strip() == "Service Unavailable":
            print(f"Event {link} not found.")
            return

    sp = soup.find("div", id="main")
    event_name = sp.find("h2").text.strip()
    metadata_div = sp.find("div", class_="row")
    metadata_table = metadata_div.find_all("td")

    metadata = []

    for m in metadata_table:
        metadata.append(m.text.strip())

    metadata_dict = {}
    for i in range(0, int(len(metadata)), 2):
        metadata_dict[metadata[i]] = metadata[i + 1]

    event_date = metadata_dict["Date"]
    month_name = event_date.split(" ")[0].strip()

    date_object = datetime.strptime(month_name, "%B")
    month_number = date_object.month

    day = event_date.split(", ")[0].split(" ")[1].strip()
    date = f"{year}-{month_number}-{day}"

    country = metadata_dict["Country"]

    try:
        city = metadata_dict["City"]
    except:
        city = None

    try:
        state = metadata_dict["State"]
    except:
        state = None

    event_dict = {
        "event_id": event_id,
        "event_name": event_name,
        "date": date,
        "country": country,
        "state": state,
        "city": city,
    }

    tournaments = sp.find_all("div", {"id": re.compile("heading_tournament_*")})

    for t in tournaments:
        competition = t.find("span").text.strip()
        competition_id = uuid.uuid4()
        competition_dict = {
            "competition_id": competition_id,
            "competition_name": competition,
            "event_id": event_id,
        }
        if cursor:
            cursor.execute(sql_helpers.insert("competitions", competition_dict))

        category_table = t.find_next("table")
        rows = category_table.find_all("tr")
        rows = rows[1:]
        for r in rows:
            entries = r.find_all("td")
            stage = entries[0].text.strip()

            fighter_1 = entries[1]
            if fighter_1.find("a"):
                fighter_1_id = fighter_1.find("a")["href"].split("/")[-2]
            else:
                fighter_1_id = None
            fighter_2 = entries[2]
            if fighter_2.find("a"):
                fighter_2_id = fighter_2.find("a")["href"].split("/")[-2]
            else:
                fighter_2_id = None

            if entries[3].text.strip() == "WIN":
                result = 1
            elif entries[3].text.strip() == "LOSS":
                result = 2
            else:
                result = 0
            fight_dict = {
                "fight_id": uuid.uuid4(),
                "fighter_1_id": fighter_1_id,
                "fighter_2_id": fighter_2_id,
                "result": result,
                "stage": stage,
                "competition_id": competition_id,
            }
            if cursor:
                cursor.execute(sql_helpers.insert("fights", fight_dict))

    return event_dict
