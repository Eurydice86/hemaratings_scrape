import requests
from bs4 import BeautifulSoup

from src import club


def clubs():
    clubs_table = []

    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, features="lxml")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)

    print("Scraping club list")
    for i, d in enumerate(data):
        print(f"{100 * (i/len(data)):2.2f}% completed.", end="\r")
        link = d["href"]
        line = club.club(link)
        clubs_table.append(line)

    clubs_file = open("data/clubs.csv", "w")
    clubs_file.write("club_id;club_name;short_name;country;state;city\n")
    for line in clubs_table:
        clubs_file.write(line)
    clubs_file.close()


if __name__ == "__main__":
    clubs()
