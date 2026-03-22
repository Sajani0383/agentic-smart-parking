import random

class QLearningModel:

    def __init__(self, zones):

        self.zones = zones
        self.q_table = {}

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2


    def get_state(self, observation):

        state = tuple(
            (item["zone"], item["free_slots"])
            for item in observation
        )

        return state


    def initialize_state(self, state):

        if state not in self.q_table:

            self.q_table[state] = {}

            for zone in self.zones:

                self.q_table[state][zone] = 0


    def choose_action(self, state):

        self.initialize_state(state)

        if random.uniform(0,1) < self.epsilon:

            return random.choice(self.zones)

        q_values = self.q_table[state]

        best_action = max(q_values, key=q_values.get)

        return best_action


    def update(self, state, action, reward, next_state):

        self.initialize_state(next_state)

        current_q = self.q_table[state][action]

        max_future_q = max(self.q_table[next_state].values())

        new_q = current_q + self.alpha * (
            reward + self.gamma * max_future_q - current_q
        )

        self.q_table[state][action] = new_q


    def print_q_table(self):

        for state in self.q_table:

            print("State:", state)

            for action in self.q_table[state]:

                print("   ", action, "->", self.q_table[state][action])