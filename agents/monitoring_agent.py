class MonitoringAgent:

    def observe(self, environment):
        parking_state = environment.get_state()

        observation = {}

        for zone_data in parking_state:
            zone = zone_data["zone"]

            observation[zone] = {
                "free_slots": zone_data["free_slots"],
                "entry_count": zone_data["entry_count"],
                "exit_count": zone_data["exit_count"]
            }

        return observation