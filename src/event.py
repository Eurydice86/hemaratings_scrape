from datetime import datetime

# import numpy as np
import requests
from bs4 import BeautifulSoup


def event(link, year):
    event_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="lxml")

    sp = soup.find("div", id="main")
    event_name = sp.find("h2").text.strip()

    rs = sp.find_all("dd")
    metadata = []
    for r in rs:
        metadata.append(r.text.strip())

    month_name = metadata[0].split(" ")[0].strip()

    date_object = datetime.strptime(month_name, "%B")
    month_number = date_object.month

    month_number
    day = metadata[0].split(" ")[1].strip()
    date = f"{day}/{month_number}/{year}"
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
    print(event("/events/details/1926/", 2023))
