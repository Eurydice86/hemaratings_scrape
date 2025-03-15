from datetime import datetime

import requests
import uuid
import re
from bs4 import BeautifulSoup

from src import sql_helpers


def event(link, year, cursor):
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
    date = f"{day}/{month_number}/{year}"

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
            cursor.execute(sql_helpers.insert("fights", fight_dict))

    return event_dict


if __name__ == "__main__":
    import json

    e = event("/events/details/2019/", 2024)
    print(json.dumps(e, indent=2))
    e = event("/events/details/2330/", 2025)
    print(json.dumps(e, indent=2))
    e = event("/events/details/1813/", 2023)
    print(json.dumps(e, indent=2))
