from walk.location import Location


def test_location_initialization():
    loc = Location(
        pentagon_pos=20, audmax_pos=50, kaia_pos=80, p_pentagon=0.5, p_kaia=0.3
    )

    assert loc.pentagon_pos == 20
    assert loc.audmax_pos == 50
    assert loc.kaia_pos == 80
    assert loc.p_pentagon == 0.5
    assert loc.p_kaia == 0.3


def test_description_contains_keywords():
    loc = Location(20, 50, 80, 0.5, 0.5)
    desc = loc.description()

    assert isinstance(desc, str)
    assert "Pentagon" in desc or "pentagon" in desc
    assert "Kaia" in desc or "kaia" in desc
