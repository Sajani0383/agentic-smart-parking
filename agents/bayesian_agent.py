class BayesianAgent:

    def compute_probability(self, parking_state):
        congestion = {}

        for zone, data in parking_state.items():
            free_slots = data["free_slots"]

            prob = round(1 - (free_slots / 100), 2)
            congestion[zone] = prob

        return congestion