

from food import Food
class FoodMenu(Food):
    def __init__(self, quantity, name):
        super().__init__(name)
        self.quantity = quantity