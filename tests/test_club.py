from src import clubs


def test_no_state():
    c = clubs.club("/clubs/details/2/")
    assert c["club_name"] == "EHMS"
    assert c["club_short_name"] == "EHMS"
    assert c["country"] == "Finland"
    assert c["state"] == None
    assert c["club_id"] == "2"
    assert c["parent_club_id"] == None
    

def test_all():
    c = clubs.club("/clubs/details/1672/")
    assert c["club_name"] == "College of Silva Vulcani"
    assert c["club_short_name"] == None
    assert c["country"] == "United States"
    assert c["state"] == "California"
    assert c["city"] == None
    assert c["club_id"] == "1672"
    assert c["parent_club_id"] == "619"


def test_city():
    c = clubs.club("/clubs/details/562/")
    assert c["club_name"] == "Wiener Fecht- und Ausdauersportrunde"
    assert c["club_short_name"] == "WFA"
    assert c["country"] == "Austria"
    assert c["state"] == None
    assert c["city"] == "Vienna"
    assert c["club_id"] == "562"
    assert c["parent_club_id"] == None
