import src.controllers.main_controller as main_controller
import src.data.food_data as food_data
import src.views.food_quantity as food_quantity
import src.models.menu as menu
import src.models.food_menu as foodMenu
from datetime import datetime
import appdirs


class NutritionController:
    def __init__(self, main_controller: main_controller.MainController):
        self.main_controller = main_controller
        self.view = None  # La view sera assignée par la view elle-même
        self.current_profile = self.main_controller.current_profile
        self.food_data = (
            food_data.FoodData()
        )  # Initialiser la base de données en mémoire
        self.food_data.deserialize(
            "src/data/data.json"
        )  # Charger les données depuis le fichier JSON

    def fill_food_list(
        self, food_list
    ):  # Remplir la liste des aliments selon le fichier JSON
        for food in self.food_data.content:
            food_list.append(food.name)

    def search_foods(self, query: str):
        """Filtre les aliments selon la query de recherche (insensible à la casse)"""
        query = query.strip().lower()

        # Si la query est vide, afficher tous les aliments
        if not query:
            for food_name, food_data in self.view.food_items.items():
                food_data["checkbox"].pack(
                    side="left", padx=10, pady=10, fill="x", expand=True
                )
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            return

        # Filtrer et afficher seulement les aliments qui correspondent
        for food_name, food_data in self.view.food_items.items():
            if query in food_name.lower():
                # Afficher l'aliment
                food_data["checkbox"].pack(
                    side="left", padx=10, pady=10, fill="x", expand=True
                )
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            else:
                # Cacher l'aliment
                food_data["frame"].pack_forget()

    def food_by_name(self, name):
        """Retourne un objet Food de la base de données selon son nom"""
        for food in self.food_data.content:
            if food.name == name:
                return food
        return None  # Si aucun aliment ne correspond au nom donné

    def add_menu(self):
        """Ouvre une nouvelle fenêtre pour ajouter un aliment avec sa quantité et l'ajoute à la liste de l'utilisateur une fois validé"""
        selected_foods = [
            food_name
            for food_name, data in self.view.food_items.items()
            if data["var"].get() == "on"
        ]

        if not selected_foods:
            return  # Aucun aliment sélectionné, ne rien faire

        # Ouvrir la fenêtre de quantités
        quantity_window = food_quantity.FoodQuantity(selected_foods)
        quantity_window.wait_window()  # Attendre que la fenêtre soit fermée
        quantities = quantity_window.quantities  # Récupérer les quantités saisies
        a_menu = menu.Menu(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )  # reformater la date pour le traitement des données avec .strptime lors de la désérialisation du JSON (pour la partie stat notamment)

        for food_name, quantity in quantities.items():
            food = self.food_by_name(food_name)
            if food:
                a_menu.add_food_menu(
                    food=food,
                    quantity=quantity,
                )

        self.current_profile.eating_habits.append(a_menu)
        self.main_controller.settings.serialize(
            appdirs.user_data_dir("Nutritrack") + "/settings.json"
        )  # Sauvegarder les données après l'ajout du menu
