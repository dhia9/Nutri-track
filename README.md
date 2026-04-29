# Nutritrack

NutriTrack est une application desktop développée en Python, permettant à chaque utilisateur de :

- Saisir et suivre ses apports nutritionnels quotidiens
- Définir des objectifs physiques personnalisés (prise de masse, perte de poids, maintien)
- Visualiser des statistiques sur son hygiène de vie
- Recevoir des recommandations alimentaires pour atteindre ses macros-cibles
- Être alerté en cas de dépassement de seuils critiques (sel, sucre, lipides saturés, etc.)

## Installation

```
pip install -r requirements.txt
```

## Base de données

Les données sont issues du site [ciqual.aneses.fr](https://ciqual.aneses.fr), qui fournit une base de données complète
sur la composition nutritionnelle des aliments. Cette base de données est intégrée dans l'application pour permettre aux
utilisateurs de rechercher et d'ajouter facilement des aliments à leur suivi nutritionnel.
