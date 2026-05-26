import json
import os

import appdirs
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile
from src.utils.json_serializable import JsonSerializable

SETTINGS_PATH = os.path.join(appdirs.user_data_dir("Nutritrack"), "settings.json")


class Settings(JsonSerializable):
    # Mapping des thèmes aux couleurs d'accentuation
    THEME_COLORS_MAP = {
        'green': '#2DBA7F',
        'blue': '#3B82F6',
        'red': '#EF4444',
        'yellow': '#F59E0B',
        'pink': '#EC4899',
    }

    def __init__(self):
        self.profiles = []
        self.appearance_mode = "dark"  # Mode d'apparence (dark/light)
        self.theme_name = "green"  # Nom du thème (couleur)
        
        os.makedirs(appdirs.user_data_dir("Nutritrack"), exist_ok=True)
        # Initialiser le dictionnaire des couleurs du thème
        self.theme_colors = {
            'primary_accent': self.THEME_COLORS_MAP[self.theme_name],  # Vert principal par défaut
            'bg': '#121212',
            'sidebar': '#1D1F21',
            'content': '#17191B',
            'button': '#2A2D30',
            'button_hover': '#35393D',
            'text': '#F1F1F1',
            'text_secondary': '#A8AFB6',
            'frame': '#35393D',
            'frame_dark': '#2A2A4A',
            'frame_darker': '#1A1A2E',
            'error': '#D9534F',
            'error_hover': '#C9302C',
        }
        # créer le fichier settings.json s'il n'existe pas déjà
        if not os.path.isfile(SETTINGS_PATH):
            self.serialize(
                SETTINGS_PATH
            )  # Créer un fichier JSON vide avec les données initiales

        self.favorites_menus: set[Menu] = set()  # Set pour stocker les menus favoris

    def set_theme_color(self, theme_name: str):
        """Met à jour la couleur d'accentuation du thème"""
        if theme_name in self.THEME_COLORS_MAP:
            self.theme_name = theme_name
            self.theme_colors['primary_accent'] = self.THEME_COLORS_MAP[theme_name]
            self.serialize(SETTINGS_PATH)

    def set_appearance_mode(self, mode: str):
        """Met à jour le mode d'apparence (dark/light)"""
        if mode in ['dark', 'light']:
            self.appearance_mode = mode
            self.serialize(SETTINGS_PATH)

    def create_profile(self, name, age, height, weight, sex, target_weight):

        new_profile = Profile(name, age, height, weight, sex, target_weight)
        self.profiles.append(new_profile)

        self.serialize(SETTINGS_PATH)  # Sauvegarder le profil après sa création

    def update_profile(self, profile, name, age, height, weight, sex, target_weight):
        profile.name = name
        profile.age = age
        profile.height = height
        profile.weight = weight
        profile.sex = sex
        profile.target_weight = target_weight

        self.serialize(SETTINGS_PATH)

    def delete_profile(self, name):
        for profile in self.profiles:
            if profile.name == name:
                self.profiles.remove(profile)

        self.serialize(SETTINGS_PATH)

    # charger le dico Settings stocké dans le fichier
    def deserialize(self, path):
        try:
            # Lire le fichier json
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Charger les préférences d'apparence et de thème s'ils existent
            if "appearance_mode" in data:
                self.appearance_mode = data["appearance_mode"]
            if "theme_name" in data:
                self.theme_name = data["theme_name"]
                # Mettre à jour la couleur d'accentuation en fonction du thème
                if self.theme_name in self.THEME_COLORS_MAP:
                    self.theme_colors['primary_accent'] = self.THEME_COLORS_MAP[self.theme_name]

            # Pour chaque profil
            for data_profile in data["profiles"]:
                # Extraire les propriétés du profil
                profile = Profile(
                    data_profile["name"],
                    data_profile["age"],
                    data_profile["height"],
                    data_profile["weight"],
                    data_profile["sex"],
                    data_profile["target_weight"],
                )

                # Récupérer les menus. On commence par chercher dans la liste
                for data_menu in data_profile["eating_habits"]:
                    # Initialiser un objet Menu avec ses attributs
                    menu = Menu(data_menu["date"])

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

            # Charger les menus favoris s'ils existent dans le JSON
            if "favorites_menus" in data:
                for data_menu in data["favorites_menus"]:
                    # Initialiser un objet Menu avec ses attributs
                    menu = Menu(data_menu["date"])

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

                    # Ajouter le menu au set des menus favoris
                    self.favorites_menus.add(menu)

            # Charger les couleurs du thème s'ils existent dans le JSON
            if "theme_colors" in data:
                self.theme_colors.update(data["theme_colors"])

        except FileNotFoundError:
            # s'il n'y a pas de fichier, réinitialiser les profils à une liste vide
            self.profiles.clear()
            print(f"Le fichier {path} n'existe pas")
