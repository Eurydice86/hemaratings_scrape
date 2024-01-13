import json

import numpy as np
import requests
from bs4 import BeautifulSoup


def event(link):
    final_categories = []
    final_participants = []
    event_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="html.parser")

    sp = soup.find("div", id="main")
    event_name = sp.find("h2").text.strip()

    cols = sp.find_all("dt")
    columns = []
    for c in cols:
        columns.append(c.text.strip())

    rs = sp.find_all("dd")
    metadata = []
    for r in rs:
        metadata.append(r.text.strip())

    tournaments = sp.find_all("table", class_="table table-striped")[0]
    cols = tournaments.find_all("th")
    columns = []
    for c in cols:
        columns.append(c.text.strip())

    rows = []
    rs = tournaments.find_all("td")
    for r in rs:
        rows.append(r.text.strip())
    np_rows = np.array(rows)
    np_rows = np_rows.reshape(int(len(rows) / len(columns)), len(columns))
    for row in np_rows:
        final_categories.append(row[0])

    participants = sp.find_all("table", class_="table table-striped")[1]
    rs = participants.find_all("a", href=True)
    for r in rs:
        if str(r["href"]).split("/")[1] == "fighters":
            final_participants.append(r["href"].split("/")[-2])

    date = metadata[0]
    country = metadata[1].strip()
    state = ""
    city = ""
    if len(metadata) == 3:
        city = metadata[2].strip()
    if len(metadata) == 4:
        state = metadata[2].strip()
        country = metadata[1].strip()
        city = metadata[3].strip()

    """
    print("Event id:", event_id)
    print("Event name:", event_name)
    print("Date:", date)
    print("Country:", country)
    print("City:", city)
    print("Categories")
    for cat in final_categories:
        print(cat)
    print("Participants")
    for p in final_participants:
        print(p)
    """

    event = {
        "id": event_id,
        "name": event_name,
        "date": date,
        "country": country,
        "state": state,
        "city": city,
        "categories": final_categories,
        "participants": final_participants,
    }

    filename = "data/events/event_" + event_id + ".json"
    with open(filename, "w") as file:
        json.dump(event, file, indent=4)


if __name__ == "__main__":
    event("/events/details/1926/")