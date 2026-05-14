import customtkinter as ctk

from datetime import datetime, timedelta
from src.controllers.main_controller import MainController


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent, main_controller: MainController):
        super().__init__(parent)
        self.parent = parent
        self.main_controller = main_controller
        self.controller = self.main_controller.controllers["Nutrition"]
        self.controller.view = self  # Assigner la view au contrôleur

        self.liste_aliments = []

        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.grid_rowconfigure(0, weight=0)

        self.title = ctk.CTkLabel(
            self,
            text="🍽️Gestion nutritionnelle",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.title.grid(row=0, column=0, columnspan=3, sticky="w", padx=20)

        self.tiltle2 = ctk.CTkLabel(
            self, text="Profil : ", font=ctk.CTkFont(size=13), text_color="#A8AFB6"
        )
        self.tiltle2.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(50, 0)
        )

        self.frame_carre_noir1 = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#35393D"
        )
        self.frame_carre_noir1.grid(
            row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_carre_noir1.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir1.grid_rowconfigure(i, weight=1)

        self.frame_carre_noir2 = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#35393D"
        )
        self.frame_carre_noir2.grid(
            row=2, column=2, columnspan=3, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_carre_noir2.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir2.grid_rowconfigure(i, weight=1)

        self.frame_carre_noir3 = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#35393D"
        )
        self.frame_carre_noir3.grid(
            row=2, column=5, columnspan=3, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_carre_noir3.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir3.grid_rowconfigure(i, weight=1)

        self.frame_carre_noir4 = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#35393D"
        )
        self.frame_carre_noir4.grid(
            row=2, column=8, columnspan=2, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_carre_noir4.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir4.grid_rowconfigure(i, weight=1)

        self.calories_label = ctk.CTkLabel(
            self.frame_carre_noir1, text="Calories", font=ctk.CTkFont(size=13)
        )
        self.calories_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.proteines_label = ctk.CTkLabel(
            self.frame_carre_noir2, text="Protéines", font=ctk.CTkFont(size=13)
        )
        self.proteines_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.glucides_label = ctk.CTkLabel(
            self.frame_carre_noir3, text="Glucides", font=ctk.CTkFont(size=13)
        )
        self.glucides_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        self.lipides_label = ctk.CTkLabel(
            self.frame_carre_noir4, text="Lipides", font=ctk.CTkFont(size=13)
        )
        self.lipides_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        date_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=10)
        date_frame.grid(row=0, column=8, sticky="w", padx=10, pady=5)

        self.button_previous = ctk.CTkButton(
            date_frame,
            text="◀",
            width=30,
            fg_color="#000000",
            font=ctk.CTkFont(size=14),
            hover_color="#F1F1F1",
            corner_radius=10,
        )
        self.button_previous.grid(row=0, column=0, padx=4)

        self.button_previous.bind("<Button-1>", self.controller.previous_day)

        self.date_label = ctk.CTkLabel(
            date_frame,
            text=self.controller.current_date.strftime("  %A %d %B %Y  ").capitalize(),
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
        )
        self.date_label.grid(row=0, column=1, padx=4)

        self.button_next = ctk.CTkButton(
            date_frame,
            text="▶",
            width=30,
            fg_color="#0F0A0A",
            font=ctk.CTkFont(size=14),
            hover_color="#F1F1F1",
            corner_radius=10,
        )
        self.button_next.grid(row=0, column=2, padx=4)
        self.button_next.bind("<Button-1>", self.controller.next_day)

        self.frame_ajout = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_ajout.grid(
            row=5, column=0, columnspan=3, rowspan=10, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_ajout.grid_columnconfigure(i, weight=1)
            self.frame_ajout.grid_rowconfigure(i, weight=1)

        self.bouton_aliment = ctk.CTkButton(
            self.frame_ajout,
            text="✚ Ajouter un menu",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#A8AFB6",
            command=self.add_menu,
        )
        self.bouton_aliment.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        # Barre de recherche
        self.search_entry = ctk.CTkEntry(
            self.frame_ajout,
            placeholder_text="🔍 Rechercher un aliment...",
            fg_color="#2A2A4A",
            border_color="#4CAF50",
            border_width=2,
            text_color="#FFFFFF",
        )
        self.search_entry.grid(
            row=1, column=0, columnspan=10, sticky="ew", padx=15, pady=(15, 10)
        )
        self.search_entry.bind("<KeyRelease>", self.search_foods)  # Binder la recherche

        # Frame scrollable pour la liste d'aliments
        self.items_frame = ctk.CTkScrollableFrame(
            self.frame_ajout, fg_color="#35393D", corner_radius=10
        )
        self.items_frame.grid(
            row=2,
            column=0,
            columnspan=10,
            rowspan=8,
            sticky="nsew",
            padx=15,
            pady=(0, 10),
        )

        self.food_items = {}
        # example_foods = ["Pomme", "Poulet grillé", "Riz blanc", "Brocoli", "Œuf", "Yaourt nature", "Pain complet", "Saumon"]
        list_food = []
        self.fill_food_list(list_food)

        for food in list_food:
            item_frame = ctk.CTkFrame(
                self.items_frame, fg_color="#2A2A4A", corner_radius=8
            )
            item_frame.pack(fill="x", padx=5, pady=5)

            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(
                item_frame,
                text=food,
                variable=var,
                onvalue="on",
                offvalue="off",
                text_color="#FFFFFF",
                fg_color="#4CAF50",
                checkmark_color="#35393D",
            )
            checkbox.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            self.food_items[food] = {
                "var": var,
                "checkbox": checkbox,
                "frame": item_frame,
            }

        self.frame_aliment = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D", height=200)
        self.frame_aliment.grid(
            row=5, column=3, columnspan=10, rowspan=10, padx=10, pady=20, sticky="ew"
        )

        for i in range(10):
            self.frame_aliment.grid_columnconfigure(i, weight=1)
            self.frame_aliment.grid_rowconfigure(i, weight=1)

        for i in range(10):
            self.frame_aliment.grid_columnconfigure(i, weight=1)
            self.frame_aliment.grid_rowconfigure(i, weight=1)

        self.frame_aliment_label = ctk.CTkLabel(
            self.frame_aliment,
            text="📋 Menus du jour",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#A8AFB6",
        )
        self.frame_aliment_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        # Scrollable frame pour afficher les menus du jour
        self.menus_scrollable_frame = ctk.CTkScrollableFrame(
            self.frame_aliment, fg_color="#35393D", corner_radius=10
        )
        self.menus_scrollable_frame.grid(
            row=1,
            column=0,
            columnspan=10,
            rowspan=9,
            sticky="nsew",
            padx=15,
            pady=(10, 10),
        )

        self.progress_calories = ctk.CTkProgressBar(
            self.frame_carre_noir1,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        self.progress_calories.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_protéine = ctk.CTkProgressBar(
            self.frame_carre_noir2,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        self.progress_protéine.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_glucides = ctk.CTkProgressBar(
            self.frame_carre_noir3,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        self.progress_glucides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_lipides = ctk.CTkProgressBar(
            self.frame_carre_noir4,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        self.progress_lipides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        # Labels pour afficher les valeurs des macros
        self.calories_value_label = ctk.CTkLabel(
            self.frame_carre_noir1,
            text="0 kcal",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.calories_value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        self.proteines_value_label = ctk.CTkLabel(
            self.frame_carre_noir2,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.proteines_value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        self.glucides_value_label = ctk.CTkLabel(
            self.frame_carre_noir3,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.glucides_value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        self.lipides_value_label = ctk.CTkLabel(
            self.frame_carre_noir4,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.lipides_value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))

        # Afficher les menus initialement après la création de tous les labels
        self.display_menus()


    def fill_food_list(self, food_list):
        self.controller.fill_food_list(food_list)

    def search_foods(self, event):
        """Callback pour la barre de recherche"""
        query = self.search_entry.get()
        self.controller.search_foods(query)

    def add_menu(self):
        self.controller.add_menu()

    def menu_today(self, date:datetime.date):
        self.controller.menu_today(date)
    
    def macros_today(self, date:datetime.date):
        self.controller.macros_today(date)

    def display_menus(self):
        self.controller.display_menus()
