import json

import numpy as np
import requests
from bs4 import BeautifulSoup


def fighter(link):
    final_categories = []
    final_ratings = []
    final_rankings = []
    fighter_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link

    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="html.parser")

    sp = soup.find("div", id="main")
    fighter_name = sp.find("h2").text.strip()

    """
    cols = sp.find_all("dt")
    columns = []
    for c in cols:
        columns.append(c.text.strip())
    print(columns)
    """

    dummy = sp.find_all("a", href=True)[0]
    club_id = dummy["href"].split("/")[-2]

    nationality = ""
    if sp.find("i"):
        nationality = sp.find("i")["title"]

    ratings = []
    record = sp.find_all("table", class_="table table-striped")[1]

    """
    headers = record.find_all("th")
    for h in headers:
        print(h.text.strip())
    """

    rows = record.find_all("td")
    for r in rows:
        ratings.append(r.text.strip())

    ratings_np = np.array(ratings)
    ratings_np = ratings_np.reshape(int(len(ratings) / 3), 3)
    for r in ratings_np:
        #print(r)
        final_categories.append(r[0])
        final_rankings.append(r[1])
        final_ratings.append(r[2])

    fighter = {
        "id": fighter_id,
        "name": fighter_name,
        "nationality": nationality,
        "categories": final_categories,
        "ratings": final_ratings,
        "rankings": final_rankings,
        "club_id": club_id,
    }

    filename = "data/fighters/fighter_" + fighter_id + ".json"
    with open(filename, "w") as file:
        json.dump(fighter, file, indent=4)

    #print(json.dumps(fighter, indent=4))


if __name__ == "__main__":
    fighter("/fighters/details/7951/")
