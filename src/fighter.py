import requests
from bs4 import BeautifulSoup


def fighter(link):
    fighter_id = link.split("/")[-2]
    full_url = "https://hemaratings.com" + link

    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, "lxml")

    sp = soup.find("div", id="main")
    fighter_name = sp.find("h2").text.strip()

    dummy = sp.find_all("a", href=True)[0]
    club_id = "-"
    if dummy["href"].split("/")[1] == "clubs":
        club_id = dummy["href"].split("/")[-2]

    nationality = "-"
    if sp.find("i"):
        nationality = sp.find("i")["title"]

    out_file = open("data/fighters.csv", "a")
    out_file.write(f"{fighter_id};{fighter_name};{nationality};{club_id}\n")
    out_file.close()


if __name__ == "__main__":
    fighter("/fighters/details/7951/")
    fighter("/fighters/details/5/")
