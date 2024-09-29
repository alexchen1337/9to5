class Meter:
    def __init__(self, name, max_value, min_value=0):
        self.name = name
        self.value = max_value
        self.max_value = max_value
        self.min_value = min_value

    def increase(self, amount):
        self.value = min(self.max_value, self.value + amount)

    def decrease(self, amount):
        self.value = max(self.min_value, self.value - amount)

    def is_depleted(self):
        return self.value <= self.min_value

    def __str__(self):
        return f"{self.name}: {self.value}/{self.max_value}"
