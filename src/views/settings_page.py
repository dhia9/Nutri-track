import customtkinter as ctk
import src.controllers.main_controller as main_controller
import src.views.home_page as home_page
import src.controllers.settings_controller as settings_controller


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, main_controller):
        super().__init__(parent)

        self.main_controller = main_controller
        self.main_controller.controllers["Settings"].view = self
        # ajout du controleur de la page
        self.controlleur = self.main_controller.controllers["Settings"]
        self.profile = self.main_controller.current_profile

        # Configuration des 5 colonnes
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        # Configuration des 10 lignes
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

        # ===== TITRE =====
        self.titre = ctk.CTkLabel(
            self, text="Paramètres", font=ctk.CTkFont(size=26, weight="bold")
        )

        self.titre.grid(
            row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 0)
        )

        # ===== SECTION PROFIL =====
        self.label4 = ctk.CTkLabel(
            self,
            text="Gestion du profil sélectionné :",
            font=ctk.CTkFont(size=16, weight="bold"),
        )

        self.label4.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=10)

        # ===== GRAND CADRE GAUCHE =====
        self.frame_carre_noir = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")

        self.frame_carre_noir.grid(
            row=2, rowspan=5, column=0, columnspan=2, padx=20, sticky="nsew"
        )

        if self.profile is not None:
            self.label_nom = ctk.CTkLabel(self.frame_carre_noir, text="Nom du profil")
            self.label_nom.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
            self.nom_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"{self.profile.name}"
            )
            self.nom_entry.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_age = ctk.CTkLabel(self.frame_carre_noir, text="Âge")
            self.label_age.grid(row=2, column=0, sticky="w", padx=20, pady=(16, 10))
            self.age_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"{self.profile.age}"
            )
            self.age_entry.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_taille = ctk.CTkLabel(self.frame_carre_noir, text="Taille (cm)")
            self.label_taille.grid(row=4, column=0, sticky="w", padx=20, pady=(16, 10))
            self.taille_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"{self.profile.height}"
            )
            self.taille_entry.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_poids = ctk.CTkLabel(self.frame_carre_noir, text="Poids (kg)")
            self.label_poids.grid(row=6, column=0, sticky="w", padx=20, pady=(16, 10))
            self.poids_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"{self.profile.weight}"
            )
            self.poids_entry.grid(row=7, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_objectif = ctk.CTkLabel(
                self.frame_carre_noir, text="Objectif (kg)"
            )
            self.label_objectif.grid(
                row=3, column=1, sticky="w", padx=20, pady=(16, 10)
            )
            self.objectif_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"{self.profile.target_weight}"
            )
            self.objectif_entry.grid(row=4, column=1, sticky="w", padx=20, pady=(0, 10))

        else:
            self.label_nom = ctk.CTkLabel(self.frame_carre_noir, text="Nom du profil")
            self.label_nom.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
            self.nom_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"Aucun profil sélectionné"
            )
            self.nom_entry.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_age = ctk.CTkLabel(self.frame_carre_noir, text="Âge")
            self.label_age.grid(row=2, column=0, sticky="w", padx=20, pady=(16, 10))
            self.age_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"Aucun profil sélectionné"
            )
            self.age_entry.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_taille = ctk.CTkLabel(self.frame_carre_noir, text="Taille (cm)")
            self.label_taille.grid(row=4, column=0, sticky="w", padx=20, pady=(16, 10))
            self.taille_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"Aucun profil sélectionné"
            )
            self.taille_entry.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_poids = ctk.CTkLabel(self.frame_carre_noir, text="Poids (kg)")
            self.label_poids.grid(row=6, column=0, sticky="w", padx=20, pady=(16, 10))
            self.poids_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"Aucun profil sélectionné"
            )
            self.poids_entry.grid(row=7, column=0, sticky="w", padx=20, pady=(0, 10))

            self.label_objectif = ctk.CTkLabel(
                self.frame_carre_noir, text="Objectif (kg)"
            )
            self.label_objectif.grid(
                row=3, column=1, sticky="w", padx=20, pady=(16, 10)
            )
            self.objectif_entry = ctk.CTkEntry(
                self.frame_carre_noir, placeholder_text=f"Aucun profil sélectionné"
            )
            self.objectif_entry.grid(row=4, column=1, sticky="w", padx=20, pady=(0, 10))

        self.label_sexe = ctk.CTkLabel(self.frame_carre_noir, text="Sexe")
        self.label_sexe.grid(row=0, column=1, sticky="w", padx=20, pady=(16, 10))
        self.sexe_var = ctk.StringVar(value="Homme")
        self.boutton_sexe1 = ctk.CTkRadioButton(
            self.frame_carre_noir, text="Homme", variable=self.sexe_var, value="Homme"
        )
        self.boutton_sexe1.grid(row=1, column=1, sticky="w", padx=20, pady=(0, 10))
        self.boutton_sexe2 = ctk.CTkRadioButton(
            self.frame_carre_noir, text="Femme", variable=self.sexe_var, value="Femme"
        )
        self.boutton_sexe2.grid(row=2, column=1, sticky="w", padx=20, pady=(0, 10))

        # Bouton modifier ke profil
        self.boutton_modifier = ctk.CTkButton(
            self.frame_carre_noir, text="Modifier le profil", command=self.edit_profile
        )
        self.boutton_modifier.grid(
            row=12, column=0, sticky="ew", padx=20, pady=(16, 20)
        )

        # Bouton supprimer le profil
        self.boutton_supprimer = ctk.CTkButton(
            self.frame_carre_noir,
            text="Supprimer le profil",
            bg_color="red",
            hover_color="#ff4d4d",
            command=self.delete_profile,
        )
        self.boutton_supprimer.grid(
            row=12, column=1, sticky="w", padx=20, pady=(16, 20)
        )

        # ===== GRAND CADRE DROIT =====
        self.frame_carre_noir2 = ctk.CTkFrame(
            self, corner_radius=15, fg_color="#35393D"
        )

        self.frame_carre_noir2.grid(
            row=2, rowspan=5, column=2, columnspan=3, padx=20, sticky="nsew"
        )

        self.label5 = ctk.CTkLabel(
            self,
            text="Préférences d'affichage :",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label5.grid(row=1, column=2, sticky="w", padx=20, pady=(20, 10))

        self.mode_app_label = ctk.CTkLabel(
            self.frame_carre_noir2,
            text="Mode d'affichage de l'application :",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.mode_app_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        self.mode_var = ctk.StringVar(value="dark")
        self.boutton_mode = ctk.CTkRadioButton(
            self.frame_carre_noir2,
            text="Clair",
            variable=self.mode_var,
            value="light",
            command=self.change_mode,
        )
        self.boutton_mode.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))
        self.boutton_mode2 = ctk.CTkRadioButton(
            self.frame_carre_noir2,
            text="Sombre",
            variable=self.mode_var,
            value="dark",
            command=self.change_mode,
        )
        self.boutton_mode2.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        self.theme_label = ctk.CTkLabel(
            self.frame_carre_noir2,
            text="Thème de l'application :",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.theme_label.grid(row=8, column=0, sticky="w", padx=20, pady=(16, 10))
        self.theme_var = ctk.StringVar(value="green")
        self.boutton_theme1 = ctk.CTkRadioButton(
            self.frame_carre_noir2, text="Bleu", variable=self.theme_var, value="blue"
        )
        self.boutton_theme1.grid(row=9, column=0, sticky="w", padx=20, pady=(0, 10))
        self.boutton_theme2 = ctk.CTkRadioButton(
            self.frame_carre_noir2, text="Rouge", variable=self.theme_var, value="red"
        )
        self.boutton_theme2.grid(row=10, column=0, sticky="w", padx=20, pady=(0, 10))
        self.boutton_theme3 = ctk.CTkRadioButton(
            self.frame_carre_noir2, text="Vert", variable=self.theme_var, value="green"
        )
        self.boutton_theme3.grid(row=11, column=0, sticky="w ", padx=20, pady=(0, 10))
        self.boutton_theme4 = ctk.CTkRadioButton(
            self.frame_carre_noir2,
            text="Jaune",
            variable=self.theme_var,
            value="yellow",
        )
        self.boutton_theme4.grid(row=12, column=0, sticky="w ", padx=20, pady=(0, 10))
        self.boutton_theme5 = ctk.CTkRadioButton(
            self.frame_carre_noir2, text="Rose", variable=self.theme_var, value="pink"
        )
        self.boutton_theme5.grid(row=13, column=0, sticky="w ", padx=20, pady=(0, 10))

    def edit_profile(self):

        name = self.nom_entry.get()
        if name == "":
            name = self.profile.name
        age = self.age_entry.get()
        if age == "":
            age = self.profile.age

        height = self.taille_entry.get()
        if height == "":
            height = self.profile.height

        weight = self.poids_entry.get()
        if weight == "":
            weight = self.profile.weight

        target_weight = self.objectif_entry.get()
        if target_weight == "":
            target_weight = self.profile.target_weight

        sex = self.sexe_var.get()

        self.controlleur.edit_profile(name, age, height, weight, target_weight, sex)

        self.nom_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.taille_entry.delete(0, "end")
        self.poids_entry.delete(0, "end")
        self.objectif_entry.delete(0, "end")

    def delete_profile(self):
        self.controlleur.delete_profile()
        self.nom_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.taille_entry.delete(0, "end")
        self.poids_entry.delete(0, "end")
        self.objectif_entry.delete(0, "end")

    def update_profile_details(self, profile):
        self.profile = profile

        self.nom_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.taille_entry.delete(0, "end")
        self.poids_entry.delete(0, "end")
        self.objectif_entry.delete(0, "end")

        if self.profile is not None:
            self.nom_entry.configure(placeholder_text=f"{self.profile.name}")
            self.age_entry.configure(placeholder_text=f"{self.profile.age}")
            self.taille_entry.configure(placeholder_text=f"{self.profile.height}")
            self.poids_entry.configure(placeholder_text=f"{self.profile.weight}")
            self.objectif_entry.configure(
                placeholder_text=f"{self.profile.target_weight}"
            )
            self.sexe_var.set(self.profile.sex)
        else:
            self.nom_entry.configure(placeholder_text="Aucun profil sélectionné")
            self.age_entry.configure(placeholder_text="Aucun profil sélectionné")
            self.taille_entry.configure(placeholder_text="Aucun profil sélectionné")
            self.poids_entry.configure(placeholder_text="Aucun profil sélectionné")
            self.objectif_entry.configure(placeholder_text="Aucun profil sélectionné")
            self.sexe_var.set("Homme")

    def change_mode(self):
        mode = self.mode_var.get()
        ctk.set_appearance_mode(mode)

    def change_theme(self):
        theme = self.theme_var.get()
