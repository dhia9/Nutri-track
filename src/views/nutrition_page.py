import customtkinter as ctk
from src.controllers.main_controller import MainController


class NutritionPage(ctk.CTkFrame):
    def __init__(self, parent, main_controller: MainController):
        super().__init__(parent)
        self.parent = parent
        self.main_win = parent.master
        self.main_controller = main_controller
        self.controller = self.main_controller.controllers["Nutrition"]
        self.controller.view = self  # Assigner la view au contrôleur

        self.liste_aliments = []
        
        # Variables de pagination
        self.items_per_page = 20
        self.current_page = 0
        self.all_foods = []  # Liste complète des aliments
        self.filtered_foods = []  # Aliments filtrés par recherche
        self.is_filtered = False
        self.selected_foods = {}  # Garder track des aliments sélectionnés même hors page

        # Configuration du grid principal
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
        for i in range(15):
            self.grid_rowconfigure(i, weight=1 if i >= 5 else 0)

        # Titre principal
        self.title = ctk.CTkLabel(
            self,
            text="Gestion nutritionnelle",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.title.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 0)
        )

        # Sous-titre Profil
        self.tiltle2 = ctk.CTkLabel(
            self,
            text=f"Profil : {self.controller.current_profile.name}",
            font=ctk.CTkFont(size=13),
            text_color="#A8AFB6",
        )
        self.tiltle2.grid(
            row=1, column=0, columnspan=3, sticky="w", padx=20, pady=(5, 0)
        )

        # Cartes de macros (Calories, Protéines, Glucides, Lipides)
        self._create_macro_card("Calories", "frame_carre_noir1", 2, 0, 2)
        self._create_macro_card("Protéines", "frame_carre_noir2", 2, 2, 3)
        self._create_macro_card("Glucides", "frame_carre_noir3", 2, 5, 3)
        self._create_macro_card("Lipides", "frame_carre_noir4", 2, 8, 2)

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
            row=5,
            column=0,
            columnspan=3,
            rowspan=10,
            padx=10,
            pady=(10, 5),
            sticky="nsew",
        )

        self._configure_frame_grid(self.frame_ajout)

        self.bouton_aliment = ctk.CTkButton(
            self.frame_ajout,
            text="✚ Ajouter un menu",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A8AFB6",
            command=self.controller.add_menu,
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
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.controller.search_foods(self.search_entry.get()),
        )

        # Frame scrollable pour la liste d'aliments
        self.items_frame = ctk.CTkScrollableFrame(
            self.frame_ajout, fg_color="#35393D", corner_radius=10
        )
        self.items_frame.grid(
            row=2,
            column=0,
            columnspan=10,
            rowspan=7,
            sticky="nsew",
            padx=15,
            pady=(0, 10),
        )

        self.food_items = {}
        list_food = []
        self.controller.fill_food_list(list_food)
        self.all_foods = list_food
        self.filtered_foods = list_food
        
        # Frame pour la pagination (créer AVANT d'afficher la première page)
        pagination_frame = ctk.CTkFrame(self.frame_ajout, fg_color="#35393D", corner_radius=10)
        pagination_frame.grid(
            row=9,
            column=0,
            columnspan=10,
            sticky="ew",
            padx=15,
            pady=(5, 10),
        )
        
        # Bouton Précédent
        self.btn_prev_page = ctk.CTkButton(
            pagination_frame,
            text="◀ Précédent",
            width=100,
            font=ctk.CTkFont(size=10),
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.controller.previous_page
        )
        self.btn_prev_page.pack(side="left", padx=5, pady=5)
        
        # Label pour afficher la page actuelle
        self.page_label = ctk.CTkLabel(
            pagination_frame,
            text="Page 1 / 1",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#A8AFB6",
        )
        self.page_label.pack(side="left", padx=20, pady=5, expand=True)
        
        # Bouton Suivant
        self.btn_next_page = ctk.CTkButton(
            pagination_frame,
            text="Suivant ▶",
            width=100,
            font=ctk.CTkFont(size=10),
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.controller.next_page
        )
        self.btn_next_page.pack(side="right", padx=5, pady=5)
        
        # Afficher la première page (APRES avoir créé les boutons)
        self._display_current_page()

        self.frame_aliment = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_aliment.grid(
            row=5,
            column=3,
            columnspan=7,
            rowspan=10,
            padx=10,
            pady=(10, 5),
            sticky="nsew",
        )

        self._configure_frame_grid(self.frame_aliment)

        self.frame_aliment_label = ctk.CTkLabel(
            self.frame_aliment,
            text="📋 Menus du jour",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#A8AFB6",
        )
        self.frame_aliment_label.grid(
            row=0, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        # Scrollable frame pour afficher les menus du jour
        self.menus_scrollable_frame = ctk.CTkScrollableFrame(
            self.frame_aliment, fg_color="#35393D", corner_radius=10
        )
        self.menus_container = ctk.CTkFrame(
            self.menus_scrollable_frame, fg_color="transparent"
        )

        self.menus_container.pack(fill="both", expand=True)
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

        self.progress_proteine = ctk.CTkProgressBar(
            self.frame_carre_noir2,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        self.progress_proteine.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

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
        self.calories_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.proteines_value_label = ctk.CTkLabel(
            self.frame_carre_noir2,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.proteines_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.glucides_value_label = ctk.CTkLabel(
            self.frame_carre_noir3,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.glucides_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.lipides_value_label = ctk.CTkLabel(
            self.frame_carre_noir4,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        self.lipides_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        # Bouton pour choisir le menu proposé
        self.bouton_menu = ctk.CTkButton(
            self.frame_ajout,
            text="Menu Favoris",
            font=ctk.CTkFont(size=10, weight="bold"),
            corner_radius=10,
            fg_color="#4CAF50",
            hover_color="#45a049",
        )
        self.bouton_menu.grid(row=0, column=1, sticky="w", padx=15, pady=(10, 0))

        self.bouton_menu.bind("<Button-1>", self.controller.show_favorite_menus)

        # Afficher les menus initialement après la création de tous les labels
        self.controller.display_menus()

        self.suggestion_card = ctk.CTkFrame(
            self.menus_scrollable_frame,
            fg_color="#2A2A4A",
            corner_radius=10,
            height=120,
        )
        self.suggestion_card.pack(fill="x", padx=5, pady=(5, 10))
        self.suggestion_card.pack_propagate(False)

        self.suggestion_card.grid_columnconfigure(0, weight=1)
        self.suggestion_card.grid_columnconfigure(1, weight=1)

        self.suggestion_title = ctk.CTkLabel(
            self.suggestion_card,
            text="Suggérer un menu",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#FFFFFF",
        )
        self.suggestion_title.grid(
            row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 4)
        )

        self.label_nap = ctk.CTkLabel(
            self.suggestion_card,
            text="nap : facteur d'activité physique",
            font=ctk.CTkFont(size=11),
            text_color="#A8AFB6",
        )
        self.label_nap.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=(0, 2))

        self.input_nap = ctk.CTkEntry(
            self.suggestion_card,
            width=90,
            height=28,
            corner_radius=6,
            fg_color="#35393D",
            border_color="#4CAF50",
            border_width=1,
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=11),
        )
        self.input_nap.insert(
            0, str(self.controller.current_profile.suggestCaracteristics["nap"])
        )
        self.input_nap.bind("<KeyRelease>", self.controller.mealPerD_change)
        self.input_nap.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=(0, 8))

        self.label_mealPerD = ctk.CTkLabel(
            self.suggestion_card,
            text="Nombre de repas par jour",
            font=ctk.CTkFont(size=11),
            text_color="#A8AFB6",
        )
        self.label_mealPerD.grid(row=1, column=1, sticky="w", padx=(5, 10), pady=(0, 2))

        self.input_mealPerD = ctk.CTkEntry(
            self.suggestion_card,
            width=90,
            height=28,
            corner_radius=6,
            fg_color="#35393D",
            border_color="#4CAF50",
            border_width=1,
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=11),
        )
        self.input_mealPerD.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=(0, 8))
        self.input_mealPerD.insert(
            0,
            str(self.controller.current_profile.suggestCaracteristics["meals_per_day"]),
        )
        self.input_mealPerD.bind("<KeyRelease>", self.controller.mealPerD_change)
        self.bouton_suggestion = ctk.CTkButton(
            self.suggestion_card,
            text="Suggérer",
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45A049",
        )

        self.bouton_suggestion.grid(row=2, column=2, columnspan=1, pady=(0, 10), padx=7)
        self.bouton_suggestion.bind("<Button-1>", self.controller.show_Suggested_menus)

    def _configure_frame_grid(self, frame):
        """Factorisation : Configure la grille d'un frame avec poids égal"""
        for i in range(10):
            frame.grid_columnconfigure(i, weight=1)
            frame.grid_rowconfigure(i, weight=1)

    def _display_current_page(self):
        """Affiche les aliments de la page actuelle"""
        # Vider le frame
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.food_items.clear()
        
        # Déterminer la liste à utiliser (filtrée ou complète)
        foods_to_display = self.filtered_foods if self.is_filtered else self.all_foods
        
        # Calculer les indices de début et fin
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_foods = foods_to_display[start_idx:end_idx]
        
        # Créer les checkboxes pour les aliments de cette page
        for food in page_foods:
            item_frame = ctk.CTkFrame(
                self.items_frame, fg_color="#2A2A4A", corner_radius=8
            )
            item_frame.pack(fill="x", padx=5, pady=5)

            # Restaurer l'état précédent si l'aliment était sélectionné
            initial_state = "on" if self.selected_foods.get(food, False) else "off"
            var = ctk.StringVar(value=initial_state)
            
            # Ajouter un callback pour sauvegarder l'état de sélection
            def make_callback(food_name, var_ref):
                def on_change():
                    self.selected_foods[food_name] = (var_ref.get() == "on")
                return on_change
            
            checkbox = ctk.CTkCheckBox(
                item_frame,
                text=food,
                variable=var,
                onvalue="on",
                offvalue="off",
                text_color="#FFFFFF",
                fg_color="#4CAF50",
                checkmark_color="#35393D",
                command=make_callback(food, var)
            )
            checkbox.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            self.food_items[food] = {
                "var": var,
                "checkbox": checkbox,
                "frame": item_frame,
            }
        
        # Mettre à jour les labels et boutons de pagination
        total_pages = (len(foods_to_display) + self.items_per_page - 1) // self.items_per_page
        if total_pages == 0:
            total_pages = 1
            
        self.page_label.configure(text=f"Page {self.current_page + 1} / {total_pages}")
        
        # Gérer l'état des boutons
        if self.current_page > 0:
            self.btn_prev_page.configure(state="normal", fg_color="#4CAF50")
        else:
            self.btn_prev_page.configure(state="disabled", fg_color="#777777")
            
        if self.current_page < total_pages - 1:
            self.btn_next_page.configure(state="normal", fg_color="#4CAF50")
        else:
            self.btn_next_page.configure(state="disabled", fg_color="#777777")

    def _update_pagination(self, foods_list):
        """Met à jour la pagination après une recherche"""
        self.filtered_foods = foods_list
        self.is_filtered = True
        self.current_page = 0
        self._display_current_page()

    def _create_macro_card(self, macro_name, frame_attr, row, col_start, col_span):
        """Factorisation : Crée une carte de macro (Calories, Protéines, etc.)"""
        frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        frame.grid(
            row=row,
            column=col_start,
            columnspan=col_span,
            padx=10,
            pady=20,
            sticky="ew",
        )
        self._configure_frame_grid(frame)
        setattr(self, frame_attr, frame)

        # Label du titre
        label = ctk.CTkLabel(frame, text=macro_name, font=ctk.CTkFont(size=13))
        label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))
        setattr(self, f"{macro_name.lower()}_label", label)

        # Barre de progression
        progress = ctk.CTkProgressBar(
            frame,
            width=300,
            height=10,
            corner_radius=5,
            progress_color="#2DBA7F",
            fg_color="#2A2A4A",
        )
        progress.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))
        setattr(self, f"progress_{macro_name.lower()}", progress)

        # Label de valeur
        value_label = ctk.CTkLabel(
            frame,
            text="0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50",
        )
        value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))
        setattr(self, f"{macro_name.lower()}_value_label", value_label)
