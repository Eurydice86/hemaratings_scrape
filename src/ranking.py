import requests
from bs4 import BeautifulSoup


def ranking(category):
    rankings_list = []

    category_id = category.split("=")[-1]
    page = requests.get(category)
    sp = BeautifulSoup(page.text, "lxml")
    table = sp.find("table", id="mainTable")
    table = table.find("tbody")
    rows = table.find_all("tr")

    for r in rows:
        name = r.find("a")
        fighter_id = name["href"].split("/")[-2]
        weighted_rating = r.find_all("span")[1].text
        deviation_list = r.find_all("i")[-1]["title"].split("(")
        deviation = deviation_list[-1].strip(")")
        active = not deviation_list[0].strip() == "Inactive"

        ranking_dict = {
            "category_id": category_id,
            "fighter_id": fighter_id,
            "weighted_rating": weighted_rating,
            "deviation": deviation,
            "active": active,
        }

        rankings_list.append(ranking_dict)

    return rankings_list


if __name__ == "__main__":
    ranking("https://hemaratings.com/Periods/Details/?ratingsetid=12")
