import random

class ParkingEnvironment:

    def __init__(self, zones):
        self.zones = zones

        self.total_slots = {zone: random.randint(80, 100) for zone in zones}
        self.occupied_slots = {zone: random.randint(10, 50) for zone in zones}

        self.entry_count = {zone: 0 for zone in zones}
        self.exit_count = {zone: 0 for zone in zones}

    def reset(self):
        for zone in self.zones:
            self.occupied_slots[zone] = random.randint(10, 50)
            self.entry_count[zone] = 0
            self.exit_count[zone] = 0
        return self.get_state()

    def get_free_slots(self, zone):
        return self.total_slots[zone] - self.occupied_slots[zone]

    def get_state(self):
        state = []

        for zone in self.zones:
            state.append({
                "zone": zone,
                "free_slots": self.get_free_slots(zone),
                "entry_count": self.entry_count[zone],
                "exit_count": self.exit_count[zone]
            })

        return state

    def step(self, action):
        # simulate entries and exits
        for zone in self.zones:
            entry = random.randint(0, 10)
            exit = random.randint(0, 10)

            self.entry_count[zone] = entry
            self.exit_count[zone] = exit

            self.occupied_slots[zone] += entry - exit

            # keep within limits
            self.occupied_slots[zone] = max(
                0,
                min(self.occupied_slots[zone], self.total_slots[zone])
            )

        # reward logic
        free_slots = self.get_free_slots(action)

        if free_slots > 50:
            reward = 2
        elif free_slots > 20:
            reward = 1
        else:
            reward = -1

        return self.get_state(), reward