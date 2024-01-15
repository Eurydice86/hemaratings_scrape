import requests
from bs4 import BeautifulSoup


def category(category):
    full_url = "https://hemaratings.com" + category

    get = requests.get(full_url)
    soup = BeautifulSoup(get.text, features="html.parser")

    category_name = soup.find("h2")
    category_name = category_name.text.split("-")[0]

    table = soup.find("table", id="mainTable")
    entries = table.find_all("a", href=True)

    fighters_ratings = []
    for e in entries:
        splt = e["href"].split("/")
        if splt[1] == "fighters":
            fighter_id = e["href"].strip().split("/")[-2]
            print(fighter_id)


if __name__ == "__main__":
    category("/periods/details/?ratingsetid=22")
