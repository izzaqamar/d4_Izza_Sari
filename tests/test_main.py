import pytest
from unittest.mock import patch, MagicMock


@patch("main.Experiment")
@patch("main.Location")
@patch("main.plt")
def test_main_runs_without_crashing(mock_plt, mock_Location, mock_Experiment):
    # Mock location object
    mock_Location.return_value.description.return_value = "Mocked location"

    # Mock experiment behavior
    mock_exp_instance = MagicMock()
    mock_exp_instance.execute.return_value = [
        {"destination": "Kaia", "seconds": 5, "steps": 20},
        {"destination": "Pentagon", "seconds": 7, "steps": 30},
    ]
    mock_exp_instance.analyze_results.return_value = {
        "destinations": {"Kaia": 1, "Pentagon": 1},
        "seconds": {"min": 5, "max": 7, "mean": 6, "std": 1},
        "steps": {"min": 20, "max": 30, "mean": 25, "std": 5},
    }
    mock_Experiment.return_value = mock_exp_instance

    # Prevent plots from opening
    mock_plt.show.return_value = None


    # Check we created 4 scenarios
    assert mock_Experiment.call_count == 4