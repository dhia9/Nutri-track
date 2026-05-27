
from src.models.macro import Macro



def print_test(test_name, status):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol} {test_name}{reset}")


def print_section(section_name):
    print(f"\n{'=' * 60}")
    print(f"  {section_name}")
    print(f"{'=' * 60}")


# ============================================================================
# MACRO TESTS
# ============================================================================

def test_macro_masse_negative_raises_error():
    try:
        Macro(-10, 20, 100, 5, 15)
        print_test("test_macro_masse_negative_raises_error", False)
        return False
    except ValueError as e:
        result = "La masse doit être positive" in str(e)
        print_test("test_macro_masse_negative_raises_error", result)
        return result


def test_macro_scaling_affects_all_values():
    try:
        macro_100g = Macro(100, 25, 150, 10, 20)
        macro_50g = Macro(50, 25, 150, 10, 20)

        result = (
            macro_100g.proteine == 25 and
            macro_50g.proteine == 12.5 and
            macro_100g.calorie == 150 and
            macro_50g.calorie == 75 and
            macro_100g.fat == 10 and
            macro_50g.fat == 5 and
            macro_100g.carbohydrate == 20 and
            macro_50g.carbohydrate == 10
        )

        print_test("test_macro_scaling_affects_all_values", result)
        return result

    except Exception:
        print_test("test_macro_scaling_affects_all_values", False)
        return False


def test_macro_zero_masse_creates_zero_values():
    try:
        macro = Macro(0, 25, 150, 10, 20)

        result = (
            macro.proteine == 0 and
            macro.calorie == 0 and
            macro.fat == 0 and
            macro.carbohydrate == 0
        )

        print_test("test_macro_zero_masse_creates_zero_values", result)
        return result

    except Exception:
        print_test("test_macro_zero_masse_creates_zero_values", False)
        return False

