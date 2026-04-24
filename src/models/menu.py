from food_menu import FoodMenu


class Menu:
    def __init__(self, id, date):
        self.id = id
        self.date = date
        self.content = []

    def add_food_menu(self, food_menu, quantity):
        self.content.append(food_menu(quantity))
