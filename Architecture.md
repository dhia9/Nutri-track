# Architecture

```
NUTRITRACK/
│
├── src/
│   ├── views/                      # UI (CustomTkinter)
│   │   ├── base_view.py
│   │   ├── main_window.py
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   ├── nutrition_page.py
│   │   └── stats_page.py
│   │
│   ├── controllers/                # Orchestration / evenements
│   │   ├── main_controller.py
│   │   ├── home_controller.py
│   │   ├── login_controller.py
│   │   ├── nutrition_controller.py
│   │   └── stats_controller.py
│   │
│   ├── models/                     # Domaine
│   │   ├── settings.py             # Liste des profils + regles
│   │   ├── profile.py
│   │   ├── menu.py
│   │   ├── food.py
│   │   ├── food_menu.py
│   │   ├── macro.py
│   │   └── macro_type.py
│   │
│   ├── data/                       # Acces aux donnees
│   │   ├── data_loader.py
│   │   ├── food_data.py
│   │   └── json/
│   │       ├── aliments.json
│   │       └── profils.json
│   │
│   ├── utils/
│   │   └── json_serializable.py
│   │
│   └── assets/                     # Ressources statiques
│       ├── images/
│       └── fonts/
│
├── tests/
│   ├── test_models/
│   ├── test_controllers/
│   └── test_data/
│
├── venv/
├── main.py
├── .gitignore
├── cahier-des-charges.md
├── Architecture.md                 # Ce fichier
├── README.md
└── REQUIREMENTS.txt
```

```mermaid
classDiagram
    direction LR

    class CTkBase {
        <<external>>
    }

    CTkBase <|-- Views
    CTkBase <|-- Window
    MainController ..> Settings: current_profile
    MainController ..> FoodData
    MainController ..> DataLoader
    MainController ..> Views
    MainController ..> Window
    JsonSerializable <|-- Settings
    JsonSerializable <|-- FoodData
    Menu *-- FoodMenu: content
    FoodMenu *-- Food: item
    Food *-- Macro: macros
    Macro --> MacroType: type
    Profile *-- Menu: eating_habits
    Settings o-- Profile: profiles
    FoodData o-- Food: food_data

    namespace UI {
        class Views {
            +__init__()
        }
        class Window {
            +__init__()
        }
    }

    namespace Controllers {
        class MainController {
            +current_profile: Profile
            +event_handlers()
            +__init__()
        }
    }

    namespace Models {
        class Settings {
            +profiles: Profile[]
            +create_profile(attributes...)
        }
        class Food {
            +name: str
            +macros: Macro[]
            +__init__(name)
        }
        class FoodMenu {
            +quantity: int
        }
        class Macro {
            +type: MacroType
            +value: float
            +__init__(type, value)
        }
        class Menu {
            +id: int
            +date: date
            +content: FoodMenu[]
        }
        class MacroType {
            <<enum>>
            CALORIE
            PROTEIN
            FAT
            CARBOHYDRATE
        }
        class Profile {
            +name: str
            +age: int
            +height: float
            +weight: float
            +sex: str
            +target_weight: float
            +eating_habits: Menu[]
            +__init__(attributes...)
            +get_imc()
        }
    }

    namespace Data {
        class DataLoader {
            +load_foods() Food[]
            +load_profiles() Profile[]
        }
        class FoodData {
            +food_data: Food[]
        }
    }

    namespace Utils {
        class JsonSerializable {
            +serialize(path)
            +deserialize(path)
        }
    }
```
