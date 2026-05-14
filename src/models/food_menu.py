from src.models.food import Food
from src.models.model import Model


class FoodMenu(Food, Model):
    def __init__(self, quantity, name, macros=[]):
        super().__init__(name, macros)
        self.quantity = quantity
