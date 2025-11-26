from unittest.mock import patch
from walk.location import Location
from walk.walker import Walker


def test_walker_initial_state():
    loc = Location()
    w = Walker(loc)
    assert w.position == loc.audmax_pos
    assert w.num_steps == 0
    assert w.num_seconds == 0


@patch("random.random", side_effect=[0.1, 0.1])  # step taken + move east
def test_take_second_step_east(mock_rand):
    loc = Location()
    w = Walker(loc)
    took_step = w.take_second()

    assert took_step is True
    assert w.position == loc.audmax_pos + 1
    assert w.num_steps == 1
    assert w.num_seconds == 1


@patch("random.random", return_value=0.9)  # no step
def test_take_second_no_step(mock_rand):
    loc = Location()
    w = Walker(loc)
    took_step = w.take_second()

    assert took_step is False
    assert w.position == loc.audmax_pos
    assert w.num_steps == 0
    assert w.num_seconds == 1


@patch("random.random", return_value=0.0)
def test_arrival_pentagon(mock_rand):
    loc = Location()
    loc.p_pentagon = 1.0  # guaranteed to enter
    w = Walker(loc)
    w.position = loc.pentagon_pos

    assert w.has_arrived() is True
    assert w.destination == "Pentagon"