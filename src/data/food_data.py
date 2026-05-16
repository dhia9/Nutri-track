import json

from src.models.food import Food
from src.models.macro import Macro
from src.utils.json_serializable import JsonSerializable


class FoodData(JsonSerializable):
    def __init__(self, content: list = None):
        if content is None:
            content = []
        self.content = content

    def deserialize(self, path):
        try:
            # Lire les fichiers depuis le JSON
            with open(path, "r", encoding="utf-8") as f:
                data: list = json.load(f)

            # Pour chaque Aliment/plat sotcké dans la BDD
            for data_food in data["content"]:
                # Créer un objet Food avec ses attributs (sans les macros, à extraire)
                food = Food(data_food["name"], [])

                # Extraire les macros de l'aliment/plat
                for data_macro in data_food["macros"]:
                    food.macros.append(
                        Macro(
                            data_macro["masse"],
                            data_macro["proteine"],
                            data_macro["calorie"],
                            data_macro["fat"],
                            data_macro["carbohydrate"],
                        )
                    )

                # Ajouter le plat/aliment à la liste de la base de données en mémoire
                self.content.append(food)
        # Si le fichier n'existe pas
        except FileNotFoundError:
            self.content = []
            print(f"Le fichier {path} n'existe pas")
