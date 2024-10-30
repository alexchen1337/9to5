# Meters for Health, Energy, Family Happiness

class Meter:
    def __init__(self, name, max_value, min_value=0):
        self.name = name
        self.value = max_value
        self.max_value = max_value
        self.min_value = min_value
        self.history = []

    def increase(self, amount):
        self.history.append(self.value)
        self.value = self.value + amount

    def decrease(self, amount):
        self.history.append(-1*self.value)
        self.value = self.value = self.value - amount

    def is_depleted(self):
        return self.value <= self.min_value

    def __str__(self):
        return f"{self.name}: {self.value}/{self.max_value}"

    # returns all 30 days of meter levels at end of game
    def get_history(self):
        return self.history
    
    def get_value(self):
        return self.value
    
    def set_value(self, change):
        if change > 0:
            self.increase(change)
        else:
            self.decrease(-change)
    
    # output warning when meter level is too low
    def level_warning(self):
        if self.value < .2 * self.max_value:
            print(f"Warning: {self.name} is low!")

    