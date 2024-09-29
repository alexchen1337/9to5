import pygame

class Store():

    def __init__(self):
        
        # items available for sale : price
        self.items = {
            'Greek Yogurt'    : 5,
            'Vegetable Juice' : 10, 
            'Salad'           : 15,
            'Chicken & Rice'  : 20,

            'Flowers' : 5,
            'Superhero Toy' : 10,
            "Children's Bike" : 15,
            'Jewelry' : 20,

            'Tea' : 5,
            'Coffee' : 10,
            'Caffenine Pills' : 15,
            'Crushed-up White Substance' : 20
            }
        
    def buy_item(self, player, meter, item_name):
        if item_name in self.items:
            price = self.items[item_name]
            if meter.savings_account >= price:
                meter.decrease(price)
                #if we have an inventory do this else write function to apply effect
                player.add_to_inverntoy(item_name)
                print(f"{player} bought {item_name} for {price}.")
            else:
                print(f"Not enough money to buy {item_name}.")
        else:
            print(f"{item_name} is not available in the store.")