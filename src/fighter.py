import numpy as np
import requests
from bs4 import BeautifulSoup


def category_name_to_id(name):
    match name:
        case "Longsword (Mixed & Men's, Steel)":
            return 1
        case "Longsword (Women's, Steel)":
            return 2
        case "Longsword (Underrepresented Genders & Women's, Steel)":
            return 22
        case "Longsword (Mixed & Men's, Nylon)":
            return 8
        case "Rapier and Dagger (Mixed, Steel)":
            return 4
        case "Single Rapier (Mixed, Steel)":
            return 5
        case "Sabre (Mixed & Men's, Steel)":
            return 3
        case "Sword and Buckler (Mixed, Steel)":
            return 6
        case "Sidesword (Mixed, Steel)":
            return 9
        case "Singlestick (Mixed)":
            return 12


def which_weapons(categories, ratings, rankings, fighter):
    file_out = open("data/ratings.csv", "a")

    for i in range(len(categories)):
        pass
        # check category name and make an entry in the ratings table
        # something like "if name is LS steel mixed"
        category_id = category_name_to_id(categories[i])
        rating = ratings[i]
        ranking = rankings[i]
        file_out.write(f"{category_id},{fighter},{rating},{ranking}\n")

    file_out.close()


def fighter(link):
    final_categories = []
    final_ratings = []
    final_rankings = []
    fighter_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link

    page = requests.get(full_url)
    # soup = BeautifulSoup(page.text, features="html.parser")
    soup = BeautifulSoup(page.text, "lxml")

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

    nationality = "-"
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
        # print(r)
        final_categories.append(r[0])
        final_rankings.append(r[1])
        final_ratings.append(r[2])

    which_weapons(final_categories, final_ratings, final_rankings, fighter_id)

    """
    fighter = {
        "id": fighter_id,
        "name": fighter_name,
        "nationality": nationality,
        "club_id": club_id,
    }
    """

    out_file = open("data/fighters.csv", "a")
    out_file.write(f"{fighter_id},{fighter_name},{nationality},{club_id}\n")
    out_file.close()


if __name__ == "__main__":
    fighter("/fighters/details/7951/")
    # fighter("/fighters/details/5/")
