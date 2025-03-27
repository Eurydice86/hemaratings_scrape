from src import events

def test_Keppinautur_24():
    e = events.event("/events/details/2019/", 2024)
    assert e["event_name"] == "Keppinautur 2024"
    assert e["event_id"] == "2019"
    assert e["country"] == "Iceland"
    assert e["city"] == "Hella"
    assert e["date"] == "2024-3-22"
    
def test_SoCal_25():
    e = events.event("/events/details/2334/", 2025)
    assert e["event_name"] == "SoCal Swordfight 2025"
    assert e["event_id"] == "2334"
    assert e["country"] == "United States"
    assert e["city"] == "Los Angeles"
    assert e["date"] == "2025-3-14"

def test_MiniFecht_25():
    e = events.event("/events/details/2330/", 2025)
    assert e["event_name"] == "MiniFecht 2025"
    assert e["event_id"] == "2330"
    assert e["country"] == "Slovakia"
    assert e["city"] == "Bratislava"
    assert e["date"] == "2025-3-15"


def test_BrunnerStich_23():
    e = events.event("/events/details/1813/", 2023)
    assert e["event_name"] == "Brunner Stich 2023"
    assert e["event_id"] == "1813"
    assert e["country"] == "Czech Republic"
    assert e["city"] == None
    assert e["date"] == "2023-5-13"

