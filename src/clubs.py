import requests
from bs4 import BeautifulSoup

from src import club


def clubs():
    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, features="html.parser")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)

    print("Scraping club list")
    for i, d in enumerate(data):
        print(f"{100 * (i/len(data)):2.2f}% completed.", end="\r")
        link = d["href"]
        club.club(link)


if __name__ == "__main__":
    clubs()
