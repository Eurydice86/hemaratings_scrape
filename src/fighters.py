import requests
import sqlite3
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing import Pool, cpu_count

from src import sql_helpers


def fighter(link):
    """Extracts the id, name, nationality and club id of a fighter, given the link to their Hemagon profile page and returns a dictionary with the info."""
    
    requests_session = requests.Session()

    fighter_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    page = requests_session.get(full_url)

    strained = SoupStrainer("article")
    soup = BeautifulSoup(page.text, "lxml", parse_only=strained)
    sp = soup.find("article")

    fighter_name = sp.find("h2").text.strip()

    club_id = None
    dummy = sp.find_all("a", href=True)
    if dummy:
        dummy = dummy[0]
        if dummy["href"].split("/")[1] == "clubs":
            club_id = dummy["href"].split("/")[-2]

    nationality = None
    if sp.find("i"):
        nationality = sp.find("i")["title"]

    fighter_dict = {
        "fighter_id": fighter_id,
        "name": fighter_name,
        "nationality": nationality,
        "club_id": club_id,
    }

    return fighter_dict


def fighters():
    """Generates a list of all the fighters on the Hemaratings 'fighters' page and calls the fighter
    function for each, then collects the fighter info dictionaries and writes them into the database."""

    conn = sqlite3.connect("data/hemaratings.db")
    cursor = conn.cursor()

    cursor.execute(sql_helpers.drop_table("fighters"))
    cursor.execute(
        sql_helpers.create_table(
            "fighters",
            {
                "fighter_id": "INTEGER PRIMARY KEY",
                "name": "TEXT",
                "nationality": "TEXT",
                "club_id": "INTEGER",
            },
        )
    )

    page = requests.get("https://hemaratings.com/fighters/")
    sp = BeautifulSoup(page.text, "lxml")

    ftrs_table = sp.find("table", id="mainTable")
    ftrs = ftrs_table.find_all("a", href=True)
    print("Scraping fighter list")

    fighters_list = []
    for i in range(len(ftrs)):
        fighter_id = ftrs[i]["href"]
        if fighter_id.split("/")[1] == "fighters":
            fighters_list.append(fighter_id)

    num_processes = cpu_count() - 1

    with Pool(num_processes) as pool:
        results = pool.map(fighter, fighters_list)
    for f in results:
        cursor.execute(sql_helpers.insert("fighters", f))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    fighters()
