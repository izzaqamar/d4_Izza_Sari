import pytest
from walk.location import Location
from walk.walker import Walker
from walk.simulation import Simulation
from walk.experiment import Experiment


@pytest.fixture(autouse=True)
def debug_walk_path():
    import walk

    print("WALK PATH:", walk.__file__)


class TestLocation:
    """Test the Location class."""

    def test_default_initialization(self):
        """Test Location with default parameters."""
        loc = Location()
        assert loc.pentagon_pos == 20
        assert loc.audmax_pos == 50
        assert loc.kaia_pos == 80
        assert loc.p_pentagon == 0.5
        assert loc.p_kaia == 0.5

    def test_custom_initialization(self):
        """Test Location with custom parameters."""
        loc = Location(
            pentagon_pos=15, audmax_pos=40, kaia_pos=70, p_pentagon=0.3, p_kaia=0.7
        )
        assert loc.pentagon_pos == 15
        assert loc.audmax_pos == 40
        assert loc.kaia_pos == 70
        assert loc.p_pentagon == 0.3
        assert loc.p_kaia == 0.7

    def test_invalid_positions(self):
        """Test that invalid positions raise ValueError."""
        with pytest.raises(ValueError):
            Location(
                pentagon_pos=60, audmax_pos=50, kaia_pos=80
            )  # Pentagon after AudMax

    def test_invalid_probabilities(self):
        """Test that invalid probabilities raise ValueError."""
        with pytest.raises(ValueError):
            Location(p_pentagon=1.5, p_kaia=0.5)
        with pytest.raises(ValueError):
            Location(p_pentagon=0.5, p_kaia=-0.1)

    def test_position_checks(self):
        """Test position checking methods."""
        loc = Location()
        assert loc.is_at_pentagon(20)
        assert not loc.is_at_pentagon(21)
        assert loc.is_at_kaia(80)
        assert not loc.is_at_kaia(79)
        assert loc.is_at_boundary(0)
        assert loc.is_at_boundary(100)
        assert not loc.is_at_boundary(50)


class TestWalker:
    """Test the Walker class."""

    def test_initialization(self):
        """Test Walker initialization."""
        loc = Location()
        walker = Walker(loc)
        assert walker.position == 50  # Starts at AudMax
        assert walker.num_seconds == 0
        assert walker.num_steps == 0
        assert walker.destination is None

    def test_take_second_increments_time(self):
        """Test that take_second always increments time."""
        loc = Location()
        walker = Walker(loc)
        initial_seconds = walker.num_seconds
        walker.take_second()
        assert walker.num_seconds == initial_seconds + 1

    def test_has_arrived_at_pentagon(self):
        """Test arrival detection at Pentagon with probability 1.0."""
        loc = Location(p_pentagon=1.0, p_kaia=0.0)
        walker = Walker(loc)
        walker.position = 20  # Move to Pentagon
        assert walker.has_arrived()
        assert walker.destination == "Pentagon"

    def test_has_arrived_at_kaia(self):
        """Test arrival detection at Kaia with probability 1.0."""
        loc = Location(p_pentagon=0.0, p_kaia=1.0)
        walker = Walker(loc)
        walker.position = 80  # Move to Kaia
        assert walker.has_arrived()
        assert walker.destination == "Kaia"

    def test_has_arrived_at_boundary(self):
        """Test arrival at boundaries."""
        loc = Location()
        walker = Walker(loc)

        # Test west boundary
        walker.position = 0
        assert walker.has_arrived()
        assert "West" in walker.destination or "E6" in walker.destination

        # Test east boundary
        walker2 = Walker(loc)
        walker2.position = 100
        assert walker2.has_arrived()
        assert "East" in walker2.destination or "Railway" in walker2.destination


class TestSimulation:
    """Test the Simulation class."""

    def test_simulation_completes(self):
        """Test that simulation runs to completion."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        sim = Simulation(loc)
        result = sim.run()

        assert "destination" in result
        assert "seconds" in result
        assert "steps" in result
        assert result["seconds"] > 0
        assert result["steps"] >= 0

    def test_simulation_result_structure(self):
        """Test that simulation result has correct structure."""
        loc = Location()
        sim = Simulation(loc)
        result = sim.run()

        assert isinstance(result, dict)
        assert isinstance(result["destination"], str)
        assert isinstance(result["seconds"], int)
        assert isinstance(result["steps"], int)


class TestExperiment:
    """Test the Experiment class."""

    def test_experiment_initialization(self):
        """Test Experiment initialization."""
        loc = Location()
        exp = Experiment(num_simulations=10, seed=42, location=loc)
        assert exp.num_simulations == 10
        assert exp.location == loc

    def test_experiment_execute(self):
        """Test that experiment runs correct number of simulations."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=5, seed=42, location=loc)
        results = exp.execute()

        assert len(results) == 5
        assert all("destination" in r for r in results)

    def test_analyze_results(self):
        """Test result analysis."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=10, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        assert "destinations" in stats
        assert "seconds" in stats
        assert "steps" in stats

        assert "min" in stats["seconds"]
        assert "max" in stats["seconds"]
        assert "mean" in stats["seconds"]
        assert "std" in stats["seconds"]
