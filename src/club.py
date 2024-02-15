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
    parent_club_id = "-"

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


if __name__ == "__main__":
    club("/clubs/details/78/")
    club("/clubs/details/326/")
