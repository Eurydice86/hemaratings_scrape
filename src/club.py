import requests
from bs4 import BeautifulSoup


def club(link):
    club_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    name = "-"
    short_name = "-"
    country = "-"
    state = "-"
    city = "-"

    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="lxml")

    name_sp = soup.find("h2")
    name = name_sp.text.strip().split("\n")[0].split("\r")[0].strip()
    if len(name_sp.text.strip().split("\n")) == 2:
        short_name = name_sp.text.strip().split("\n")[1].split("\r")[0].strip("() ")

    club_dict = {
        "club_id": club_id,
        "club_name": name,
        "club_short_name": short_name,
        "country": country,
        "state": state,
        "city": city,
    }

    return club_dict


if __name__ == "__main__":
    club("/clubs/details/78/")
