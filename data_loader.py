import pandas as pd


class DataLoader:

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.data = None


    def load_data(self):

        self.data = pd.read_csv(self.dataset_path)

        return self.data


    def clean_data(self):

        if self.data is None:
            raise ValueError("Dataset not loaded")

        self.data = self.data.dropna(subset=["zone"])

        if "date_time" in self.data.columns:
            self.data["date_time"] = pd.to_datetime(
                self.data["date_time"],
                errors="coerce"
            )

        numeric_columns = [
            "total_slots",
            "occupied_slots",
            "entry_count",
            "exit_count",
            "parking_fee_collection"
        ]

        for col in numeric_columns:

            if col in self.data.columns:

                self.data[col] = self.data[col].fillna(0)

        return self.data


    def get_zones(self):

        if self.data is None:
            raise ValueError("Dataset not loaded")

        return self.data["zone"].unique().tolist()


    def get_zone_data(self, zone):

        if self.data is None:
            raise ValueError("Dataset not loaded")

        return self.data[self.data["zone"] == zone]


    def get_traffic_data(self):

        if self.data is None:
            raise ValueError("Dataset not loaded")

        return self.data[
            [
                "zone",
                "entry_count",
                "exit_count"
            ]
        ]