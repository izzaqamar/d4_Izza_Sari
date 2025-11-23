# Inf/201 project (D4)
# Name: Izza Qamar, Sari Ali

#Module providing the Location class representing the 1D world of Ås.

#Represents the 1D geography of Ås from E6 (0) to railway line (100)
#Contains the positions of Pentagon dorms, AudMax, and Kaia dorms,
# as well as probabilities of stopping at Pentagon or Kaia.

class Location:
    def __init__(self, pentagon_pos=20, audmax_pos=50, kaia_pos=80,
                 p_pentagon=0.5, p_kaia=0.5):
        
        #Initializing the location setup.

        #pentagon_pos : (int) Position of Pentagon dorms (default: 20)
        #audmax_pos : (int) Position of AudMax where Alex starts (default: 50)
        #kaia_pos : (int) Position of Kaia dorms (default: 80)
        #p_pentagon : (float)Probability of entering Pentagon when at that position (0.0-1.0)
        #p_kaia : (float)Probability of entering Kaia when at that position (0.0-1.0)
        
        self.west_boundary = 0  # E6
        self.east_boundary = 100  # Railway line

        self.pentagon_pos = pentagon_pos
        self.audmax_pos = audmax_pos
        self.kaia_pos = kaia_pos

        self.p_pentagon = p_pentagon
        self.p_kaia = p_kaia

        # Validate positions
        if not (self.west_boundary < pentagon_pos < audmax_pos < kaia_pos < self.east_boundary):
            raise ValueError("Positions must satisfy: 0 < Pentagon < AudMax < Kaia < 100")

        # Validate probabilities
        if not (0.0 <= p_pentagon <= 1.0 and 0.0 <= p_kaia <= 1.0):
            raise ValueError("Probabilities must be between 0.0 and 1.0")

    def is_at_pentagon(self, position):
        #Check if Alex is at Pentagon position.
        return position == self.pentagon_pos

    def is_at_kaia(self, position):
        #Check if Alex is at Kaia position.
        return position == self.kaia_pos

    def is_at_boundary(self, position):
        #Check if Alex has reached a boundary (E6 or railway).
        return position <= self.west_boundary or position >= self.east_boundary

    def description(self):
        return (f"Pentagon at {self.pentagon_pos} (p={self.p_pentagon}), "
                f"AudMax at {self.audmax_pos}, "
                f"Kaia at {self.kaia_pos} (p={self.p_kaia})")
