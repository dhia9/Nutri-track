from profile import Profile

class Settings:
    def __init__(self):
        self.profiles = []

    
    def create_profile(self):
        new_profile = Profile()
        self.profiles.append(new_profile)