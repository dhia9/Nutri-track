from src.models.food_menu import FoodMenu
from src.models.model import Model


class Menu(Model):
    def __init__(self, date):
        self.date = date
        self.content = []

    def add_food_menu(self, food, quantity):
        self.content.append(FoodMenu(quantity, food.name, food.macros))
