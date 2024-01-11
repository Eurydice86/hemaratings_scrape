import requests
from bs4 import BeautifulSoup

import club


def clubs():
    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, "lxml")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)
    for i, d in enumerate(data):
        print(f"{i+1} of {len(data)}")
        link = d["href"]
        club.club(link)


if __name__ == "__main__":
    clubs()
