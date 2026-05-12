from datetime import datetime, timedelta
import random

class StatsController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = None
    def get_current_profile(self):
        return self.main_controller.current_profile
    def generate_history(self, days=30):
        history = []
        today = datetime.today()
        for i in range(days):
            date = today - timedelta(days=(days - i))
            history.append({
                "date": date.strftime("%Y-%m-%d"),
                "calories": random.randint(1800, 2600),
                "proteins": random.randint(70, 140),
                "carbs": random.randint(150, 300),
                "fats": random.randint(40, 90),
                "salt": round(random.uniform(3, 9), 1),
                "sugar": round(random.uniform(20, 70), 1),
            })
        return history
