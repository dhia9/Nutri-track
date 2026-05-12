import customtkinter as ctk


class HomePage(ctk.CTkFrame):
    PROFILE_BTN_DEFAULT = "#2DBA7F"
    PROFILE_BTN_DEFAULT_HOVER = "#249968"
    PROFILE_BTN_SELECTED = "#1F2327"
    PROFILE_BTN_SELECTED_HOVER = "#1F2327"

    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.main_controller.controllers["Home"].view = self
        self.controlleur = self.main_controller.controllers["Home"]

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
            font=ctk.CTkFont(size=13),
            text_color="#A8AFB6",
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
            fg_color="#17191B",
            corner_radius=12,
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
        self._render_profiles()

        self.label4 = ctk.CTkLabel(
            self,
            text="Créer un nouveau profil",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label4.grid(row=4, column=0, columnspan=3, sticky="w", padx=20, pady=10)

        frame_carre_noir = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        frame_carre_noir.grid(row=5, column=0, columnspan=3, padx=20, sticky="ew")
        frame_carre_noir.grid_columnconfigure((0, 1, 2), weight=1)

        self.nom = ctk.CTkLabel(frame_carre_noir, text="Prénom et nom")
        self.nom.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        self.nom_entry = ctk.CTkEntry(frame_carre_noir)
        self.nom_entry.grid(row=1, column=0, sticky="ew", padx=20)

        # Créer les validateurs
        int_vcmd = (self.register(self._validate_int), "%S")
        float_vcmd = (
            self.register(self._validate_float),
            "%S",
        )

        # Âge
        self.age_label = ctk.CTkLabel(frame_carre_noir, text="Âge")
        self.age_label.grid(row=0, column=1, sticky="w", padx=20, pady=(20, 10))
        self.age_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=int_vcmd,
        )
        self.age_entry.grid(row=1, column=1, sticky="ew", padx=20)

        # Taille
        self.taille_label = ctk.CTkLabel(frame_carre_noir, text="Taille (cm)")
        self.taille_label.grid(row=2, column=0, sticky="w", padx=20, pady=(16, 10))
        self.taille_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=int_vcmd,
        )
        self.taille_entry.grid(row=3, column=0, sticky="ew", padx=20)

        # Poids
        self.poids_label = ctk.CTkLabel(frame_carre_noir, text="Poids (kg)")
        self.poids_label.grid(row=2, column=1, sticky="w", padx=20, pady=(16, 10))
        self.poids_entry = ctk.CTkEntry(
            frame_carre_noir,
            validate="key",
            validatecommand=float_vcmd,
        )
        self.poids_entry.grid(row=3, column=1, sticky="ew", padx=20)

        self.sexe_label = ctk.CTkLabel(frame_carre_noir, text="Sexe")
        self.sexe_label.grid(row=2, column=2, sticky="w", padx=20, pady=(16, 10))

        self.sexe_var = ctk.StringVar(value="Homme")

        self.boutton_sexe1 = ctk.CTkRadioButton(
            frame_carre_noir, text="Homme", variable=self.sexe_var, value="Homme"
        )
        self.boutton_sexe1.grid(row=3, column=2, sticky="w", padx=20)

        self.boutton_sexe2 = ctk.CTkRadioButton(
            frame_carre_noir, text="Femme", variable=self.sexe_var, value="Femme"
        )
        self.boutton_sexe2.grid(row=3, column=2, sticky="w", padx=120)

        # Objectif poids
        self.objectif_label = ctk.CTkLabel(frame_carre_noir, text="Objectif poids (kg)")
        self.objectif_label.grid(row=4, column=0, sticky="w", padx=20, pady=(16, 10))

        self.objectif_var = ctk.StringVar()

        self.objectif_Entry = ctk.CTkEntry(
            frame_carre_noir,
            textvariable=self.objectif_var,
            placeholder_text="Objectif de Poids",
            validate="key",
            validatecommand=float_vcmd,
        )
        self.objectif_Entry.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 20),
        )

        self.boutton_valider = ctk.CTkButton(frame_carre_noir, text="Créer le profil")
        self.boutton_valider.grid(row=5, column=2, sticky="e", padx=20, pady=(0, 20))
        self.boutton_valider.bind("<Button-1>", lambda event: self.create_profile())

    def _render_profiles(self):
        for child in self.profiles_container.winfo_children():
            child.destroy()
        self.profile_buttons.clear()

        profiles = self.controlleur.main_controller.settings.profiles
        if not profiles:
            empty_label = ctk.CTkLabel(
                self.profiles_container,
                text="Aucun profil existant pour le moment.",
                text_color="#A8AFB6",
            )
            empty_label.grid(row=0, column=0, sticky="w", padx=12, pady=12)
            return

        for index, profile in enumerate(profiles):
            row = index // 3
            col = index % 3

            card = ctk.CTkFrame(
                self.profiles_container, corner_radius=12, fg_color="#2A2D30"
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
                text_color="#A8AFB6",
            ).pack(anchor="w", padx=14)

            ctk.CTkLabel(
                card,
                text=f"{profile.weight} kg -> objectif {profile.target_weight} kg",
                text_color="#A8AFB6",
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
                command=lambda p=profile: self.controlleur.select_profile(p),
            )
            select_button.pack(fill="x", padx=14, pady=(0, 12))
            self.profile_buttons[profile.name] = select_button

    def set_selected_profile(self, profile):
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

    def _validate_int(self, char):
        """Accepte uniquement les chiffres entiers"""
        if char == "":
            return True
        return char.isdigit()

    def _validate_float(self, char):
        """Accepte uniquement les chiffres et virgule/point à la saisie"""
        if char == "":
            return True
        return char.isdigit() or char == "."

    def create_profile(self):
        self.controlleur.create_profile()
        self._render_profiles()
