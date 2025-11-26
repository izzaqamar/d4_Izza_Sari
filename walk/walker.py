# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali

# Module providing the Walker class representing Alex's random walk.

import random
import numpy as np


# Represents Alex walking home with unsteady steps.
class Walker:

    STEP_PROBABILITY = 0.2
    EAST_PROBABILITY = 0.5

    def __init__(self, location, seed=None):
        # Initializing walker at AudMax.
        self.location = location
        self.position = location.audmax_pos
        self.num_seconds = 0
        self.num_steps = 0
        self.destination = None  # Will be 'Pentagon', 'Kaia', or 'Boundary'

        #  Apply seed if provided
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def take_second(self):
        self.num_seconds += 1

        # Check if Alex takes a step this second (20% probability)
        if random.random() < self.STEP_PROBABILITY:
            self.num_steps += 1

            # Determine direction (50% east, 50% west)
            if random.random() < self.EAST_PROBABILITY:
                self.position += 1  # Move east
            else:
                self.position -= 1  # Move west

            return True

        return False

    def has_arrived(self):
        # Check if Alex has arrived at a destination.

        # Check if at Pentagon
        if self.location.is_at_pentagon(self.position):
            if random.random() < self.location.p_pentagon:
                self.destination = "Pentagon"
                return True

        # Check if at Kaia
        if self.location.is_at_kaia(self.position):
            if random.random() < self.location.p_kaia:
                self.destination = "Kaia"
                return True

        # Check if at boundary (E6 or railway)
        if self.location.is_at_boundary(self.position):
            if self.position <= self.location.west_boundary:
                self.destination = "E6 (West Boundary)"
            else:
                self.destination = "Railway (East Boundary)"
            return True

        return False
