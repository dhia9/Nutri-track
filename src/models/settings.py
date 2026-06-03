import json
import os

import appdirs
from src.models.food_menu import FoodMenu
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.mesures_corporelles import MesuresCorporelles
from src.models.profile import Profile
from src.utils.json_serializable import JsonSerializable

SETTINGS_PATH = os.path.join(appdirs.user_data_dir("Nutritrack"), "settings.json")


class Settings(JsonSerializable):
    def __init__(self):
        self.profiles = []
        self.appearance_mode = "dark"  # Mode d'apparence (dark/light)
        self.theme = "#2DBA7F"  # Nom du thème (couleur)
        self.favorites_menus: set[Menu] = set()  # Set pour stocker les menus favoris

        os.makedirs(appdirs.user_data_dir("Nutritrack"), exist_ok=True)#création du dossier si pas déja fait
        # créer le fichier settings.json s'il n'existe pas déjà
        if not os.path.isfile(SETTINGS_PATH):#verification d'existence du fichier
            self.serialize(
                SETTINGS_PATH
            )  # Créer un fichier JSON vide avec les données initiales

    def create_profile(self, name, age, height, weight, sex, target_weight):
        """Crée un nouveau profil et le sauvegarde.

        Args:
            name: Nom du profil.
            age: Âge du profil.
            height: Taille en cm.
            weight: Poids en kg.
            sex: Sexe (Homme/Femme).
            target_weight: Objectif de poids en kg.
        """
        new_profile = Profile(name, age, height, weight, sex, target_weight)
        self.profiles.append(new_profile)

        self.serialize(SETTINGS_PATH)  # Sauvegarder le profil après sa création

    def update_profile(self, profile, name, age, height, weight, sex, target_weight):
        """Met à jour les données d'un profil et les sauvegarde.

        Args:
            profile: Le profil à mettre à jour.
            name: Nouveau nom.
            age: Nouvel âge.
            height: Nouvelle taille en cm.
            weight: Nouveau poids en kg.
            sex: Nouveau sexe.
            target_weight: Nouvel objectif de poids.
        """
        profile.name = name
        profile.age = age
        profile.height = height
        profile.weight = weight
        profile.sex = sex
        profile.target_weight = target_weight

        self.serialize(SETTINGS_PATH)

    def delete_profile(self, name):
        """Supprime un profil par son nom et sauvegarde.

        Args:
            name: Nom du profil à supprimer.
        """
        for profile in self.profiles:
            if profile.name == name:
                self.profiles.remove(profile)

        self.serialize(SETTINGS_PATH)

    # charger le dico Settings stocké dans le fichier
    def deserialize(self, path):
        """Désérialise les données depuis un fichier JSON.

        Charge tous les profils, leurs menus et les menus favoris.

        Args:
            path: Chemin du fichier JSON.
        """
        try:
            # Lire le fichier json
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Charger les préférences d'apparence et de thème s'ils existent
            if "appearance_mode" in data:
                self.appearance_mode = data["appearance_mode"]
            if "theme" in data:
                self.theme = data["theme"]

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

                # Charger les mesures corporelles si elles existent
                if "mesures_corporelles" in data_profile:
                    for data_mesure in data_profile["mesures_corporelles"]:
                        mesure = MesuresCorporelles(
                            data_mesure["date"],
                            data_mesure["poids"],
                            data_mesure["tour_de_taille"],
                            data_mesure["tour_de_bras"],
                            data_mesure["masse_grasse"],
                        )
                        profile.mesures_corporelles.append(mesure)

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

        except FileNotFoundError:
            # s'il n'y a pas de fichier, réinitialiser les profils à une liste vide
            self.profiles.clear()
            print(f"Le fichier {path} n'existe pas")

    def set_theme_color(self, theme: str):
        """Met à jour la couleur d'accentuation du thème"""
        self.theme = theme
        self.serialize(SETTINGS_PATH)

    def set_appearance_mode(self, mode: str):
        """Met à jour le mode d'apparence (dark/light)"""
        if mode in ["dark", "light"]:
            self.appearance_mode = mode
            self.serialize(SETTINGS_PATH)
