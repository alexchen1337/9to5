class Meter:
    def __init__(self, name, max_value, min_value=0, hidden=False):
        self.name = name
        self.value = max_value
        self.max_value = max_value
        self.min_value = min_value
        self.history = []
        self.hidden = hidden  # Flag to keep track if the meter is hidden

    def increase(self, amount):
        self.history.append(self.value)
        self.value = min(self.max_value, self.value + amount)
        if not self.hidden:
            print(f"{self.name} increased by {amount} to {self.value}/{self.max_value}")

    def decrease(self, amount):
        self.history.append(self.value)
        self.value = max(self.min_value, self.value - amount)
        if not self.hidden:
            print(f"{self.name} decreased by {amount} to {self.value}/{self.max_value}")

    def is_depleted(self):
        return self.value <= self.min_value

    def __str__(self):
        return f"{self.name}: {self.value}/{self.max_value}" if not self.hidden else f"{self.name} (Hidden)"

    # Returns meter levels history at the end of the game
    def get_history(self):
        return self.history
    
    # Returns the current meter value
    def get_value(self):
        return self.value
    
    # Sets value with an increase or decrease based on `change` amount
    def set_value(self, change):
        if change > 0:
            self.increase(change)
        else:
            self.decrease(-change)
    
    # Output warning if meter level is too low
    def level_warning(self):
        if self.value < 0.2 * self.max_value:
            print(f"Warning: {self.name} is low!")

    # Checks if the meter is hidden and still outputs warning if level is low
    def hidden_warning(self):
        if self.hidden and self.value < 0.2 * self.max_value:
            print(f"Warning: {self.name} is at a critical level!")


# Instantiate visible meters
health_meter = Meter("Health", max_value=100)
energy_meter = Meter("Energy", max_value=100)
family_happiness_meter = Meter("Family Happiness", max_value=100)

# Instantiate hidden meters
boss_happiness_meter = Meter("Boss Happiness", max_value=100, hidden=True)
wife_happiness_meter = Meter("Wife Happiness", max_value=100, hidden=True)

# Example action to test the hidden meters
def perform_action(action):
    if action == "work_overtime":
        boss_happiness_meter.increase(5)  # Boss is happier
        family_happiness_meter.decrease(10)  # Family happiness decreases
        wife_happiness_meter.decrease(5)  # Wife happiness decreases
    elif action == "family_time":
        family_happiness_meter.increase(10)
        wife_happiness_meter.increase(7)
        boss_happiness_meter.decrease(3)  # Boss happiness decreases if you skip work

# Function to check for warnings on hidden meters
def check_hidden_meters():
    boss_happiness_meter.hidden_warning()
    wife_happiness_meter.hidden_warning()
