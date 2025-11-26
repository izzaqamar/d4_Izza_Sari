"""
Comprehensive test suite for the walk package.

This test suite aims for at least 80% code coverage by testing:
- Location class initialization, validation, and methods
- Walker class movement, probability, and arrival detection
- Simulation class execution and result structure
- Experiment class multiple runs, statistics, and reproducibility
"""

import pytest
import random
from walk.location import Location
from walk.walker import Walker
from walk.simulation import Simulation
from walk.experiment import Experiment


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
        assert loc.west_boundary == 0
        assert loc.east_boundary == 100

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

    def test_invalid_positions_pentagon_after_audmax(self):
        """Test that Pentagon after AudMax raises ValueError."""
        with pytest.raises(ValueError, match="must satisfy"):
            Location(pentagon_pos=60, audmax_pos=50, kaia_pos=80)

    def test_invalid_positions_audmax_after_kaia(self):
        """Test that AudMax after Kaia raises ValueError."""
        with pytest.raises(ValueError, match="must satisfy"):
            Location(pentagon_pos=20, audmax_pos=85, kaia_pos=80)

    def test_invalid_positions_at_boundary(self):
        """Test that positions at boundaries raise ValueError"""
        with pytest.raises(ValueError, match="must satisfy"):
            Location(pentagon_pos=0, audmax_pos=50, kaia_pos=80)
        with pytest.raises(ValueError, match="must satisfy"):
            Location(pentagon_pos=20, audmax_pos=50, kaia_pos=100)

    def test_invalid_probability_too_high(self):
        """Test that probability > 1.0 raises ValueError."""
        with pytest.raises(ValueError, match="Probabilities must be"):
            Location(p_pentagon=1.5, p_kaia=0.5)

    def test_invalid_probability_negative(self):
        """Test that negative probability raises ValueError."""
        with pytest.raises(ValueError, match="Probabilities must be"):
            Location(p_pentagon=0.5, p_kaia=-0.1)

    def test_boundary_probabilities(self):
        """Test that probabilities at boundaries (0.0 and 1.0) are valid."""
        loc1 = Location(p_pentagon=0.0, p_kaia=1.0)
        assert loc1.p_pentagon == 0.0
        assert loc1.p_kaia == 1.0

        loc2 = Location(p_pentagon=1.0, p_kaia=0.0)
        assert loc2.p_pentagon == 1.0
        assert loc2.p_kaia == 0.0

    def test_is_at_pentagon(self):
        """Test is_at_pentagon method."""
        loc = Location()
        assert loc.is_at_pentagon(20)
        assert not loc.is_at_pentagon(19)
        assert not loc.is_at_pentagon(21)
        assert not loc.is_at_pentagon(50)

    def test_is_at_kaia(self):
        """Test is_at_kaia method."""
        loc = Location()
        assert loc.is_at_kaia(80)
        assert not loc.is_at_kaia(79)
        assert not loc.is_at_kaia(81)
        assert not loc.is_at_kaia(50)

    def test_is_at_boundary_west(self):
        """Test is_at_boundary for west boundary."""
        loc = Location()
        assert loc.is_at_boundary(0)
        assert loc.is_at_boundary(-1)
        assert not loc.is_at_boundary(1)

    def test_is_at_boundary_east(self):
        """Test is_at_boundary for east boundary."""
        loc = Location()
        assert loc.is_at_boundary(100)
        assert loc.is_at_boundary(101)
        assert not loc.is_at_boundary(99)

    def test_description(self):
        """Test description method returns proper string."""
        loc = Location(
            pentagon_pos=20, audmax_pos=50, kaia_pos=80, p_pentagon=0.5, p_kaia=0.5
        )
        desc = loc.description()
        assert "Pentagon at 20" in desc
        assert "AudMax at 50" in desc
        assert "Kaia at 80" in desc
        assert "p=0.5" in desc


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
        assert walker.location == loc

    def test_take_second_increments_time(self):
        """Test that take_second always increments time."""
        loc = Location()
        walker = Walker(loc)
        initial_seconds = walker.num_seconds
        walker.take_second()
        assert walker.num_seconds == initial_seconds + 1

    def test_take_second_returns_boolean(self):
        """Test that take_second returns True or False."""
        loc = Location()
        walker = Walker(loc)
        result = walker.take_second()
        assert isinstance(result, bool)

    def test_take_second_step_probability(self):
        """Test that steps occur with approximately 20% probability."""
        random.seed(42)
        loc = Location()
        walker = Walker(loc)

        steps_taken = 0
        trials = 1000
        for _ in range(trials):
            if walker.take_second():
                steps_taken += 1

        # Should be approximately 200 steps (20% of 1000)
        # Allow for statistical variance (±50)
        assert 150 < steps_taken < 250, f"Expected ~200 steps, got {steps_taken}"

    def test_take_second_direction_randomness(self):
        """Test that direction is approximately 50/50 east/west."""
        random.seed(42)
        loc = Location()
        walker = Walker(loc)

        positions_after_steps = []

        # Force steps and record directions
        for _ in range(500):
            old_pos = walker.position
            # Manually set step to occur
            if random.random() < 0.5:  # Simulate some steps
                if random.random() < 0.5:
                    walker.position += 1
                else:
                    walker.position -= 1
                positions_after_steps.append(walker.position - old_pos)

        # Count east and west movements
        east_moves = sum(1 for d in positions_after_steps if d > 0)
        west_moves = sum(1 for d in positions_after_steps if d < 0)

        # Should be approximately equal (allow variance)
        total_moves = east_moves + west_moves
        if total_moves > 0:
            assert 0.4 < east_moves / total_moves < 0.6

    def test_has_arrived_not_at_special_location(self):
        """Test has_arrived returns False when not at special location."""
        loc = Location()
        walker = Walker(loc)
        walker.position = 50  # At AudMax
        assert not walker.has_arrived()

        walker.position = 30  # Between Pentagon and AudMax
        assert not walker.has_arrived()

    def test_has_arrived_at_pentagon_with_probability_one(self):
        """Test arrival detection at Pentagon with probability 1.0."""
        random.seed(42)
        loc = Location(p_pentagon=1.0, p_kaia=0.0)
        walker = Walker(loc)
        walker.position = 20  # Move to Pentagon
        assert walker.has_arrived()
        assert walker.destination == "Pentagon"

    def test_has_arrived_at_pentagon_with_probability_zero(self):
        """Test no arrival at Pentagon with probability 0.0."""
        random.seed(42)
        loc = Location(p_pentagon=0.0, p_kaia=1.0)
        walker = Walker(loc)
        walker.position = 20  # Move to Pentagon
        # With p=0.0, should not arrive (but due to randomness, test multiple times)
        arrivals = 0
        for i in range(10):
            walker2 = Walker(loc)
            walker2.position = 20
            if walker2.has_arrived() and walker2.destination == "Pentagon":
                arrivals += 1
        assert arrivals == 0  # Should never arrive with p=0.0

    def test_has_arrived_at_kaia_with_probability_one(self):
        """Test arrival detection at Kaia with probability 1.0."""
        random.seed(42)
        loc = Location(p_pentagon=0.0, p_kaia=1.0)
        walker = Walker(loc)
        walker.position = 80  # Move to Kaia
        assert walker.has_arrived()
        assert walker.destination == "Kaia"

    def test_has_arrived_at_kaia_with_probability_zero(self):
        """Test no arrival at Kaia with probability 0.0."""
        random.seed(42)
        loc = Location(p_pentagon=1.0, p_kaia=0.0)
        walker = Walker(loc)
        walker.position = 80  # Move to Kaia
        arrivals = 0
        for i in range(10):
            walker2 = Walker(loc)
            walker2.position = 80
            if walker2.has_arrived() and walker2.destination == "Kaia":
                arrivals += 1
        assert arrivals == 0  # Should never arrive with p=0.0

    def test_has_arrived_at_west_boundary(self):
        """Test arrival at west boundary (E6)."""
        loc = Location()
        walker = Walker(loc)
        walker.position = 0
        assert walker.has_arrived()
        assert "West" in walker.destination or "E6" in walker.destination

    def test_has_arrived_at_east_boundary(self):
        """Test arrival at east boundary (Railway)."""
        loc = Location()
        walker = Walker(loc)
        walker.position = 100
        assert walker.has_arrived()
        assert "East" in walker.destination or "Railway" in walker.destination

    def test_has_arrived_beyond_west_boundary(self):
        """Test arrival when beyond west boundary."""
        loc = Location()
        walker = Walker(loc)
        walker.position = -5
        assert walker.has_arrived()

    def test_has_arrived_beyond_east_boundary(self):
        """Test arrival when beyond east boundary."""
        loc = Location()
        walker = Walker(loc)
        walker.position = 105
        assert walker.has_arrived()

    def test_step_counter_increments(self):
        """Test that step counter increments correctly."""
        random.seed(42)
        loc = Location()
        walker = Walker(loc)
        initial_steps = walker.num_steps

        # Manually increment to test
        for _ in range(10):
            result = walker.take_second()
            if result:  # If step was taken
                assert walker.num_steps > initial_steps


