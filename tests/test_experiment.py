from unittest.mock import MagicMock, patch
from walk.experiment import Experiment
from walk.location import Location


@patch("walk.experiment.Simulation")
def test_experiment_execute(mock_sim):
    mock_sim_instance = MagicMock()
    mock_sim_instance.run.return_value = {"destination": "Kaia", "seconds": 5, "steps": 10}
    mock_sim.return_value = mock_sim_instance

    exp = Experiment(num_simulations=3, seed=42, location=Location())
    results = exp.execute()

    assert len(results) == 3
    assert results[0]["destination"] == "Kaia"


def test_experiment_analyze_results():
    exp = Experiment(1, 0, Location())

    fake = [
        {"destination": "Kaia", "seconds": 5, "steps": 10},
        {"destination": "Pentagon", "seconds": 7, "steps": 20},
    ]

    summary = exp.analyze_results(fake)

    assert summary["destinations"]["Kaia"] == 1
    assert summary["destinations"]["Pentagon"] == 1

    assert summary["seconds"]["min"] == 5
    assert summary["seconds"]["max"] == 7
    assert summary["steps"]["mean"] == 15.0