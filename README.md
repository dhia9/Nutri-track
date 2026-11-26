<p align="center">
  <h1 align="center">Nutritrack</h1>
  <p align="center">
    Application de suivi nutritonnel.<br /> NutriTrack est un projet de développement d'une application de suivi nutritionnel, réalisé dans le cadre du module ISN4.
    <br />
    <a href="https://gitlab.insa-lyon.fr/melhamdeou/nutritrack">GitLab</a>
    ·
    <a href="Architecture.md">Architecture</a>
    ·
    <a href="RAPPORT_EVALUATION.md">Rapport</a>
    ·
    <a href="[RAPPORT_EVALUATION.md](https://github.com/user-attachments/assets/3470ed3e-adeb-4116-8b9c-839076bf0d3c)">Demo</a>
   
  </p>
</p>

----

NutriTrack est une application desktop développée en Python, permettant à chaque utilisateur de :

- Saisir et suivre ses apports nutritionnels quotidiens
- Définir des objectifs physiques personnalisés (prise de masse, perte de poids, maintien)
- Visualiser des statistiques sur son hygiène de vie
- Recevoir des recommandations alimentaires pour atteindre ses macros-cibles
- Être alerté en cas de dépassement de seuils critiques (sel, sucre, lipides saturés, etc.)

## Installation

Cloner le repo git et se placer dans le dossier du projet.

```shell
git clone https://gitlab.insa-lyon.fr/melhamdeou/nutritrack # fonctionne uniquement sur le BV ou via le VPN de l'INSA
cd nutritrack
```

### Avec pip (fonctionne sur le BV)

```shell
python3 -m venv venv
source venv/bin/activate # Pour Linux, sur Windows : venv\Scripts\activate
pip install -r REQUIREMENTS.txt
python3 main.pyw # lancer l'application
```

### Avec uv

```shell
uv venv
source .venv/bin/activate # Pour Linux, sur Windows : .\venv\Scripts\activate
uv add -r REQUIREMENTS.txt
uv run main.pyw # lancer l'application
```

## Profil de démonstration

