from src.models.model import Model


class Profile(Model):
    def __init__(self, name, age, height, weight, sex, target_weight):
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