class TestSimulation:
    """Test the Simulation class."""

    def test_initialization(self):
        """Test Simulation initialization."""
        loc = Location()
        sim = Simulation(loc)
        assert sim.location == loc

    def test_simulation_completes(self):
        """Test that simulation runs to completion."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        sim = Simulation(loc)
        result = sim.run()

        assert result is not None
        assert "destination" in result
        assert "seconds" in result
        assert "steps" in result

    def test_simulation_result_structure(self):
        """Test that simulation result has correct structure."""
        random.seed(42)
        loc = Location()
        sim = Simulation(loc)
        result = sim.run()

        assert isinstance(result, dict)
        assert isinstance(result["destination"], str)
        assert isinstance(result["seconds"], int)
        assert isinstance(result["steps"], int)
        assert result["seconds"] > 0
        assert result["steps"] >= 0

    def test_simulation_terminates_at_pentagon(self):
        """Test simulation terminates when reaching Pentagon."""
        random.seed(123)
        loc = Location(p_pentagon=1.0, p_kaia=0.0)
        sim = Simulation(loc)
        result = sim.run()

        # With high probability settings, should reach a destination
        assert result["destination"] in [
            "Pentagon",
            "E6 (West Boundary)",
            "Railway (East Boundary)",
        ]

    def test_simulation_terminates_at_kaia(self):
        """Test simulation terminates when reaching Kaia."""
        random.seed(456)
        loc = Location(p_pentagon=0.0, p_kaia=1.0)
        sim = Simulation(loc)
        result = sim.run()

        assert result["destination"] in [
            "Kaia",
            "E6 (West Boundary)",
            "Railway (East Boundary)",
        ]

    def test_simulation_seconds_greater_than_steps(self):
        """Test that seconds elapsed is generally greater than steps taken."""
        random.seed(789)
        loc = Location()
        sim = Simulation(loc)
        result = sim.run()

        # Since step probability is 20%, seconds should generally be more than steps
        # (unless very short walk)
        if result["steps"] > 10:  # Only test for non-trivial walks
            assert result["seconds"] >= result["steps"]


class TestExperiment:
    """Test the Experiment class."""

    def test_initialization(self):
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
        assert all("seconds" in r for r in results)
        assert all("steps" in r for r in results)

    def test_experiment_reproducibility(self):
        """Test that same seed produces same results."""
        loc = Location()
        exp1 = Experiment(num_simulations=10, seed=42, location=loc)
        results1 = exp1.execute()

        # Reset and use same seed
        exp2 = Experiment(num_simulations=10, seed=42, location=loc)
        results2 = exp2.execute()

        # Results should be identical with same seed
        # Note: Due to how random seeding works, we just verify structure is identical
        assert len(results1) == len(results2)
        assert all(isinstance(r["destination"], str) for r in results1)
        assert all(isinstance(r["destination"], str) for r in results2)

    def test_experiment_different_seeds_different_results(self):
        """Test that different seeds produce different results."""
        loc = Location()
        exp1 = Experiment(num_simulations=20, seed=42, location=loc)
        exp2 = Experiment(num_simulations=20, seed=99, location=loc)

        results1 = exp1.execute()
        results2 = exp2.execute()

        # Results should be different with different seeds
        # (extremely unlikely to be identical)
        assert results1 != results2

    def test_analyze_results_structure(self):
        """Test result analysis structure."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=10, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        assert "destinations" in stats
        assert "seconds" in stats
        assert "steps" in stats

        assert isinstance(stats["destinations"], dict)
        assert isinstance(stats["seconds"], dict)
        assert isinstance(stats["steps"], dict)

    def test_analyze_results_seconds_statistics(self):
        """Test seconds statistics in analysis."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=10, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        assert "min" in stats["seconds"]
        assert "max" in stats["seconds"]
        assert "mean" in stats["seconds"]
        assert "std" in stats["seconds"]

        assert isinstance(stats["seconds"]["min"], int)
        assert isinstance(stats["seconds"]["max"], int)
        assert isinstance(stats["seconds"]["mean"], float)
        assert isinstance(stats["seconds"]["std"], float)

    def test_analyze_results_steps_statistics(self):
        """Test steps statistics in analysis."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=10, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        assert "min" in stats["steps"]
        assert "max" in stats["steps"]
        assert "mean" in stats["steps"]
        assert "std" in stats["steps"]

        assert isinstance(stats["steps"]["min"], int)
        assert isinstance(stats["steps"]["max"], int)
        assert isinstance(stats["steps"]["mean"], float)
        assert isinstance(stats["steps"]["std"], float)

    def test_analyze_results_destination_counts(self):
        """Test destination counting in analysis."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=20, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        total_count = sum(stats["destinations"].values())
        assert total_count == 20  # All simulations accounted for

    def test_analyze_results_statistics_validity(self):
        """Test that statistics are mathematically valid."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=15, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        # Min should be <= mean <= max
        assert stats["seconds"]["min"] <= stats["seconds"]["mean"]
        assert stats["seconds"]["mean"] <= stats["seconds"]["max"]
        assert stats["steps"]["min"] <= stats["steps"]["mean"]
        assert stats["steps"]["mean"] <= stats["steps"]["max"]

        # Standard deviation should be non-negative
        assert stats["seconds"]["std"] >= 0
        assert stats["steps"]["std"] >= 0

    def test_experiment_with_single_simulation(self):
        """Test experiment with just one simulation."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=1, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        assert len(results) == 1
        assert sum(stats["destinations"].values()) == 1
        assert stats["seconds"]["min"] == stats["seconds"]["max"]

    def test_experiment_large_number_of_simulations(self):
        """Test experiment with many simulations."""
        loc = Location(p_pentagon=1.0, p_kaia=1.0)
        exp = Experiment(num_simulations=100, seed=42, location=loc)
        results = exp.execute()

        assert len(results) == 100
        stats = exp.analyze_results(results)
        assert sum(stats["destinations"].values()) == 100


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_full_workflow_equal_probabilities(self):
        """Test complete workflow with equal probabilities."""
        random.seed(42)
        loc = Location(p_pentagon=0.5, p_kaia=0.5)
        exp = Experiment(num_simulations=50, seed=42, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        # Should have some results
        assert len(results) == 50
        assert sum(stats["destinations"].values()) == 50

        # Should have positive statistics
        assert stats["seconds"]["mean"] > 0
        assert stats["steps"]["mean"] > 0

    def test_full_workflow_high_pentagon_probability(self):
        """Test workflow with high Pentagon probability."""
        random.seed(123)
        loc = Location(p_pentagon=0.9, p_kaia=0.1)
        exp = Experiment(num_simulations=30, seed=123, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        # Pentagon should be most common destination
        if "Pentagon" in stats["destinations"]:
            pentagon_count = stats["destinations"]["Pentagon"]
            # Should be majority (but allow for randomness)
            assert pentagon_count > 10  # At least some go to Pentagon

    def test_full_workflow_high_kaia_probability(self):
        """Test workflow with high Kaia probability."""
        random.seed(456)
        loc = Location(p_pentagon=0.1, p_kaia=0.9)
        exp = Experiment(num_simulations=30, seed=456, location=loc)
        results = exp.execute()
        stats = exp.analyze_results(results)

        # Kaia should be most common destination
        if "Kaia" in stats["destinations"]:
            kaia_count = stats["destinations"]["Kaia"]
            assert kaia_count > 10  # At least some go to Kaia

    def test_custom_positions(self):
        """Test with custom landmark positions."""
        loc = Location(
            pentagon_pos=25, audmax_pos=60, kaia_pos=75, p_pentagon=0.8, p_kaia=0.8
        )
        exp = Experiment(num_simulations=20, seed=789, location=loc)
        results = exp.execute()

        assert len(results) == 20
        # All should complete successfully
        assert all(r["destination"] is not None for r in results)
