import csv
import requests
from bs4 import BeautifulSoup

from src import event


def events():
    events = requests.get("https://hemaratings.com/events/")
    sp = BeautifulSoup(events.text, features="lxml")

    rows = sp.find_all("div", class_="panel panel-default")
    print("Scraping events list")
    with open("data/events.csv", "w", newline="") as events_csv:
        fieldnames = [
            "event_id",
            "event_name",
            "date",
            "year",
            "country",
            "state",
            "city",
        ]
        writer = csv.DictWriter(events_csv, fieldnames=fieldnames)
        writer.writeheader()

        for i, r in enumerate(rows):
            print(f"{100 * (i/len(rows)):2.2f}% completed.", end="\r")
            year = r.find("div")["id"].split("_")[1]
            link = r.find("a", href=True)["href"]
            line = event.event(link, year)
            writer.writerow(line)


if __name__ == "__main__":
    events()
