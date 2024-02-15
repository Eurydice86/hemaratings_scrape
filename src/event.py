import numpy as np
import requests
from bs4 import BeautifulSoup


def event(link, year):
    final_categories = []
    final_participants = []
    event_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    page = requests.get(full_url)
    # soup = BeautifulSoup(page.text, features="html.parser")
    soup = BeautifulSoup(page.text, features="lxml")

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

    date = f"{metadata[0]}, {year}"
    country = metadata[1].strip()
    state = None
    city = None
    if len(metadata) == 3:
        city = metadata[2].strip()
    if len(metadata) == 4:
        state = metadata[2].strip()
        country = metadata[1].strip()
        city = metadata[3].strip()

    event_dict = {
        "event_id": event_id,
        "event_name": event_name,
        "date": date,
        "country": country,
        "state": state,
        "city": city,
    }

    return event_dict


if __name__ == "__main__":
    event("/events/details/1926/")
