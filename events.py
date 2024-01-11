import requests
from bs4 import BeautifulSoup

import event


def events():
    events = requests.get("https://hemaratings.com/events/")
    events_soup = BeautifulSoup(events.text, "lxml")

    table = events_soup.find("div", id="main")
    column_names = table.find_all("div", class_="panel-body")

    for i, c in enumerate(column_names):
        print(f"{i+1} of {len(column_names)}")
        link = c.find("a", href=True)["href"]
        event.event(link)


if __name__ == "__main__":
    events()
