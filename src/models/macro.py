from macro_type import Macro_type

class Macro(Macro_type) :
    def __init__(self, masse : float, proteine : float, calorie : float, fat : float, carbohydrate : float) :
        super().__init__(proteine, calorie, fat, carbohydrate)
        self.masse = masse
        self.proteine = self.proteine * (masse / 100)
        self.calorie = self.calorie * (masse / 100)
        self.fat = self.fat * (masse / 100)
        self.carbohydrate = self.carbohydrate * (masse / 100)

    
        if masse < 0 :
            raise ValueError("La masse doit être positive")

    def __str__(self) :
        return f"Il y a l'aliment = {self.macrotype}, qui pèse = {self.masse} grammes"
    




    