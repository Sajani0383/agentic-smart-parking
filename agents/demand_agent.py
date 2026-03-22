class DemandAgent:

    def predict(self, parking_state):
        demand = {}

        for zone, data in parking_state.items():
            free = data["free_slots"]

            if free > 60:
                demand[zone] = "LOW"
            elif free > 30:
                demand[zone] = "MEDIUM"
            else:
                demand[zone] = "HIGH"

        return demand