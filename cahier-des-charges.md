# Projet ISN — NutriTrack

**Auteurs :** Yanis Belaid, Marouan El-Hamdeoui, Nolan Mahadali, Léo Peyronnet, Dhia Somai

---

## 1. Présentation générale du projet

### 1.1 Contexte

De plus en plus de personnes cherchent à mieux gérer leur alimentation, que ce soit pour perdre du poids, prendre de la masse, améliorer leurs performances sportives ou simplement adopter de meilleures habitudes de vie. Pourtant, il est souvent difficile d'avoir une vision claire de ce que l'on consomme réellement au quotidien. Les apports en calories, protéines, glucides, lipides sont rarement connus avec précision.

La plupart des solutions existantes nécessitent une connexion internet, un compte en ligne ou le partage de données personnelles. NutriTrack, une application locale et simple d'utilisation, a donc été conçue pour permettre à chaque utilisateur de suivre son alimentation, d'analyser ses habitudes et de recevoir des recommandations adaptées, sans dépendre d'un service distant.

### 1.2 Objectif du projet

NutriTrack est une application desktop développée en Python, permettant à chaque utilisateur de :

- Saisir et suivre ses apports nutritionnels quotidiens
- Définir des objectifs physiques personnalisés (prise de masse, perte de poids, maintien)
- Visualiser des statistiques sur son hygiène de vie
- Recevoir des recommandations alimentaires pour atteindre ses macros-cibles
- Être alerté en cas de dépassement de seuils critiques (sel, sucre, lipides saturés, etc.)

### 1.3 Périmètre du projet

Le projet est limité à une application locale, sans synchronisation en ligne. Les données de chaque utilisateur sont stockées dans des fichiers JSON distincts sur le système de fichiers local. La base de données alimentaire est partagée entre tous les utilisateurs et stockée dans un fichier CSV ou JSON dédié.

---

## 2. Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Langage | Python | Logique applicative, algorithmes nutritionnels |
| Interface graphique | CustomTkinter et Tkinter | UI moderne, widgets natifs |
| Stockage utilisateur | JSON (un fichier par utilisateur) | Historique des journées, profil, préférences |
| Base alimentaire | CSV ou JSON partagé | Référentiel des aliments et valeurs nutritionnelles |
| Visualisation | Matplotlib | Graphiques de statistiques nutritionnelles |

---

## 3. Description des fonctionnalités

### 3.1 Page d'accueil

La page d'accueil est le point d'entrée de l'application. Elle permet de sélectionner un profil utilisateur existant ou d'en créer un nouveau.

**Fonctionnalités :**

- Liste déroulante des profils existants
- Formulaire de création de profil : nom, âge, taille, poids, sexe, objectif physique

### 3.2 Page Gestion nutritionnelle

Cette page constitue le cœur de l'application. Elle permet de saisir les aliments consommés dans la journée et d'évaluer les apports par rapport aux besoins.

**Formulaire d'ajout de consommation :**

- Champ de recherche avec auto-complétion sur la base alimentaire
- Saisie de la quantité en grammes
- Bouton « Ajouter » mettant à jour la liste du jour et le fichier JSON
- Liste des entrées du jour (aliment, quantité, kcal, protéines, glucides, lipides)
- Possibilité de supprimer une entrée

### 3.3 Page Statistiques

Cette page offre une vue synthétique de l'hygiène de vie de l'utilisateur sur une période donnée.

**Graphiques disponibles :**

- Évolution des apports caloriques sur les 7 / 30 derniers jours (courbe)
- Répartition moyenne des macronutriments sur la période (camembert)
- Histogramme comparatif consommé vs cible par macro
- Évolution du taux de sel et de sucre sur la période (courbe avec seuil affiché)
- Score de cohérence nutritionnelle : pourcentage de jours où l'objectif a été respecté

---

## 4. Algorithmes

NutriTrack permet de répondre aux besoins de suivi nutritionnel à travers trois algorithmes principaux :

- **Algorithme de calcul des apports nutritionnels** : détermine les apports totaux sur une journée.
- **Algorithme de détection de dépassement** : identifie les seuils nutritionnels dépassés (sucre, sel, lipides, etc.).
- **Algorithme de recommandation alimentaire** : propose des aliments adaptés pour compléter les besoins nutritionnels restants.
