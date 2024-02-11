import csv
import requests
import sys
from bs4 import BeautifulSoup
from datetime import date


from src import ranking


def rankings(history=False, year=0, month=0):
    """Goes through the 'rankings' page on Hemaratings and calls the ranking
    function for each of the categories"""

    ratings_filename = "data/ratings.csv"
    if month != 0 and year != 0:
        ratings_filename = f"data/ratings_{year}_{int(month):02}.csv"
    page = requests.get("https://hemaratings.com/")
    sp = BeautifulSoup(page.text, "lxml")

    dd_menu = sp.find("ul", class_="dropdown-menu")
    categories = dd_menu.find_all("a", href=True)

    print("Scraping ratings")
    with open("data/categories.csv", "w", newline="") as categories_csv:
        c_fieldnames = ["category_id", "category_name"]
        c_writer = csv.DictWriter(categories_csv, fieldnames=c_fieldnames)
        c_writer.writeheader()

        with open(ratings_filename, "w", newline="") as ratings_csv:
            fieldnames = [
                "category_id",
                "year",
                "month",
                "fighter_id",
                "weighted_rating",
                "deviation",
                "active",
            ]

            writer = csv.DictWriter(ratings_csv, fieldnames=fieldnames)
            writer.writeheader()
            for c in categories:
                link = "https://hemaratings.com" + c["href"]
                c_page = requests.get(link)
                c_sp = BeautifulSoup(c_page.text, "lxml")
                category_name = c_sp.find("h2").text.split("-")[0].strip()
                print(category_name)

                categories_dict = {
                    "category_id": c["href"].split("=")[1],
                    "category_name": category_name,
                }

                if history:
                    date_dropdown = c_sp.find("select")
                    dates = date_dropdown.find_all("option")
                    c_writer.writerow(categories_dict)
                    for i, d in enumerate(dates):
                        year = d["value"].split("-")[0]
                        month = d["value"].split("-")[1]
                        print(
                            f"Scraping month {month}/{year} ({i + 1} of {len(dates)} dates completed).",
                            end="\r",
                        )
                        sys.stdout.write("\033[K")

                        rankings_list = ranking.ranking(link, year=year, month=month)
                        for line in rankings_list:
                            writer.writerow(line)
                else:
                    year = date.today().year
                    month = date.today().month
                    c_writer.writerow(categories_dict)
                    rankings_list = ranking.ranking(link, year=year, month=month)
                    for i, line in enumerate(rankings_list):
                        writer.writerow(line)


if __name__ == "__main__":
    rankings(history=True)
