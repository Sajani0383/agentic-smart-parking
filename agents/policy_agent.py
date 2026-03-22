import random

class PolicyAgent:

    def __init__(self, zones):
        self.zones = zones
        self.epsilon = 0.3

    def choose_zone(self, demand):

        # Exploration
        if random.random() < self.epsilon:
            zone = random.choice(self.zones)
            mode = "Exploration"

        # Exploitation
        else:

            if demand:

                priority = {
                    "LOW": 0,
                    "MEDIUM": 1,
                    "HIGH": 2
                }

                zone = max(
                    demand,
                    key=lambda z: priority[demand[z]]
                )

            else:
                zone = random.choice(self.zones)

            mode = "Exploitation"

        return zone, mode
    