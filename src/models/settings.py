from profile import Profile


class Settings:
    def __init__(self):
        self.profiles = []

    def create_profile(self, name, age, height, weight, sex, target_weight):
        new_profile = Profile(name, age, weight, height, sex, target_weight)
        self.profiles.append(new_profile)
