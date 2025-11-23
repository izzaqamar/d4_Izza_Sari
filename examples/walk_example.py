#!/usr/bin/env python3

# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali
"""
Script illustrating the use of the walk package.

This script simulates Alex's random walk home from AudMax and presents
statistics on the results, including destination frequencies and walk durations.
"""

import matplotlib.pyplot as plt
import numpy as np

from walk.location import Location
from walk.experiment import Experiment


def main():
    #Run experiments with different probability configurations.
    
    # Define different scenarios to test
    scenarios = [
        {'name': 'Equal probabilities', 'p_pentagon': 0.5, 'p_kaia': 0.5},
        {'name': 'Prefer Pentagon', 'p_pentagon': 0.8, 'p_kaia': 0.3},
        {'name': 'Prefer Kaia', 'p_pentagon': 0.3, 'p_kaia': 0.8},
        {'name': 'Low probabilities', 'p_pentagon': 0.2, 'p_kaia': 0.2},
    ]
    
    # Number of simulations per scenario
    num_simulations = 1000
    seed = 42
    
    # Create figure for visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    print("=" * 70)
    print("ALEX'S WALK HOME FROM AUDMAX - SIMULATION RESULTS")
    print("=" * 70)
    print(f"\nRunning {num_simulations} simulations per scenario...\n")
    
    for idx, scenario in enumerate(scenarios):
        # Create location with specific probabilities
        location = Location(
            pentagon_pos=20,
            audmax_pos=50,
            kaia_pos=80,
            p_pentagon=scenario['p_pentagon'],
            p_kaia=scenario['p_kaia']
        )
        
        # Run experiment
        experiment = Experiment(num_simulations, seed + idx, location)
        results = experiment.execute()
        stats = experiment.analyze_results(results)
        
        # Print results
        print(f"\n{'-' * 70}")
        print(f"Scenario: {scenario['name']}")
        print(f"Location: {location.description()}")
        print(f"{'-' * 70}")
        
        print("\nDestination frequencies:")
        total = sum(stats['destinations'].values())
        for dest, count in sorted(stats['destinations'].items()):
            percentage = (count / total) * 100
            print(f"  {dest:25s}: {count:4d} ({percentage:5.1f}%)")
        
        print("\nTime statistics (seconds):")
        print(f"  Minimum : {stats['seconds']['min']:6d}")
        print(f"  Maximum : {stats['seconds']['max']:6d}")
        print(f"  Mean    : {stats['seconds']['mean']:8.1f} ± {stats['seconds']['std']:.1f}")
        
        print("\nSteps statistics:")
        print(f"  Minimum : {stats['steps']['min']:6d}")
        print(f"  Maximum : {stats['steps']['max']:6d}")
        print(f"  Mean    : {stats['steps']['mean']:8.1f} ± {stats['steps']['std']:.1f}")
        
        # Plot histogram of seconds
        ax = axes[idx]
        seconds_list = [r['seconds'] for r in results]
        ax.hist(seconds_list, bins=50, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Duration (seconds)')
        ax.set_ylabel('Frequency')
        ax.set_title(f"{scenario['name']}\n"
                    f"p_pentagon={scenario['p_pentagon']}, p_kaia={scenario['p_kaia']}")
        ax.grid(True, alpha=0.3)
        
        # Add destination info as text
        dest_text = '\n'.join([f"{dest}: {count}" 
                              for dest, count in sorted(stats['destinations'].items())])
        ax.text(0.98, 0.97, dest_text, transform=ax.transAxes,
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               fontsize=8)
    
    print(f"\n{'=' * 70}")
    print("Simulation complete!")
    print("=" * 70)
    
    plt.tight_layout()
    plt.savefig('alex_walk_results.png', dpi=150)
    print("\nResults plot saved to 'alex_walk_results.png'")
    print("Close the figure window to end the program.\n")
    plt.show()


if __name__ == '__main__':
    main()
