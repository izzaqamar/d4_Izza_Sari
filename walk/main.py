# walk/main.py
from .location import Location
from .experiment import Experiment
import matplotlib.pyplot as plt


def main():
    # Locations to simulate
    location_names = ["Kaia", "Pentagon", "Library", "Dorm"]

    for name in location_names:
        # Create a Location object
        loc = Location()
        exp = Experiment(num_simulations=10, seed=42, location=loc)

        results = exp.execute()
        summary = exp.analyze_results(results)
        print(f"Results for {name}: {summary}")

    # Show plots (can be mocked in tests)
    plt.show()


# Only run main when executed directly
if __name__ == "__main__":
    main()
    