Pour ajouter un profil de demonstration, lancer le programme python ```add_exemple.py```.
Cela ajoutera un profil "Demonstration" (si un profil du même nom n'existe pas).
Ce profil comprend des données sur 7 jours (du 08/06/2026 au 14/06/2026) notamment :

- des plats consommés
- des plats favoris
- des mesures corporelles

Cela permet de mettre à jours les différentes courbes de la partie Statistique et de rendre plus sûr la suggestion des menus.

(Le fichier ```./src/assets/examples/profile_example.json``` a été généré par IA (claude IA) en se basant sur le fichier ```data.json``` pour les données des aliments et sur le fichier ```settings.json``` pour la structure du fichier)

## Base de données

Les données sont issues du site [ciqual.anses.fr](https://ciqual.anses.fr/), qui fournit une base de données complète
sur la composition nutritionnelle des aliments. Cette base de données est intégrée dans l'application pour permettre aux
utilisateurs de rechercher et d'ajouter facilement des aliments à leur suivi nutritionnel. Les données sont stockées au
format JSON dans le dossier `src/data/data.json` et sont chargées en mémoire au démarrage de l'application.
Afin d'éviter de surcharger l'application et l'IHM, nous avons implémenté une pagination pour l'affichage des aliments,
limitant le nombre d'aliments affichés à 20 par page. Nous avons également fait un nettoyage manuel pour supprimer les
aliments redondants ou peu pertinents (ex : "eau du robinet", "lait en poudre", etc.), afin d'améliorer l'expérience
utilisateur et la pertinence des suggestions de menus.

## Dépendances

- `customtkinter` : pour l'interface graphique
- `Pillow` : pour la manipulation d'images
- `matplotlib` : pour les graphiques statistiques
- `numpy` : pour les calculs numériques
- `python-dateutil` : pour la gestion des dates
- `black` : pour le formatage du code
- `appdirs` : pour la gestion des chemins de fichiers spécifiques à l'application
- `platformdirs` : pour la création de répertoires de manière multiplateforme

## Organisation du code

Voir [Architecture.md](Architecture.md) pour une description détaillée de l'architecture logicielle, des classes et de
leurs interactions.

```
NUTRITRACK/
│
├── src/                            # Code source de l'application
│   ├── views/                      # UI (CustomTkinter)
│   ├── controllers/                # Orchestration / événements
│   ├── models/                     # Domaine
│   ├── data/                       # Accès aux données
│   ├── utils/                      # Fonctions utilitaires (ex: serialisation JSON)
│   └── assets/                     # Ressources statiques
│       └── images/
├── venv/
├── main.py                         # Point d'entrée de l'application
├── tests.py                        # Permet de lancer tous les tests unitaires
├── .gitignore
├── cahier-des-charges.md
├── Architecture.md                 
├── README.md
└── REQUIREMENTS.txt                # Dépendances du projet
```

# Fonctionnalités

## Page d'accueil

La page d'accueil permet de créer un profil utilisateur ou de se connecter à un profil existant en renseignant les
champs nécessaires.

## Page de suivi nutritionnel

- Affiche les apports nutritionnels du jour, avec une répartition par repas.
- Permet d'ajouter des aliments à chaque repas, en recherchant dans la base de données.
- Permet de visualiser les macros consommés et restants pour la journée.
- Permet de générer un menu recommandé pour le repas en cours, en fonction des besoins nutritionnels restants.
- Permet de marquer des menus comme favoris pour une utilisation future.
- Permet de supprimer des aliments ou des repas entiers.
- Affiche un historique des repas consommés, avec la possibilité de consulter les détails de chaque repas.

## Page statistiques

- Affiche des graphiques sur les apports nutritionnels sur une période donnée (semaine, mois).
- Permet de visualiser la répartition des macros sur une période donnée.
- Permet de saisir des mesures corporelles (poids, tour de taille, etc.) et de suivre leur évolution.

## Page paramètres

- Permet de modifier les informations du profil (poids, taille, âge, objectif).
- Permet de choisir un thème d'affichage (clair/sombre).
- Permet de supprimer le profil.

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

Les coefficients sont choisis pour pondérer davantage les calories et les protéines, qui sont souvent les macros les
plus critiques à ajuster.

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

- L'algorithme est **glouton** : il ne revient jamais sur un choix, ce qui peut produire des repas sous-optimaux si les
  aliments disponibles sont peu nombreux.
- Suggestions de menus : L'algorithme de suggestion propose parfois des aliments non pertinents (ex : lait en poudre,
  menthe). Il faudrait mieux prendre en compte le type de chaque aliment pour avoir de meilleures recommandations.

# Crédits

## Auteurs

- Yanis Belaid <yanis.belaid@insa-lyon.fr>
- Marouan El-Hamdeoui <marouan.el-hamdeoui@insa-lyon.fr>
- Nolan Mahadali <nolan.mahadali@insa-lyon.fr>
- Léo Peyronnet <leo.peyronnet@insa-lyon.fr>
- Dhia Somai <dhia.somai@insa-lyon.fr>

## Participation

| Auteur  | Rôle                                                                                                                                                                                                                                                                                                                     | Pourcentage |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Léo     | Chef de projet, architecture globale, sérialisation, algorithme de recommendation des menus, gestion de projet, intégration, tests unitaires, documentation. Contrôle qualité et revue des merge requests.                                                                                                               | 20%         |
| Nolan   | Gestion de la base de données, implémentation des modèles, mesures corporelles, page statistiques, page paramètres, système de thème et de personnalisation, controlleurs.                                                                                                                                               | 20%         |
| Dhia    | Implémentation de la logique métier (calcul des apports, implémentation des modèles, détection de dépassement, recommandations), gestion des profils, gestion des données utilisateur, tests, page statistiques, stats_controller, IHM suggestion de  menus (fenêtre secondaire suggestedMenus et nutrition_controller). | 20%         |
| Yanis   | Implémentation de la logique métier, page nutrition, page d'accueil, système de pagination, optimisations, création de l'interface utilisateur, fenêtres secondaires (ajout d'aliments, controlleur menus favoris, etc.).                                                                                                | 20%         |
| Marouan | Réalisation de Main, Home et Nutrition Controller. Developpement Tkinter de CTKMessageBox. Ajout des fenetres secondaire lié à Nutrition Page (food_quantity.py, fav_win.py) et ajout du Logo (conceptionné par Gemini IA).                                                                                              | 20%         | 

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
