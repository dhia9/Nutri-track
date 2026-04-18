# Architecture

```
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
│    │   ├── user.py
│    │   ├── profile.py 
│    │   └── nutrition.py   
│    │
│    ├── controllers/                    
│    │   ├── control_home_page.py
│    │   ├── control_nutrition_page.py
│    │   └── control_stats_page.py  
│    │
│    ├── data/        
│    │   ├── json/              
│    │   │   ├── aliments.json
│    │   │   └── profils.json  
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
├── venv/                     
├── main.py                   
├── .gitignore                
├── cahier-des-charges.md
├── Architecture.md            # Ce fichier
├── README.md
└── REQUIREMENTS.txt
```

```mermaid
 classDiagram
    JsonSerializable <|-- Settings
    Food <|-- FoodMenu
    JsonSerializable <|-- FoodData
    ctk <|-- View
    ctk <|-- Window
    MainController ..> Profile: current_profile
    MainController ..> View
    MainController ..> Window
    MainController ..> Utils
    Menu ..> FoodMenu: content
    FoodData ..> Food: food_data
    Profile ..> Menu: eating_habbits
    Profile <.. Settings: profiles
    Food ..> Macro: macros
    Macro ..> MacroType: type

    namespace UI {
        class ctk {
            instance custom tkinter
        }
        class View {
            +init(self)
            +attributs ctk
        }
        class Window {
            +init(self)
            +attributs ctk
        }
    }

    namespace Models {
        class Settings {
            +Profile[] profiles
            +create_profile(self, attributes...)
        }
        class Food {
            +string: name
            +Macro[]: macros
            +init(self, name)
        }
        class FoodData {
            +Food[]: food_data
        }
        class FoodMenu {
            +int: quantity
        }
        class Macro {
            +MacroType: type
            +float: value
            +init(self, type, value)
        }
        class Menu {
            +int: id
            +date: date
            +FoodMenu[]: content
        }
        class MacroType {
            +CALORIE
            +PROTEIN
            +FAT
            +CARBOHYDRATE
        }
        class Profile {
            +str: name
            +int: age
            +float: height
            +float: weight
            +str: sex
            +float: target_weight
            +Menu[]: eating_habbits
            +init(self, attributes...)
            +getIMC()
        }
    }

    namespace Controller {
        class MainController {
            +Profile: current_profile
            +Food[]: food_data
            +event_handlers(self)
            +init(self)
        }
    }
    namespace Utilities {
        class Utils {
            +load_data() Food[]
        }
        class JsonSerializable {
            pas d'attributs
            +serialize(path)
            +deserialize(path)
        }
    }




```
