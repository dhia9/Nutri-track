from macro import Macro

class Food() :
    def __init__(self, name, macros : Macro) :
        self.name = name
        self.macros = macros