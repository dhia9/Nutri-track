from src.models.food import Food
from src.models.model import Model


class FoodMenu(Food, Model):
    def __init__(self, quantity, name, macros=None):
        macros_list = list(macros) if macros is not None else []
        super().__init__(name, macros_list)
        self.quantity = quantity
