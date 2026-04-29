from src.models.food import Food
from src.models.model import Model


class FoodMenu(Food, Model):
    def __init__(self, quantity, name, macros=None):
        super().__init__(name, macros or [])
        self.quantity = quantity
