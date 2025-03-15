import requests
from bs4 import BeautifulSoup


def rating(category, year=0, month=0):
    ratings_list = []

    category_id = category.split("=")[-1]
    if int(month) != 0 and int(year) != 0:
        category += f"&year={year}&month={int(month)}"

    date = f"01/{month}/{year}"
    page = requests.get(category)
    sp = BeautifulSoup(page.text, "lxml")
    table = sp.find("table", id="mainTable")

    table = table.find("tbody")
    rows = table.find_all("tr")

    for r in rows:
        name = r.find("a")
        fighter_id = name["href"].split("/")[-2]
        weighted_rating = r.find_all("span")[-1].text
        deviation_list = r.find_all("i")[-1]["title"].split("(")
        deviation = deviation_list[-1].strip(")")
        active = "Inactive" if deviation_list[0].strip() == "Inactive" else "Active"

        rating_dict = {
            "category_id": category_id,
            "date": date,
            "fighter_id": fighter_id,
            "weighted_rating": weighted_rating,
            "deviation": deviation,
            "active": active,
        }

        ratings_list.append(rating_dict)

    return ratings_list


if __name__ == "__main__":
    r = rating(
        "https://hemaratings.com/periods/details/?ratingsetid=12", year=2023, month=12
    )
    print(json.dumps(r, indent=2))
