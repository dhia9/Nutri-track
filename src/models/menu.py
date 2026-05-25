from src.models.food_menu import FoodMenu
from src.models.model import Model


class Menu(Model):
    def __init__(self, date):
        self.date = date
        self.content = []

    def add_food_menu(self, food, quantity):
        self.content.append(FoodMenu(quantity, food.name, food.macros))

    def has_same_composition(self, other):
        """Vérifie si deux menus ont la même composition (aliments + quantités)"""
        if not isinstance(other, Menu):
            return False
        # Comparer le nombre d'aliments
        if len(self.content) != len(other.content):
            return False
        # Créer des ensembles de (nom, quantité) pour chaque menu
        self_foods = {(f.name, f.quantity) for f in self.content}
        other_foods = {(f.name, f.quantity) for f in other.content}
        return self_foods == other_foods

    def __eq__(self, other):
        """Compare les menus par leur date complète (pour l'unicité)"""
        if not isinstance(other, Menu):
            return False
        return self.date == other.date

    def __hash__(self):
        """Hash basé sur la date complète pour utilisation dans les sets"""
        return hash(self.date)
