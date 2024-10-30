import networkx as nx

class RelationshipGraph:
    def __init__(self):
        # Initialize directed weighted graph
        self.graph = nx.DiGraph()
        
        # Add nodes (entities in the game)
        self.graph.add_node("player")
        self.graph.add_node("wife")
        self.graph.add_node("coworker")
        self.graph.add_node("boss")
        
        # Add edges with initial weights
        self.graph.add_edge("player", "wife", weight=70)
        self.graph.add_edge("player", "coworker", weight=60)
        self.graph.add_edge("player", "boss", weight=80)
        self.graph.add_edge("wife", "coworker", weight=50)
        self.graph.add_edge("boss", "coworker", weight=50)
        self.graph.add_edge("boss", "player", weight=80)

    def get_relationship(self, source, target):
        return self.graph[source][target]["weight"]

    def set_relationship(self, source, target, weight):
        # Sets a new weight while ensuring it remains between 0 and 100
        self.graph[source][target]["weight"] = max(0, min(100, weight))

    def increase_relationship(self, source, target, amount):
        # Increase relationship weight
        current_weight = self.get_relationship(source, target)
        self.set_relationship(source, target, current_weight + amount)
        print(f"{source}'s relationship with {target} improved to {self.get_relationship(source, target)}")

    def decrease_relationship(self, source, target, amount):
        # Decrease relationship weight
        current_weight = self.get_relationship(source, target)
        self.set_relationship(source, target, current_weight - amount)
        print(f"{source}'s relationship with {target} worsened to {self.get_relationship(source, target)}")

    def check_thresholds(self):
        # Check if weights are below thresholds and trigger consequences
        if self.get_relationship("player", "boss") < 30:
            print("Consequence: Boss is unhappy with your performance!")
        if self.get_relationship("player", "wife") < 30:
            print("Consequence: Your relationship with your wife is strained!")
        if self.get_relationship("player", "coworker") < 30:
            print("Consequence: Your coworker is avoiding you!")
            
    def __str__(self):
        return nx.info(self.graph)