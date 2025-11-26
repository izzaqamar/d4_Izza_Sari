# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali

# Module providing the Experiment class for running multiple simulations.

import random
from .simulation import Simulation
import numpy as np


class Experiment:

    # Represents an experiment consisting of multiple walk simulations.
    # num_simulations : (int) Number of simulations to run
    # seed : (int) Random seed for reproducibility
    # location : The Location object
    def __init__(self, num_simulations, seed, location):

        # random.seed(seed)

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.num_simulations = num_simulations
        self.location = location

    def execute(self):
        # Execute all simulations.
        # Returns list of dict (List of result dictionaries from each simulation)

        results = []
        for _ in range(self.num_simulations):
            sim = Simulation(self.location)
            results.append(sim.run())
        return results

    def analyze_results(self, results):
        # Analyze and summarize simulation results.
        # Returns Dictionary containing statistics:
        # - destinations: count of each destination
        # - seconds: dict with min, max, mean, std
        # - steps: dict with min, max, mean, std

        # Count destinations
        destinations = {}
        seconds_list = []
        steps_list = []

        for result in results:
            dest = result["destination"]
            destinations[dest] = destinations.get(dest, 0) + 1
            seconds_list.append(result["seconds"])
            steps_list.append(result["steps"])

        # Convert to numpy arrays for statistics
        seconds_array = np.array(seconds_list)
        steps_array = np.array(steps_list)

        return {
            "destinations": destinations,
            "seconds": {
                "min": int(np.min(seconds_array)),
                "max": int(np.max(seconds_array)),
                "mean": float(np.mean(seconds_array)),
                "std": float(np.std(seconds_array)),
            },
            "steps": {
                "min": int(np.min(steps_array)),
                "max": int(np.max(steps_array)),
                "mean": float(np.mean(steps_array)),
                "std": float(np.std(steps_array)),
            },
        }
