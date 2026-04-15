# Architecture

NUTRITRACK/
│
├── venv/                     # Environnement virtuel Python (non obligatoire)
│
├── ui/                       # Pages de l'interface (CustomTkinter)
│   ├── home_page.py
│   ├── nutrition_page.py
│   └── stats_page.py
│
├── logic/                    # Algorithmes et logique
│   ├── nutrition_calc.py
│   ├── threshold_check.py
│   └── recommender.py
│
├── db/                       # Base de données
│   ├── database.db           # Database local ou connection.py si il s'agit d'une connection
│   ├── queries.py            # requete sql en python pour récupération de données
│   └── schema.py             # requete sql python pour création des tables
│
├── assets/                   # Ressources statiques
│   ├── images/
│   └── fonts/
│
├── main.py                   # Point d'entrée (vu principale, lancement de l'app)
├── .gitignore                # contient venv/
├── cahier-des-charges.md
├── Archtecture.md            # Ce fichier
├── README.md
└── REQUIREMENTS.txt
