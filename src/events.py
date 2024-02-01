import requests
from bs4 import BeautifulSoup

from src import event


def events():
    events_list = []

    events = requests.get("https://hemaratings.com/events/")
    # events_soup = BeautifulSoup(events.text, features="html.parser")
    sp = BeautifulSoup(events.text, features="lxml")

    rows = sp.find_all("div", class_="panel panel-default")
    for i, r in enumerate(rows):
        print(f"{100 * (i/len(rows)):2.2f}% completed.", end="\r")
        year = r.find("div")["id"].split("_")[1]
        link = r.find("a", href=True)["href"]
        line = event.event(link, year)
        events_list.append(line)

    events_file = open("data/events.csv", "w")
    events_file.write("event_id;event_name;date;year;country;state;city\n")
    for line in events_list:
        events_file.write(line)


if __name__ == "__main__":
    events()
