import json
import os


class AgentMemory:

    def __init__(self):

        self.file = "agent_memory.json"

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def save(self, step, zone, reward):

        with open(self.file, "r") as f:
            data = json.load(f)

        data.append({
            "step": step,
            "zone": zone,
            "reward": reward
        })

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):

        with open(self.file, "r") as f:
            data = json.load(f)

        return data