from macro_type import Macro_type

class Macro() :
    def __init__(self, type : Macro_type, masse : float) :
        self.macrotype = type
        self.masse = masse

        if masse < 0 :
            raise ValueError("La masse doit être positive")

    def __str__(self) :
        return f"Il y a l'aliment = {self.macrotype}, qui pèse = {self.masse} grammes"
    


    

    