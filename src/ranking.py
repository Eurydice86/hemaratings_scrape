import requests
from bs4 import BeautifulSoup


def ranking(category, month=0, year=0):
    rankings_list = []

    category_id = category.split("=")[-1]
    if int(month) != 0 and int(year) != 0:
        category += f"&year={year}&month={int(month)}"
    print(category)

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
        active = "Inactive" if deviation_list[0].strip() == "Inactive" else "Active"

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
    ranking("https://hemaratings.com/periods/details/?ratingsetid=12", 2, 2023)
