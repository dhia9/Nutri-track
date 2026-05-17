from src.models.macro import Macro
from src.models.model import Model


class Food(Model):
    def __init__(self, name, macros: list[Macro]):
        self.name = name
        self.macros = macros

    def score(
        self,
        cal_left: float,
        prot_left: float,
        fat_left: float,
        carb_left: float,
        portion_g: float,
    ) -> float:
        """Score de compatibilité entre cet aliment et les macros restantes.
        Moyenne sur toutes les entrées de macros (référence 100g chacune)."""
        n = len(self.macros)
        avg_calorie = sum(m.calorie for m in self.macros) / n
        avg_proteine = sum(m.proteine for m in self.macros) / n
        avg_fat = sum(m.fat for m in self.macros) / n
        avg_carbohydrate = sum(m.carbohydrate for m in self.macros) / n

        if avg_calorie == 0:
            return 0.0

        ratio = portion_g / 100

        def rel_gap(provided: float, target: float) -> float:
            if target <= 0:
                return 0.0
            r = (provided * ratio) / target
            return 1 - abs(1 - min(r, 2))

        return max(
            0.0,
            0.35 * rel_gap(avg_calorie, cal_left)
            + 0.35 * rel_gap(avg_proteine, prot_left)
            + 0.15 * rel_gap(avg_fat, fat_left)
            + 0.15 * rel_gap(avg_carbohydrate, carb_left),
        )
