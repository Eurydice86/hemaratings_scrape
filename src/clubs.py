import csv
import requests
from bs4 import BeautifulSoup

from src import club


def clubs():
    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, features="lxml")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)

    print("Scraping club list")
    with open("data/clubs.csv", "w", newline="") as clubs_csv:
        fieldnames = [
            "club_id",
            "club_name",
            "club_short_name",
            "country",
            "state",
            "city",
        ]

        writer = csv.DictWriter(clubs_csv, fieldnames=fieldnames)
        writer.writeheader()

        for i, d in enumerate(data):
            print(f"{100 * (i/len(data)):2.2f}% completed.", end="\r")
            link = d["href"]
            line = club.club(link)
            writer.writerow(line)


if __name__ == "__main__":
    clubs()
