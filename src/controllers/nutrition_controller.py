import src.controllers.main_controller as main_controller
import src.data.food_data as food_data


class NutritionController:
    def __init__(self, main_controller : main_controller.MainController):
        self.main_controller = main_controller
        self.view = None  # La view sera assignée par la view elle-même
        self.current_profile = self.main_controller.current_profile
        self.food_data = food_data.FoodData()  # Initialiser la base de données en mémoire
        self.food_data.deserialize("src/data/data.json")  # Charger les données depuis le fichier JSON  
        
    def fill_food_list(self, food_list): # Remplir la liste des aliments selon le fichier JSON 
        for food in self.food_data.content:
            food_list.append(food.name)

    def search_foods(self, query: str):
        """Filtre les aliments selon la query de recherche (insensible à la casse)"""
        query = query.strip().lower()
        
        # Si la query est vide, afficher tous les aliments
        if not query:
            for food_name, food_data in self.view.food_items.items():
                food_data["checkbox"].pack(side="left", padx=10, pady=10, fill="x", expand=True)
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            return
        
        # Filtrer et afficher seulement les aliments qui correspondent
        for food_name, food_data in self.view.food_items.items():
            if query in food_name.lower():
                # Afficher l'aliment
                food_data["checkbox"].pack(side="left", padx=10, pady=10, fill="x", expand=True)
                food_data["frame"].pack(fill="x", padx=5, pady=5)
            else:
                # Cacher l'aliment
                food_data["frame"].pack_forget()

    def add_food(self):
        pass

