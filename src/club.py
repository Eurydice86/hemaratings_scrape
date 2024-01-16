import requests
from bs4 import BeautifulSoup


def club(link):
    club_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link
    name = ""
    short_name = ""
    country = ""
    state = ""
    city = ""

    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, features="lxml")

    name_sp = soup.find("h2")
    name = name_sp.text.strip().split("\n")[0].split("\r")[0].strip()
    if len(name_sp.text.strip().split("\n")) == 2:
        short_name = name_sp.text.strip().split("\n")[1].split("\r")[0].strip("() ")

    """
    sp = soup.find("table", class_="table table-striped")

    lst = sp.find_all("td")
    country = sp.find("i")["title"]

    info = []
    for m in lst:
        info.append(m.text.strip())
    for i in info:
        print(i)
    if info[2] == "City":
        city = info[2]
    else:
        state = info[2]
        city = info[4]
    """

    """
    club = {
        "id": club_id,
        "name": name,
        "short_name": short_name,
        "country": country,
        "state": state,
        "city": city,
    }

    filename = "data/clubs/club_" + club_id + ".json"
    with open(filename, "w") as file:
        json.dump(club, file, indent=4)
    """

    file_out = open("data/clubs.csv", "a")
    file_out.write(f"{club_id},{name},{short_name},{country},{state},{city}\n")
    file_out.close()


if __name__ == "__main__":
    club("/clubs/details/78/")
