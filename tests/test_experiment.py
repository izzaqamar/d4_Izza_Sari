import pytest
from walk.location import Location
from walk.experiment import Experiment


@pytest.fixture
def simple_location():
    return Location(
        pentagon_pos=20,
        audmax_pos=50,
        kaia_pos=80,
        p_pentagon=0.5,
        p_kaia=0.5
    )


def test_experiment_execute(simple_location):
    exp = Experiment(num_simulations=10, seed=123, location=simple_location)
    results = exp.execute()

    assert len(results) == 10
    assert "destination" in results[0]
    assert "seconds" in results[0]
    assert "steps" in results[0]


def test_experiment_analyze(simple_location):
    exp = Experiment(num_simulations=5, seed=321, location=simple_location)
    results = exp.execute()
    stats = exp.analyze_results(results)

    assert "destinations" in stats
    assert "seconds" in stats
    assert "steps" in stats
    assert isinstance(stats["destinations"], dict)
    assert "min" in stats["steps"]
    assert "mean" in stats["seconds"]
