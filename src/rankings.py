import csv
import requests
from bs4 import BeautifulSoup

from src import ranking


def rankings():
    """Goes through the 'rankings' page on Hemaratings and calls the ranking
    function for each of the categories"""

    page = requests.get("https://hemaratings.com/")
    sp = BeautifulSoup(page.text, "lxml")

    dd_menu = sp.find("ul", class_="dropdown-menu")
    categories = dd_menu.find_all("a", href=True)

    print("Scraping ratings")
    with open("data/ratings.csv", "w", newline="") as ratings_csv:
        fieldnames = [
            "category_id",
            "fighter_id",
            "weighted_rating",
            "deviation",
            "active",
        ]

        writer = csv.DictWriter(ratings_csv, fieldnames=fieldnames)
        writer.writeheader()
        for i, c in enumerate(categories):
            print(f"{100 * (i/len(categories)):2.2f}% completed.", end="\r")
            link = "https://hemaratings.com" + c["href"]
            rankings_list = ranking.ranking(link)
            for line in rankings_list:
                writer.writerow(line)


if __name__ == "__main__":
    rankings()
