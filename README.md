# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali

# Github Repository Link: " https://github.com/izzaqamar/d4_Izza_Sari.git " 

Code Inspiration: The structure and layout of this project is inspired and taken from  https://gitlab.com/heplesser/chutes.

# The final code is present on the main branch

**Task1**: To implement the random-walk simulation, we created a dedicated Python package named walk, following the same modular code structure as the provided chutes package. The folder contains separate files for each main component of the simulation (location.py, walker.py, simulation.py, experiment.py, and __init__.py), making the package fully importable and easy to extend. An additional example script is included outside the package in the example folder to demonstrate how to run large batches of simulations and compute summary statistics.
The package was developed in multiple incremental steps in github.

**Task2**: For task 2 test suite was created for the walk package and a tests folder, targeting at least 80% test coverage. The project is fully configured for packaging using a pyproject.toml file, which also defines a tox environment for running both the flake8 style checks and the complete testsuite. A *.github/workflows/ci.yml* workflow file was added to enable continuous integration, automatically running all tests and style checks on every push to Github.

**Task3**: For task 3 a dedicated Jupyter notebook was created to explore how the simulation behaves under different values of p_kaia and p_pentagon. It summarizes the outcomes, and presents the results both numerically and  visualizations as line plots.