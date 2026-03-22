class Vehicle:

    def __init__(self, vehicle_id, zone):

        self.vehicle_id = vehicle_id
        self.current_zone = zone
        self.parked = False

    def move_to(self, zone):

        self.current_zone = zone

    def park(self):

        self.parked = True