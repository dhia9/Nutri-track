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
