import requests
import sqlite3
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

from src import sql_helpers


def club(link):
    club_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    name = None
    short_name = None
    country = None
    state = None
    city = None
    parent_club_id = None

    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="lxml")

    name_sp = soup.find("h2")
    name = name_sp.text.strip().split("\n")[0].split("\r")[0].strip()
    if len(name_sp.text.strip().split("\n")) == 2:
        short_name = name_sp.text.strip().split("\n")[1].split("\r")[0].strip("() ")

    metadata_table = soup.find("table", class_="table table-striped")
    md_rows = metadata_table.find_all("tr")
    for r in md_rows:
        metadata = r.find_all("td")

        if metadata[0].text.strip() == "Country":
            country = metadata[1].find("i")["title"]

        if metadata[0].text.strip() == "State":
            state = metadata[1].text.strip()

        if metadata[0].text.strip() == "City":
            city = metadata[1].text.strip()

        if metadata[0].text.strip() == "Parent club":
            parent_club_id = metadata[1].find("a")["href"].split("/")[-2]

    club_dict = {
        "club_id": club_id,
        "club_name": name,
        "club_short_name": short_name,
        "country": country,
        "state": state,
        "city": city,
        "parent_club_id": parent_club_id,
    }

    return club_dict


def clubs():
    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("clubs"))
    cursor.execute(
        sql_helpers.create_table(
            "clubs",
            {
                "club_id": "INTEGER PRIMARY KEY",
                "club_name": "TEXT",
                "club_short_name": "TEXT",
                "country": "TEXT",
                "state": "TEXT",
                "city": "TEXT",
                "parent_club_id": "INTEGER",
            },
        )
    )
    clubs = requests.get("https://hemaratings.com/clubs/")
    clubs_soup = BeautifulSoup(clubs.text, features="lxml")

    table = clubs_soup.find("table", id="mainTable")
    data = table.find_all("a", href=True)

    print("Scraping club list")
    num_processes = cpu_count() - 1

    lines = []
    for d in data:
        lines.append(d["href"])

    with Pool(num_processes) as pool:
        results = pool.map(club, lines)

    for i, line in enumerate(results):
        cursor.execute(sql_helpers.insert("clubs", line))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clubs()
