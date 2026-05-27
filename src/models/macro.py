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
        """Initialise un macro nutriment avec ses valeurs.
        
        Les valeurs sont échellées en fonction de la masse (référence 100g).
        
        Args:
            masse: Masse en grammes.
            proteine: Protéines en grammes (pour 100g).
            calorie: Calories en kcal (pour 100g).
            fat: Lipides en grammes (pour 100g).
            carbohydrate: Glucides en grammes (pour 100g).
            
        Raises:
            ValueError: Si la masse est négative.
        """
        if masse < 0:
            raise ValueError("La masse doit être positive")

        self.masse = masse
        facteur = masse / 100

        self.proteine = proteine * facteur
        self.calorie = calorie * facteur
        self.fat = fat * facteur
        self.carbohydrate = carbohydrate * facteur

    def __str__(self):
        """Représentation textuelle du macro nutriment.
        
        Returns:
            Chaîne de caractères décrivant les valeurs du macro.
        """
        return (
            f"Pour {self.masse}g : "
            f"Protéines = {self.proteine}g, "
            f"Calories = {self.calorie}kcal, "
            f"Lipides = {self.fat}g, "
            f"Glucides = {self.carbohydrate}g"
        )
