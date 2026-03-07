class ModelBasedReflexAgent:
    
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.heater_state = "OFF"   # Internal memory (model)

    def perceive(self, current_temperature):
        return current_temperature

    def act(self, current_temperature):
        
        # If temperature is below desired and heater is OFF -> turn ON
        if current_temperature < self.desired_temperature and self.heater_state == "OFF":
            self.heater_state = "ON"
            action = "Turn on heater"
        
        # If temperature is above desired and heater is ON -> turn OFF
        elif current_temperature >= self.desired_temperature and self.heater_state == "ON":
            self.heater_state = "OFF"
            action = "Turn off heater"
        
        # Otherwise -> keep previous state (no unnecessary switching)
        else:
            action = f"No change (Heater remains {self.heater_state})"
        
        return action


# Simulating different rooms
rooms = {
    "Living Room": 18,
    "Bedroom": 22,
    "Kitchen": 20,
    "Bathroom": 24
}

desired_temperature = 22

agent = ModelBasedReflexAgent(desired_temperature)

# Run the agent
for room, temperature in rooms.items():
    action = agent.act(temperature)
    print(f"{room}: Current temperature = {temperature}°C -> {action}.")