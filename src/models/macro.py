from src.models.model import Model


class Macro(Model):
    def __init__(
        self,
        masse: float,
        proteine: float,
        calorie: float,
        fat: float,
        carbohydrate: float,
    ):
        if masse < 0:
            raise ValueError("La masse doit être positive")

        self.masse = masse
        facteur = masse / 100

        self.proteine = proteine * facteur
        self.calorie = calorie * facteur
        self.fat = fat * facteur
        self.carbohydrate = carbohydrate * facteur

    def __str__(self):
        return (
            f"Pour {self.masse}g : "
            f"Protéines = {self.proteine}g, "
            f"Calories = {self.calorie}kcal, "
            f"Lipides = {self.fat}g, "
            f"Glucides = {self.carbohydrate}g"
        )
