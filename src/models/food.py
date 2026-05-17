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
        """Compatibility score between a food and remaining macro targets."""
        macro = self.macros[0]
        if macro.calorie == 0:
            return 0.0

        ratio = portion_g / macro.masse  # scale to desired portion

        def rel_gap(provided: float, target: float) -> float:
            if target <= 0:
                return 0.0
            r = (provided * ratio) / target
            return 1 - abs(1 - min(r, 2))

        return max(
            0.0,
            0.35 * rel_gap(macro.calorie, cal_left)
            + 0.35 * rel_gap(macro.proteine, prot_left)
            + 0.15 * rel_gap(macro.fat, fat_left)
            + 0.15 * rel_gap(macro.carbohydrate, carb_left),
        )
