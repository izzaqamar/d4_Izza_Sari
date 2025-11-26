from unittest.mock import patch, MagicMock
import pytest

# Patch the imports as used in main.py
@patch("walk.main.Experiment")
@patch("walk.main.Location")
@patch("walk.main.plt")
def test_main_runs_without_crashing(mock_plt, mock_Location, mock_Experiment):
    mock_Location.return_value.description.return_value = "Mocked location"

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
    mock_plt.show.return_value = None

    # Import main after patching
    from walk import main

    main.main()

    # Should be called 4 times (once per location)
    assert mock_Experiment.call_count == 4