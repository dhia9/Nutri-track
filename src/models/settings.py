import json

from src.models.food_menu import FoodMenu
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile
from src.utils.json_serializable import JsonSerializable


class Settings(JsonSerializable):
    def __init__(self):
        self.profiles = []

    def create_profile(self, name, age, height, weight, sex, target_weight):
        new_profile = Profile(name, age, weight, height, sex, target_weight)
        self.profiles.append(new_profile)

    # charger le dico Settings stocké dans le fichier
    def deserialize(self, path):
        try:
            # Lire le fichier json
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Pour chaque profil
            for data_profile in data["profiles"]:
                # Extraire les propriétés du profil
                profile = Profile(
                    data_profile["name"],
                    data_profile["age"],
                    data_profile["weight"],
                    data_profile["height"],
                    data_profile["sex"],
                    data_profile["target_weight"],
                )

                # Récupérer les menus. On commence par chercher dans la liste
                for data_menu in data_profile["eating_habits"]:
                    # Initialiser un objet Menu avec ses attributs
                    menu = Menu(data_menu["id"], data_menu["date"])

                    # Peupler le contenu du Menu par extraction des informations dans la liste content
                    for data_food in data_menu["content"]:
                        # Création d'un plat/aliment avec ses attributs
                        food = FoodMenu(data_food["quantity"], data_food["name"])

                        # Extraire les macros / propriétés du plat en parcourant la liste
                        for data_macro in data_food["macros"]:
                            # Ajouter le Macro à la liste des macros
                            food.macros.append(
                                Macro(
                                    data_macro["masse"],
                                    data_macro["proteine"],
                                    data_macro["calorie"],
                                    data_macro["fat"],
                                    data_macro["carbohydrate"],
                                )
                            )
                        # Ajouter le plat / aliment au menu
                        menu.content.append(food)

                    # Ajouter le menu à la liste des habitudes alimentaires du profil
                    profile.eating_habits.append(menu)

                # Ajouter le profil à la liste des profils
                self.profiles.append(profile)

        except FileNotFoundError:
            # s'il n'y a pas de fichier, réinitialiser les profils à une liste vide
            self.profiles.clear()
            print(f"Le fichier {path} n'existe pas")
