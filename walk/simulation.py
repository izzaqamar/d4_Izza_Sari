# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali

# Module providing the Simulation class for a single random walk.

from .walker import Walker


# Represents a single simulation of Alex's walk home
class Simulation:

    def __init__(self, location):

        # location : Location The Location object
        self.location = location

    def run(self):
        # Run a single simulation until Alex arrives somewhere.

        # Returns
        # destination: where Alex ended up ('Pentagon', 'Kaia', or boundary)
        # seconds: number of seconds it took
        # steps: number of steps taken

        walker = Walker(self.location)

        # Continue until Alex arrives somewhere
        while not walker.has_arrived():
            walker.take_second()

        return {
            "destination": walker.destination,
            "seconds": walker.num_seconds,
            "steps": walker.num_steps,
        }
