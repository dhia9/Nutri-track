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
            font=ctk.CTkFont(size=12),
            text_color=self.main_controller.theme_colors["text_secondary"],
        )

        self.tiltle2.grid(
            row=1, column=0, columnspan=3, sticky="w", padx=20, pady=(5, 0)
        )

        # Cartes de macros (Calories, Protéines, Glucides, Lipides)
        self._create_macro_card("Calories", "frame_carre_noir1", 2, 0, 2)
        self._create_macro_card("Protéines", "frame_carre_noir2", 2, 2, 3)
        self._create_macro_card("Glucides", "frame_carre_noir3", 2, 5, 3)
        self._create_macro_card("Lipides", "frame_carre_noir4", 2, 8, 2)

        date_frame = ctk.CTkFrame(
            self, fg_color=self.main_controller.theme_colors["frame"], corner_radius=10
        )
        date_frame.grid(row=0, column=8, sticky="w", padx=10, pady=5)

        self.button_previous = ctk.CTkButton(
            date_frame,
            text="◀",
            width=30,
            text_color=self.main_controller.theme_colors.get("text", "#2A2D30"),
            fg_color=self.main_controller.theme_colors["frame"],
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=self.main_controller.theme_colors["button_hover"],
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
            text_color=self.main_controller.theme_colors.get("text", "#2A2D30"),
            fg_color=self.main_controller.theme_colors["frame"],
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=self.main_controller.theme_colors["button_hover"],
            corner_radius=10,
        )
        self.button_next.grid(row=0, column=2, padx=4)
        self.button_next.bind("<Button-1>", self.controller.next_day)

        self.frame_ajout = ctk.CTkFrame(
            self, corner_radius=15, fg_color=self.main_controller.theme_colors["frame"]
        )
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
            corner_radius=10,
            text_color=self.main_controller.theme_colors["text"],
            command=self.controller.add_menu,
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
        )

        self.bouton_aliment.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))

        # Barre de recherche
        self.search_entry = ctk.CTkEntry(
            self.frame_ajout,
            placeholder_text="Rechercher un aliment...",
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.settings.theme,
            border_width=2,
            text_color=self.main_controller.theme_colors["text"],
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
            self.frame_ajout,
            fg_color=self.main_controller.theme_colors["frame"],
            corner_radius=10,
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
        list_food = []
        self.controller.fill_food_list(list_food)

        for food in list_food:
            item_frame = ctk.CTkFrame(
                self.items_frame,
                fg_color=self.main_controller.theme_colors["frame_dark"],
                corner_radius=8,
            )
            item_frame.pack(fill="x", padx=5, pady=5)

            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(
                item_frame,
                text=food,
                variable=var,
                onvalue="on",
                offvalue="off",
                text_color=self.main_controller.theme_colors["text"],
                fg_color=self.main_controller.settings.theme,
                checkmark_color=self.main_controller.theme_colors["frame"],
                hover_color=self.main_controller.darken_color(self.main_controller.settings.theme),
            )
            checkbox.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            self.food_items[food] = {
                "var": var,
                "checkbox": checkbox,
                "frame": item_frame,
            }

        self.frame_aliment = ctk.CTkFrame(
            self, corner_radius=15, fg_color=self.main_controller.theme_colors["frame"]
        )
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
            text="Menus du jour",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.main_controller.theme_colors["text_secondary"],
        )
        self.frame_aliment_label.grid(
            row=0, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        # Scrollable frame pour afficher les menus du jour
        self.menus_scrollable_frame = ctk.CTkScrollableFrame(
            self.frame_aliment,
            fg_color=self.main_controller.theme_colors["frame"],
            corner_radius=10,
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
            progress_color=self.main_controller.settings.theme,
            fg_color=self.main_controller.theme_colors["frame_dark"],
        )
        self.progress_calories.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_proteine = ctk.CTkProgressBar(
            self.frame_carre_noir2,
            width=300,
            height=10,
            corner_radius=5,
            progress_color=self.main_controller.settings.theme,
            fg_color=self.main_controller.theme_colors["frame_dark"],
        )
        self.progress_proteine.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_glucides = ctk.CTkProgressBar(
            self.frame_carre_noir3,
            width=300,
            height=10,
            corner_radius=5,
            progress_color=self.main_controller.settings.theme,
            fg_color=self.main_controller.theme_colors["frame_dark"],
        )
        self.progress_glucides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        self.progress_lipides = ctk.CTkProgressBar(
            self.frame_carre_noir4,
            width=300,
            height=10,
            corner_radius=5,
            progress_color=self.main_controller.settings.theme,
            fg_color=self.main_controller.theme_colors["frame_dark"],
        )
        self.progress_lipides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))

        # Labels pour afficher les valeurs des macros
        self.calories_value_label = ctk.CTkLabel(
            self.frame_carre_noir1,
            text="0 kcal",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        self.calories_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.proteines_value_label = ctk.CTkLabel(
            self.frame_carre_noir2,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        self.proteines_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.glucides_value_label = ctk.CTkLabel(
            self.frame_carre_noir3,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        self.glucides_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        self.lipides_value_label = ctk.CTkLabel(
            self.frame_carre_noir4,
            text="0 g",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        self.lipides_value_label.grid(
            row=2, column=0, sticky="w", padx=15, pady=(10, 0)
        )

        # Bouton pour choisir le menu proposé
        self.bouton_menu = ctk.CTkButton(
            self.frame_ajout,
            text="Menu Favoris",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=10,
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
        )

        self.bouton_menu.grid(row=0, column=1, sticky="w", padx=15, pady=(10, 0))

        self.bouton_menu.bind("<Button-1>", self.controller.show_favorite_menus)

        # Afficher les menus initialement après la création de tous les labels
        self.controller.display_menus()

        self.suggestion_card = ctk.CTkFrame(
            self.menus_scrollable_frame,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            corner_radius=10,
            height=120,
        )
        self.suggestion_card.pack(
            fill="x", padx=5, pady=(5, 10), before=self.menus_container
        )
        self.suggestion_card.pack_propagate(False)

        self.suggestion_card.grid_columnconfigure(0, weight=1)
        self.suggestion_card.grid_columnconfigure(1, weight=1)

        self.suggestion_title = ctk.CTkLabel(
            self.suggestion_card,
            text="Suggérer un menu",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.main_controller.theme_colors["text"],
        )
        self.suggestion_title.grid(
            row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 4)
        )

        self.label_nap = ctk.CTkLabel(
            self.suggestion_card,
            text="nap : facteur d'activité physique",
            font=ctk.CTkFont(size=11),
            text_color=self.main_controller.theme_colors["text_secondary"],
        )
        self.label_nap.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=(0, 2))

        self.input_nap = ctk.CTkEntry(
            self.suggestion_card,
            width=90,
            height=28,
            corner_radius=6,
            fg_color=self.main_controller.theme_colors["frame"],
            border_color=self.main_controller.settings.theme,
            border_width=1,
            text_color=self.main_controller.theme_colors["text"],
            font=ctk.CTkFont(size=11),
            validate="key",
            validatecommand=(self.register(self.main_controller.validate_float), "%P"),
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
            text_color=self.main_controller.theme_colors["text"],
        )
        self.label_mealPerD.grid(row=1, column=1, sticky="w", padx=(5, 10), pady=(0, 2))

        self.input_mealPerD = ctk.CTkEntry(
            self.suggestion_card,
            width=90,
            height=28,
            corner_radius=6,
            fg_color=self.main_controller.theme_colors["frame"],
            border_color=self.main_controller.settings.theme,
            border_width=1,
            text_color=self.main_controller.theme_colors["text"],
            font=ctk.CTkFont(size=11),
            validate="key",
            validatecommand=(self.register(self.main_controller.validate_int), "%P"),
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
            corner_radius=10,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
        )

        self.bouton_suggestion.grid(row=2, column=2, columnspan=1, pady=(0, 10), padx=7)
        self.bouton_suggestion.bind("<Button-1>", self.controller.show_Suggested_menus)

    def _configure_frame_grid(self, frame):
        """Factorisation : Configure la grille d'un frame avec poids égal"""
        for i in range(10):
            frame.grid_columnconfigure(i, weight=1)
            frame.grid_rowconfigure(i, weight=1)

    def _create_macro_card(self, macro_name, frame_attr, row, col_start, col_span):
        """Factorisation : Crée une carte de macro (Calories, Protéines, etc.)

        Args:
            macro_name: Nom du macronutriment.
            frame_attr: Nom de l'attribut pour stocker le frame.
            row: Ligne du grid où placer la carte.
            col_start: Colonne de début.
            col_span: Nombre de colonnes à couvrir.
        """
        frame = ctk.CTkFrame(
            self, corner_radius=15, fg_color=self.main_controller.theme_colors["frame"]
        )
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
            progress_color=self.main_controller.settings.theme,
            fg_color=self.main_controller.theme_colors["frame_dark"],
        )
        progress.grid(row=1, column=0, sticky="ew", padx=15, pady=(10, 0))
        setattr(self, f"progress_{macro_name.lower()}", progress)

        # Label de valeur
        value_label = ctk.CTkLabel(
            frame,
            text="0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.main_controller.settings.theme,
        )
        value_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 0))
        setattr(self, f"{macro_name.lower()}_value_label", value_label)
