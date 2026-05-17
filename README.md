# Nutritrack

NutriTrack est une application desktop développée en Python, permettant à chaque utilisateur de :

- Saisir et suivre ses apports nutritionnels quotidiens
- Définir des objectifs physiques personnalisés (prise de masse, perte de poids, maintien)
- Visualiser des statistiques sur son hygiène de vie
- Recevoir des recommandations alimentaires pour atteindre ses macros-cibles
- Être alerté en cas de dépassement de seuils critiques (sel, sucre, lipides saturés, etc.)

## Installation

```
py -m venv venv
venv\Scripts\activate # Pour Windows, sur Linux/Mac : source venv/bin/activate
pip install -r requirements.txt
```

## Base de données

Les données sont issues du site [ciqual.anses.fr](https://ciqual.anses.fr/), qui fournit une base de données complète
sur la composition nutritionnelle des aliments. Cette base de données est intégrée dans l'application pour permettre aux
utilisateurs de rechercher et d'ajouter facilement des aliments à leur suivi nutritionnel.

# Algorithme de génération de menu

## Vue d'ensemble

L'algorithme génère **un seul repas** adapté à la journée en cours. Il tient compte des repas déjà enregistrés et
répartit équitablement les macros restantes sur les repas futurs.

---

## Pipeline

```
Besoins journaliers (Mifflin-St Jeor + NAP)
        │
        ├── Macros déjà consommées aujourd'hui  (eating_habits)
        │
        └── Macros restantes ÷ repas restants
                        │
                        └── Sélection gloutonne → 1 Menu
```

---

## Étapes détaillées

### 1. Calcul des besoins journaliers (`get_nutritional_needs`)

Formule de **Mifflin-St Jeor** pour le métabolisme de base, multiplié par le facteur d'activité NAP. L'objectif (perte /
maintien / masse) est déduit automatiquement en comparant `weight` et `target_weight`, et ajuste les calories cibles (
−400 / 0 / +300 kcal).

### 2. Budget du repas (`get_meal_budget`)

```
budget_repas = (besoins_jour - déjà_consommé) / repas_restants
```

`repas_restants = meals_per_day − nombre de menus enregistrés aujourd'hui`

Chaque macro (calories, protéines, lipides, glucides) est traitée indépendamment. Le budget ne peut pas être négatif.

### 3. Sélection des aliments (`pick_best_food`)

Pour chaque aliment disponible, on calcule un **score de compatibilité** avec le budget restant :

```
score = 0.35 * écart_calories
      + 0.35 * écart_protéines
      + 0.15 * écart_lipides
      + 0.15 * écart_glucides
      + bruit,  valeur aléatoire (faible) : évite des menus identiques
```

L'écart est calculé comme `1 − |1 − ratio|`, où `ratio = apport / cible` (plafonné à 2). Un aliment déjà utilisé dans la
journée ou dans le repas est exclu.

### 4. Calcul de la portion (`compute_portion`)

La portion est fixée à **150g par défaut**, puis réduite si nécessaire pour ne pas dépasser le budget calorique restant.
Elle ne descend jamais sous **30g**.

```
portion = clamp(budget_cal / cal_par_g, 30g, 150g)
```

Le `Macro` résultant est instancié avec les valeurs **pour 100g** - la classe `Macro` gère le scaling en interne via
`masse / 100`.

### 5. Itération (`generate_menu`)

On répète les étapes 3-4 jusqu'à **4 aliments** ou jusqu'à ce que le budget calorique restant passe sous **50 kcal**.

---

## Paramètres

| Paramètre            | Rôle                                   | Valeur par défaut |
|----------------------|----------------------------------------|-------------------|
| `nap`                | Facteur d'activité physique            | `1.55`            |
| `meals_per_day`      | Nombre de repas prévus dans la journée | `3`               |
| `BASE_PORTION_G`     | Portion de base par aliment            | `150g`            |
| `MAX_ITEMS_PER_MEAL` | Nombre max d'aliments par repas        | `4`               |

---

## Limites connues

- La répartition entre repas est uniforme, sans pondération matin/midi/soir.
- L'algorithme est **glouton** : il ne revient jamais sur un choix, ce qui peut produire des repas sous-optimaux si les
  aliments disponibles sont peu nombreux.
