# This is the store class that allows the player to buy
# items to help them in the game

import pygame
from item import Item


class Store():

    def __init__(self):
        
        # items available for sale
        self.items = {
            Item('Greek Yogurt',     5, 'Health',  5),
            Item('Vegetable Juice', 10, 'Health', 10),
            Item('Salad',           15, 'Health', 15),
            Item('Chicken & Rice',  20, 'Health', 20),

            Item('Flowers',          5, 'Family Happiness',  5),
            Item('Superhero Toy',   10, 'Family Happiness', 10),
            Item("Children's Bike", 15, 'Family Happiness', 15),
            Item('Jewelry',         20, 'Family Happiness', 20),

            Item('Tea',                         5, 'Energy',  5),
            Item('Coffee',                     10, 'Energy', 10),
            Item('Caffeine Pills',             15, 'Energy', 15),
            Item('Crushed-up White Substance', 20, 'Energy', 20)
        }
        
    def buy_item(self, player, item_name):
        
        # Check if the item exists
        if item_name not in self.items:
            print(f"Sorry, {item_name} is not available in the store.")
            return
        
        item = self.items[item_name]

        # Check if player has the cash
        if player.money < item.price:
            print(f"Sorry, you don't have enough money.")
            return
        
        # charge the players
        player.money -= item.price

        # use the item
        