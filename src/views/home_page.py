import customtkinter as ctk


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, main_controller):
        super().__init__(parent, fg_color="transparent")
        self.main_controller = main_controller
        self.main_controller.controllers["Home"].view = self
        self.controlleur = self.main_controller.controllers["Home"]

        # Couleurs de boutons profil basées sur le thème
        self.PROFILE_BTN_DEFAULT = self.main_controller.settings.theme
        self.PROFILE_BTN_DEFAULT_HOVER = self.main_controller.darken_color(
            self.PROFILE_BTN_DEFAULT
        )

        self.PROFILE_BTN_SELECTED = "#1F2327"
        self.PROFILE_BTN_SELECTED_HOVER = self.main_controller.darken_color(
            self.PROFILE_BTN_SELECTED
        )
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.profile_buttons = {}

        self.titre = ctk.CTkLabel(
            self,
            text="Bienvenue sur NutriTrack",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.titre.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 0)
        )

        self.profil = ctk.CTkLabel(
            self,
            text="Sélectionnez un profil ou créez-en un nouveau pour commencer",
            font=ctk.CTkFont(size=12),
            text_color=self.main_controller.theme_colors["text_secondary"],
        )
        self.profil.grid(row=1, column=0, columnspan=3, sticky="w", padx=20)

        self.label3 = ctk.CTkLabel(
            self,
            text="Profils existants",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label3.grid(
            row=2, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 5)
        )

        self.profiles_container = ctk.CTkScrollableFrame(
            self,
            fg_color=self.main_controller.theme_colors["content"],
            corner_radius=10,
            height=170,
        )
        self.profiles_container.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=20,
            pady=(0, 10),
        )
        self.profiles_container.grid_columnconfigure((0, 1, 2), weight=1)
        self.render_profiles()

        self.label4 = ctk.CTkLabel(
            self,
            text="Créer un nouveau profil",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label4.grid(row=4, column=0, columnspan=3, sticky="w", padx=20, pady=10)

        frame_carre_noir = ctk.CTkFrame(
            self, corner_radius=15, fg_color=self.main_controller.theme_colors["frame"]
        )
        frame_carre_noir.grid(row=5, column=0, columnspan=3, padx=20, sticky="ew")
        frame_carre_noir.grid_columnconfigure((0, 1, 2), weight=1)

        self.nom = ctk.CTkLabel(
            frame_carre_noir,
            text="Prénom et nom",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.nom.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        self.nom_entry = ctk.CTkEntry(
            frame_carre_noir,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.theme_colors["button"],
        )
        self.nom_entry.grid(row=1, column=0, sticky="ew", padx=20)

        int_vcmd = (self.register(self.main_controller.validate_int), "%P")
        float_vcmd = (self.register(self.main_controller.validate_float), "%P")

        # Âge
        self.age_label = ctk.CTkLabel(
            frame_carre_noir,
            text="Âge",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.age_label.grid(row=0, column=1, sticky="w", padx=20, pady=(20, 10))
        self.age_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=int_vcmd,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.theme_colors["button"],
        )
        self.age_entry.grid(row=1, column=1, sticky="ew", padx=20)

        # Taille
        self.taille_label = ctk.CTkLabel(
            frame_carre_noir,
            text="Taille (cm)",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.taille_label.grid(row=2, column=0, sticky="w", padx=20, pady=(16, 10))
        self.taille_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=float_vcmd,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.theme_colors["button"],
        )
        self.taille_entry.grid(row=3, column=0, sticky="ew", padx=20)

        # Poids
        self.poids_label = ctk.CTkLabel(
            frame_carre_noir,
            text="Poids (kg)",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.poids_label.grid(row=2, column=1, sticky="w", padx=20, pady=(16, 10))
        self.poids_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=float_vcmd,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.theme_colors["button"],
        )
        self.poids_entry.grid(row=3, column=1, sticky="ew", padx=20)

        self.sexe_label = ctk.CTkLabel(
            frame_carre_noir,
            text="Sexe",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.sexe_label.grid(row=2, column=2, sticky="w", padx=20, pady=(16, 10))

        self.sexe_var = ctk.StringVar(value="Homme")

        self.boutton_sexe1 = ctk.CTkRadioButton(
            frame_carre_noir,
            text="Homme",
            variable=self.sexe_var,
            value="Homme",
            fg_color=self.PROFILE_BTN_DEFAULT,
        )
        self.boutton_sexe1.grid(row=3, column=2, sticky="w", padx=20)

        self.boutton_sexe2 = ctk.CTkRadioButton(
            frame_carre_noir,
            text="Femme",
            variable=self.sexe_var,
            value="Femme",
            fg_color=self.PROFILE_BTN_DEFAULT,
        )
        self.boutton_sexe2.grid(row=3, column=2, sticky="w", padx=120)

        # Objectif poids
        self.objectif_label = ctk.CTkLabel(
            frame_carre_noir,
            text="Objectif poids (kg)",
            text_color=self.main_controller.theme_colors["text"],
        )
        self.objectif_label.grid(row=4, column=0, sticky="w", padx=20, pady=(16, 10))

        self.objectif_var = ctk.StringVar()

        self.objectif_Entry = ctk.CTkEntry(
            frame_carre_noir,
            textvariable=self.objectif_var,
            placeholder_text="Objectif de Poids",
            validate="key",
            validatecommand=float_vcmd,
            fg_color=self.main_controller.theme_colors["frame_dark"],
            border_color=self.main_controller.theme_colors["button"],
        )
        self.objectif_Entry.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20),
        )

        self.boutton_valider = ctk.CTkButton(
            frame_carre_noir,
            text="Créer le profil",
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=10,
        )
        self.boutton_valider.grid(row=5, column=2, sticky="e", padx=20, pady=(0, 20))
        self.boutton_valider.bind("<Button-1>", lambda event: self.create_profile())

    def render_profiles(self):
        """Affiche les profils existants dans la liste des profils.

        Recrée les boutons de sélection des profils et met à jour l'interface
        pour afficher le statut du profil actuellement sélectionné.
        """
        for child in self.profiles_container.winfo_children():
            child.destroy()
        self.profile_buttons.clear()

        profiles = self.controlleur.main_controller.settings.profiles
        if not profiles:
            empty_label = ctk.CTkLabel(
                self.profiles_container,
                text="Aucun profil existant pour le moment.",
                text_color=self.main_controller.theme_colors["text_secondary"],
            )
            empty_label.grid(row=0, column=0, sticky="w", padx=12, pady=12)
            return

        for index, profile in enumerate(profiles):
            row = index // 3
            col = index % 3

            card = ctk.CTkFrame(
                self.profiles_container,
                corner_radius=12,
                fg_color=self.main_controller.theme_colors["button"],
            )
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

            ctk.CTkLabel(
                card,
                text=profile.name,
                font=ctk.CTkFont(size=16, weight="bold"),
            ).pack(anchor="w", padx=14, pady=(12, 4))

            ctk.CTkLabel(
                card,
                text=f"{profile.age} ans  •  {profile.sex}",
                text_color=self.main_controller.theme_colors["text_secondary"],
            ).pack(anchor="w", padx=14)

            ctk.CTkLabel(
                card,
                text=f"{profile.weight} kg -> objectif {profile.target_weight} kg",
                text_color=self.main_controller.theme_colors["text_secondary"],
            ).pack(anchor="w", padx=14, pady=(2, 10))

            is_selected = (
                self.controlleur.main_controller.current_profile is not None
                and self.controlleur.main_controller.current_profile.name
                == profile.name
            )

            select_button = ctk.CTkButton(
                card,
                text="Profil Sélectionné" if is_selected else "Sélectionner",
                height=34,
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=10,
                fg_color=(
                    self.PROFILE_BTN_SELECTED
                    if is_selected
                    else self.PROFILE_BTN_DEFAULT
                ),
                hover_color=(
                    self.PROFILE_BTN_SELECTED_HOVER
                    if is_selected
                    else self.PROFILE_BTN_DEFAULT_HOVER
                ),
                text_color="#FFFFFF",
                command=lambda p=profile: self.controlleur.select_profile(p),
            )
            select_button.pack(fill="x", padx=14, pady=(0, 12))
            self.profile_buttons[profile.name] = select_button

    def set_selected_profile(self, profile):
        """Met à jour l'interface pour montrer le profil sélectionné.

        Args:
            profile: Le profil sélectionné (ou None si aucun).
        """

        selected_name = profile.name if profile else None

        for profile_name, button in self.profile_buttons.items():
            is_selected = profile_name == selected_name
            button.configure(
                text="Profil Sélectionné" if is_selected else "Sélectionner",
                fg_color=(
                    self.PROFILE_BTN_SELECTED
                    if is_selected
                    else self.PROFILE_BTN_DEFAULT
                ),
                hover_color=(
                    self.PROFILE_BTN_SELECTED_HOVER
                    if is_selected
                    else self.PROFILE_BTN_DEFAULT_HOVER
                ),
            )

    def create_profile(self):
        """Lance la création d'un nouveau profil et rafraîchit l'affichage.

        Appelle le contrôleur pour créer un nouveau profil, puis recharge
        la liste des profils affichés.
        """
        self.controlleur.create_profile()
        self.render_profiles()
