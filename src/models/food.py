from macro import Macro

class Food(Macro) :
    def __init__(self, name, macros : Macro) :
        self.name = name
        self.macros = macros