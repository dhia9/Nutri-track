<center>

# Rapport de Projet - NutriTrack

**Auteurs :** Yanis Belaid, Marouan El-Hamdeoui, Nolan Mahadali, Léo Peyronnet, Dhia Somai

</center>

## 1. Introduction et Contexte

### 1.1 Présentation du projet

**NutriTrack** est une application proposant un suivi nutritionnel local et simple d'utilisation, permettant à chaque
utilisateur de mieux gérer son alimentation et d'atteindre ses objectifs physiques personnalisés (perte/maintien/prise
de masse).

### 1.2 Cahier des charges

Nous vous invitons à consulter le premier rendu expliquant les différentes fonctionnalités de l'application, les besoins
fonctionnels et non fonctionnels, ainsi que les contraintes techniques.

**Stack technique finale retenue :**

| Composant           | Technologie             | Justification                                                                                                                  |
|---------------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Langage             | Python 3.14             | Langage accessible, riche en bibliothèques scientifiques                                                                       |
| Interface graphique | CustomTkinter + Tkinter | Widgets modernes, natifs, cross-platform                                                                                       |
| Stockage            | JSON                    | Format léger, rapide, lisible, pas besoin de base de données complexe                                                          |
| Visualisation       | Matplotlib              | Libraire standard pour les graphiques statiques en Python                                                                      |
| Base alimentaire    | fichier JSON partagé    | Données statiques à partir de [CIQUAL](https://ciqual.anses.fr/) (récupérer en XLSX et convertie en JSON via l'IA (Claude IA)) |

## 2. Modularité et Architecture

### 2.1 Différences par rapport à l'architecture originale

Nous avons implémenté la plupart des fonctionnalités prévues dans le cahier des charges, mais nous avons dû faire
quelques ajustements par rapport à l'architecture initialement proposée pour mieux répondre aux besoins du projet et
optimiser le développement.

1. Modification de la logique de sérialisation JSON : Création d'une classe Model permettant de convertir en
   dictionnaire n'importe quelle classe héritant de Model
2. La classe JsonSerializer est uniquement utilisée pour la sérialisation ; la logique de désérialisation est gérée
   manuellement dans les classes en ayant besoin.
3. Création d'une classe MesuresCorporelles pour ajouter le suivi de mesures corporelles (poids, tour de taille, etc.)
   et permettre de meilleures statistiques
4. La logique de recommandation de menus est directement intégrée dans la classe Profile afin d'avoir directement toutes
   les informations nécessaires

### 2.2 Fonctionnalités implémentées

- Page d'accueil (sélection/création de profil)
- Page Gestion nutritionnelle (ajout/suppression d'aliments)
- Page Statistiques (graphiques, analyses)
- Page Paramètres (gestion des profils)
- Recherche et auto-complétion d'aliments
- Calcul des apports nutritionnels
- Recommandations alimentaires

## 3. Complexité et Structures de Données

### 3.1 Structures de données utilisées

Nous avons décidé d'utiliser principalement des classes afin de garantir la logique métier le plus possible. Ainsi la
plupart des modèles sont stockés sous forme de classes ayant chacune des attributs et méthodes propres.

Exemple avec la classe `Menu` :

- La classe a des attributs tels que `name`, `foods` (liste d'objets `FoodMenu`), et des méthodes comme
  `has_same_composition()` pour comparer deux menus en utilisant de sets pour plus d'efficacité.
- Cette classe permet de représenter un repas complet, composé de plusieurs aliments, et de gérer la logique métier
  associée (calcul des macros, comparaison, etc.) de manière structurée et cohérente.

Toutes les structures de données possibles sont utilisées un peu partout dans le projet, principalemet des listes pour
stocker les différents menus, profils et macros mais aussi des dictionnaires pour la sérialisation ainsi que des sets
pour accélérer certaines opérations de comparaison.

### 3.2 Complexité algorithmique

Les traitements principaux restent globalement linéaires et adaptés à une application locale. L’analyse suivante est une
estimation basée sur les volumes de données manipulés par l’application.

- **Calcul des apports nutritionnels** : `O(1)` pour un aliment ou un menu déjà connu, car les valeurs sont directement
  lues et combinées à partir des données du modèle ; on passe à `O(n)` lorsqu’il faut additionner les consommations
  d’une journée, chaque entrée étant parcourue une fois.
- **Détection de dépassement** : `O(n)`, car l’algorithme compare les apports cumulés du profil à ses objectifs en
  effectuant d’abord une somme des consommations, puis une vérification macro par macro.
- **Recommandation alimentaire** : `O(F × k)` par sélection, où `F` est le nombre d’aliments dans `food_data.content` et
  `k` le nombre d’entrées `Macro` moyennées pour chaque aliment dans `food.macros`. Dans `pick_best_food()`,
  l’application parcourt toute la base, écarte les aliments déjà utilisés dans le repas ou dans la journée, calcule un
  score de compatibilité via `Food.score()`, puis conserve le meilleur candidat ; comme un repas est limité à
  `MAX_ITEMS_PER_MEAL = 4` aliments, le coût total reste proportionnel à la taille de la base.
- **Sérialisation / désérialisation JSON** : `O(S)`, avec `S` la taille des données enregistrées (
  `S=nombre de profils × nombres de menus × ...`). La sérialisation est
  généralisée par `JsonSerializable.serialize()` et `Model.to_dict()`, qui transforment récursivement les objets en
  dictionnaires compatibles JSON. En revanche, la désérialisation reste manuelle : `Settings.deserialize()` relit le
  fichier avec `json.load()` puis reconstruit explicitement les `Profile`, `Menu`, `FoodMenu`, `Macro` et
  `MesuresCorporelles`.

Ces coûts sont limités notamment par l'usage de `set` et de dictionnaires pour certaines comparaisons.


## 4. Engagement et Implications des Membres

Qui a travaillé sur quelle partie du projet ?

- Léo : Chef de projet, architecture globale, sérialisation, algorithme de recommendation des menus, gestion de
  projet, intégration, tests unitaires,
  documentation. Contrôle qualité et revue des merge requests.
- Nolan : Gestion de la base de données, implémentation des modèles, mesures corporelles, page statistiques, page
  paramètres, système de thème et de personnalisation.
- Dhia : implémentation de la logique métier (calcul des apports, détection de dépassement, recommandations),
  gestion des profils, gestion des données utilisateur, tests, page statistiques, IHM suggestion de menus.
- Yanis : implémentation de la logique métier, page nutrition, système de pagination, optimisations, création de
  l'interface utilisateur.
- Marouan : Réalisation de Main, Home et Nutrition Controller. Developpement Tkinter de CTKMessageBox. Ajout des
  fenetres secondaire lié à Nutrition Page (Food_quantity.py, Fav_Win.py) et ajout du Logo (conceptionné par Gemini
  IA).

## 5. Conclusion

Nous avons réussi à créer une application fonctionnelle répondant
aux besoins définis dans le cahier des charges (et même plus !), tout en respectant les contraintes techniques et
temporelles. Nous sommes fiers du travail accompli et confiants que NutriTrack pourra être un outil utile pour
les utilisateurs souhaitant suivre et améliorer leur alimentation.

---

## Annexes Utilisation de l'IA

Nous avons utilisé l'IA à plusieurs étapes du projet pour accélérer le développement et améliorer la qualité du code :
Nous avons utilisé l'IA pour générer des morceaux de code, notamment pour la logique de
recommandation des menus et les docstrings.

Voici des exemples de prompts que nous avons utilisé :

1. Génération de l'algorithme de recommandation des menus :

```text
Je travaille sur un projet d'ISN (info, python, customtkinter) en 2A à l'INSA Lyon. 

NutriTrack est une application desktop développée en Python, permettant à chaque utilisateur de :
- Saisir et suivre ses apports nutritionnels quotidiens
- Définir des objectifs physiques personnalisés (prise de masse, perte de poids, maintien)
- Visualiser des statistiques sur son hygiène de vie
- Recevoir des recommandations alimentaires pour atteindre ses macros-cibles
- Être alerté en cas de dépassement de seuils critiques (sel, sucre, lipides saturés, etc.)

Je veux que tu me donne dans un premier temps un algorithme ou formule pour calculer les 
besoins nutrionels journalier d'un individu ayant un certain poids, taille, et objectif de poids.
On considère que la masse de référence pour chaque macro vaut toujours 100
J'ai déjà le code pour les structures de données
<Fichiers joints>
```

Le code généré a ensuite été extrait manuellement avec un découpage fonctionnel.

2. Génération de docstrings [Mode agent] :

```text
Je travaille sur un projet d'ISN (info, python, customtkinter) en 2A à l'INSA Lyon. 
Je souhaite que tu rédiges des docstrings pour les fonctions qui n'en n'ont pas encore, 
en restant synthétique et en précisant les entrées et les sorties. 
```

Une relecture à l'aide de la "diff" a été effectuée afin de s'assurer de la qualité des docstrings générées et de leur
pertinence par rapport au code existant.

3. Tentatives de création d'une classe de sérialisation générique :

```text
Implement JsonSerializable class in python wich is a generic class that can be used
to serialize and deserialize objects to and from JSON format. The class should have two methods: 
serialize() and deserialize(). The serialize() method should convert the object to a JSON 
string, while the deserialize() method should create an object from a JSON string.
```

Ce prompt a donné une classe trop complexe pour notre niveau et avons choisi d'implémenter manuellement la logique de
désérialisation.
