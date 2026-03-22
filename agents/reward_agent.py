class RewardAgent:

    def compute_reward(self, environment, chosen_zone):

        free_slots = environment.get_free_slots(chosen_zone)

        if free_slots > 50:
            reward = 2
        elif free_slots > 20:
            reward = 1
        else:
            reward = -1

        return reward