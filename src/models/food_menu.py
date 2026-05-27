from src.models.food import Food
from src.models.model import Model


class FoodMenu(Food, Model):
    def __init__(self, quantity, name, macros=None):
        """Initialise un aliment avec sa quantité et ses macros.

        Args:
            quantity: Quantité de l'aliment en grammes.
            name: Nom de l'aliment.
            macros: Liste des macros de l'aliment (optionnel).
        """
        macros_list = list(macros) if macros is not None else []
        super().__init__(name, macros_list)
        self.quantity = quantity
