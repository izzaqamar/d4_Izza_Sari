from  unittest.mock import MagicMock, patch
from walk.location import Location
from walk.simulation import Simulation



@patch("walk.simulation.Walker")
def test_simulation_run(mock_walker):
    mock_instance = MagicMock()
    mock_instance.has_arrived.side_effect = [False, True]
    mock_instance.destination = "Kaia"
    mock_instance.num_seconds = 5
    mock_instance.num_steps = 3

    mock_walker.return_value = mock_instance

    loc = Location()
    sim = Simulation(loc)

    result = sim.run()

    assert result["destination"] == "Kaia"
    assert result["seconds"] == 5
    assert result["steps"] == 3
    assert mock_walker.called