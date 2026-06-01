from src.models.food_menu import FoodMenu
from src.models.model import Model


class Menu(Model):
    def __init__(self, date):
        self.date = date
        self.content = []

    def add_food_menu(self, food, quantity):
        """Ajoute un aliment avec sa quantité au menu.

        Args:
            food: L'objet Food à ajouter.
            quantity: La quantité en grammes.
        """
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
        """Compare les menus par leur date.

        Args:
            other: L'autre objet à comparer.

        Returns:
            True si les menus ont la même date, False sinon.
        """
        if not isinstance(other, Menu):
            return False
        return self.date == other.date

    def __hash__(self):
        """Hash basé sur la date pour utilisation dans les sets.

        Returns:
            Un hash basé sur la date du menu.
        """
        return hash(self.date)
