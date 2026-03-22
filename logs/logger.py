import pandas as pd
import os

class SimulationLogger:

    def __init__(self):

        self.logs = []
        self.log_file = "simulation_logs.csv"

    def reset_logs(self):

        self.logs = []

        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def log_step(self, data):

        self.logs.append(data)

        df = pd.DataFrame([data])

        if not os.path.exists(self.log_file):
            df.to_csv(self.log_file, index=False)
        else:
            df.to_csv(self.log_file, mode='a', header=False, index=False)