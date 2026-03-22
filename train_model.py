from data_loader import DataLoader
from models.q_learning import QLearningModel


def train_model():

    print("Training Parking Decision Model")

    # -------------------------
    # LOAD DATASET
    # -------------------------

    loader = DataLoader("dataset/parking_dataset.csv")

    dataset = loader.load_data()

    dataset = loader.clean_data()

    zones = loader.get_zones()

    print("Zones:", zones)

    # -------------------------
    # INITIALIZE MODEL
    # -------------------------

    model = QLearningModel(zones)

    # -------------------------
    # TRAINING LOOP
    # -------------------------

    for i in range(1000):

        # simulate observation state
        observation = []

        for zone in zones:

            free_slots = dataset[
                dataset["zone"] == zone
            ]["total_slots"].mean() - dataset[
                dataset["zone"] == zone
            ]["occupied_slots"].mean()

            observation.append({
                "zone": zone,
                "free_slots": int(free_slots)
            })

        state = model.get_state(observation)

        action = model.choose_action(state)

        reward = 1

        next_state = state

        model.update(state, action, reward, next_state)

    print("Training completed")

    model.print_q_table()


if __name__ == "__main__":

    train_model()