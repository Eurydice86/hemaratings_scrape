from src import fighter


def test_all():
    f = fighter.fighter("/fighters/details/3263/")
    assert f["name"] == "Antoni Olbrychski"
    assert f["nationality"] == "Poland"
    assert f["club_id"] == "502"


def test_no_club():
    f = fighter.fighter("/fighters/details/12059/")
    assert f["name"] == "Adam Gansenberg"
    assert f["nationality"] == "United States"
    assert f["club_id"] == None


def test_no_nationality():
    f = fighter.fighter("/fighters/details/16895/")
    assert f["name"] == "Gabriel Gallegos"
    assert f["nationality"] == None
    assert f["club_id"] == "1167"

def test_only_name():
    f = fighter.fighter("/fighters/details/17021/")
    assert f["name"] == "Jarray Shen"
    assert f["nationality"] == None
    assert f["club_id"] == None
