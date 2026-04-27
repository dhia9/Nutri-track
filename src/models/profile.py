from menu import Menu


class Profile:
    def __init__(self, name, age, weight, height, sex, target_weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.sex = sex
        self.target_weight = target_weight
        self.eating_habits = []

    def get_imc(self):
        if self.height > 0:
            return self.weight / (self.height**2)
        else:
            return 0
