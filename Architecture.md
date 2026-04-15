# Architecture

NUTRITRACK/
│
├── src/ 
│    │
│    ├── views/                       # Pages de l'interface (CustomTkinter)
│    │   ├── home_page.py
│    │   ├── nutrition_page.py
│    │   └── stats_page.py
│    │
│    ├── models/                    # Algorithmes et logique
│    │   ├── nutrition_calc.py
│    │   ├── threshold_check.py 
│    │   └── recommender.py   
│    │
│    ├── controllers/                    
│    │   ├── nutrition_calc.py
│    │   ├── threshold_check.py 
│    │   └── recommender.py  
│    │
│    ├── data/        
│    │   ├── json/              
│    │   │    └── aliments.json
│    │   │   
│    │   ├── csv/               
│    │   │    └── history.csv
│    │   │   
│    │   └── data_loader.py     # accès aux fichiers             
│    │
│    └── assets/                   # Ressources statiques
│        ├── images/
│        └── fonts/
│
├── tests/    
│   │            
│   ├── test_models/
│   │   ├── test_nutrition_calc.py
│   │   └── test_threshold_check.py
│   │
│   ├── test_controllers/
│   │   └── test_recommender.py
│   │
│   └── test_data/
│       └── test_data_loader.py
│
├── venv/                     # Environnement virtuel Python (non obligatoire)
├── main.py                   # Point d'entrée (vu principale, lancement de l'app)
├── .gitignore                # contient venv/
├── cahier-des-charges.md
├── Architecture.md            # Ce fichier
├── README.md
└── REQUIREMENTS.txt
