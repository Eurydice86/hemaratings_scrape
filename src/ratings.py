import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import date
from multiprocessing import Pool, cpu_count

from src import rating
from src import sql_helpers


def ratings(history=False, year=0, month=0):
    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("ratings"))
    cursor.execute(
        sql_helpers.create_table(
            "ratings",
            {
                "category_id": "INTEGER",
                "date": "TEXT",
                "fighter_id": "INTEGER",
                "weighted_rating": "REAL",
                "deviation": "REAL",
                "active": "TEXT",
            },
        )
    )

    ratings = requests.get("https://hemaratings.com/")
    sp = BeautifulSoup(ratings.text, "lxml")

    dd_menu = sp.find("ul", class_="dropdown-menu")
    categories = dd_menu.find_all("a", href=True)

    print("Scraping ratings")

    cursor.execute(sql_helpers.drop_table("categories"))
    cursor.execute(
        sql_helpers.create_table(
            "categories",
            {"category_id": "INTEGER PRIMARY KEY", "category_name": "TEXT"},
        )
    )

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
        cursor.execute(sql_helpers.insert("categories", categories_dict))

        num_processes = cpu_count()
        if history:
            date_dropdown = c_sp.find("select")
            dates = date_dropdown.find_all("option")
            iterables = []
            for i, d in enumerate(dates):
                year = d["value"].split("-")[0]
                month = d["value"].split("-")[1]
                iterables.append((link, year, month))

            with Pool(num_processes) as pool:
                results = pool.starmap(rating.rating, iterables)
            for ratings_list in results:
                for line in ratings_list:
                    cursor.execute(sql_helpers.insert("ratings", line))
        else:
            year = date.today().year
            month = date.today().month
            ratings_list = rating.rating(link, year=year, month=month)
            for line in ratings_list:
                cursor.execute(sql_helpers.insert("ratings", line))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    ratings(history=True)
