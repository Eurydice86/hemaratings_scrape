import requests
from bs4 import BeautifulSoup


def ranking(category):
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
        deviation = r.find_all("i")[-1]["title"].split("(")[-1].strip(")")
        active = not r.find_all("i")[-1]["title"].split("(")[0].strip() == "Inactive"

        out_file = open("data/ratings.csv", "a")
        out_file.write(
            f"{category_id};{fighter_id};{weighted_rating};{deviation};{active}\n"
        )
        out_file.close()


if __name__ == "__main__":
    ranking("https://hemaratings.com/Periods/Details/?ratingsetid=12")
