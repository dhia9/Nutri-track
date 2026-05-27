import sys
from datetime import date
from src.data.food_data import FoodData
from src.models.food import Food
from src.models.macro import Macro
from src.models.menu import Menu
from src.models.profile import Profile
from src.models.macro_type import MacroType
passed = 0
failed = 0


def ok(label: str):
    global passed
    passed += 1
    print(f"  ✓ {label}")


def fail(label: str, detail: str = ""):
    global failed
    failed += 1
    msg = f"  ✗ {label}"
    if detail:
        msg += f"\n      → {detail}"
    print(msg)


def assert_approx(val, expected, label: str, tol=0.5):
    if abs(val - expected) <= tol:
        ok(label)
    else:
        fail(label, f"obtenu {val:.4f}, attendu {expected:.4f} (tolérance ±{tol})")


def section(title: str):
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}")

# SECTION 1 — MacroType

section("1. MacroType — unicité et valeurs")

print("\n  Vérifie que l'énumération MacroType contient bien les 4 types")
print("  attendus et que chaque valeur est distincte.\n")
membres = list(MacroType)
if len(membres) == 4:
    ok("MacroType contient exactement 4 membres")
else:
    fail("MacroType devrait contenir 4 membres", f"trouvé : {len(membres)}")

valeurs = [m.value for m in membres]
if len(valeurs) == len(set(valeurs)):
    #verifer en supprimant les doublans
    ok("Toutes les valeurs de MacroType sont distinctes")
else:
    fail("Des valeurs de MacroType sont dupliquées", str(valeurs))

noms_attendus = {"CALORIE", "PROTEIN", "FAT", "CARBOHYDRATE"}
noms_reels = {m.name for m in membres}
if noms_reels == noms_attendus:
    ok("Les noms des membres correspondent exactement aux 4 macronutriments")
else:
    fail("Noms inattendus dans MacroType", f"trouvé : {noms_reels}")


# ─────────────────────────────────────────────
# Résumé final
# ─────────────────────────────────────────────

print(f"\n{'═'*55}")
print(f"  Résultats : {passed} ✓ réussi(s)  |  {failed} ✗ échoué(s)")
print(f"{'═'*55}\n")

if failed > 0:
    sys.exit(1)