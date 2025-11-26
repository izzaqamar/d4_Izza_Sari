import pytest
from walk.location import Location


def test_location_valid_creation():
    loc = Location()
    assert loc.pentagon_pos == 20
    assert loc.audmax_pos == 50
    assert loc.kaia_pos == 80


def test_location_invalid_positions():
    # Pentagon must be < AudMax < Kaia
    with pytest.raises(ValueError):
        Location(pentagon_pos=60, audmax_pos=50, kaia_pos=80)


def test_location_invalid_probabilities():
    with pytest.raises(ValueError):
        Location(p_pentagon=1.5)


def test_location_checks():
    loc = Location()

    assert loc.is_at_pentagon(20)
    assert loc.is_at_kaia(80)
    assert loc.is_at_boundary(0)
    assert loc.is_at_boundary(100)
    assert not loc.is_at_boundary(50)


def test_description():
    loc = Location()
    text = loc.description()
    assert "Pentagon" in text
    assert "Kaia" in text
    