
from food_menu import FoodMenu
class Menu:
    def __init__(self,id,date):
        self.id= id
        self.date = date
        self.content = []

    def add_food_menu(self, food,quantity):
        self.content.append(FoodMenu(food, quantity))