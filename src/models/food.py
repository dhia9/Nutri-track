from src.models.macro import Macro
from src.models.model import Model


class Food(Model):
    def __init__(self, name, macros: list[Macro]):
        self.name = name
        self.macros = macros
