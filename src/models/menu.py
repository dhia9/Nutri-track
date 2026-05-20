from src.models.food_menu import FoodMenu
from src.models.model import Model


class Menu(Model):
    def __init__(self, date):
        self.date = date
        self.content = []

    def add_food_menu(self, food, quantity):
        self.content.append(FoodMenu(quantity, food.name, food.macros))

    def __eq__(self, other):
        """Compare les menus par leur date"""
        if not isinstance(other, Menu):
            return False
        return self.date == other.date

    def __hash__(self):
        """Hash basé sur la date pour utilisation dans les sets"""
        return hash(self.date)
