import requests
from bs4 import BeautifulSoup, SoupStrainer


def fighter(link):
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


if __name__ == "__main__":
    fighter("/fighters/details/1330/")
#    fighter("/fighters/details/2877/")
#    fighter("/fighters/details/5/")
#    fighter("/fighters/details/10769/")
#    fighter("/fighters/details/13912/")
