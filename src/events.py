import requests
from bs4 import BeautifulSoup

from src import event


def events():
    events_list = []

    events = requests.get("https://hemaratings.com/events/")
    # events_soup = BeautifulSoup(events.text, features="html.parser")
    events_soup = BeautifulSoup(events.text, features="lxml")

    table = events_soup.find("div", id="main")
    column_names = table.find_all("div", class_="panel-body")

    print("Scraping event list")
    for i, c in enumerate(column_names):
        print(f"{100 * (i/len(column_names)):2.2f}% completed.", end="\r")
        link = c.find("a", href=True)["href"]
        line = event.event(link)
        events_list.append(line)

    events_file = open("data/events.csv", "w")
    events_file.write("event_id;event_name;date;country;state;city\n")
    for line in events_list:
        events_file.write(line)


if __name__ == "__main__":
    events()
