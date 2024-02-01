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
    for c in categories:
        link = "https://hemaratings.com" + c["href"]
        ranking.ranking(link)


if __name__ == "__main__":
    rankings()
