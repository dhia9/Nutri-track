import customtkinter as ctk
import src.controllers.main_controller as main_controller


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, main_controller: main_controller.MainController = None):
        super().__init__(parent)
        self.main_controller = main_controller  # initialiser le contrôleur principal pour pouvoir accéder à ses méthodes et données
        self.main_controller.controllers["Home"].view = (
            self  # Assigner la vue au contrôleur de la page d'accueil pour qu'il puisse interagir avec les éléments de la page
        )
        self.controlleur = self.main_controller.controllers[
            "Home"
        ]  # Stocker une référence directe au contrôleur de la page d'accueil pour faciliter son utilisation dans les méthodes de la vue

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
            text="Selectionner un profil ou créez-en un nouveau pour commencer",
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

        self.label4 = ctk.CTkLabel(
            self,
            text="Créer un nouveau profil",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label4.grid(
            row=4, column=0, columnspan=3, sticky="w", padx=20, pady=(300, 10)
        )

        frame_carre_noir = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        frame_carre_noir.grid(
            row=5, rowspan=5, column=0, columnspan=3, padx=20, sticky="ew"
        )

        self.nom = ctk.CTkLabel(frame_carre_noir, text="Prénom et nom")
        self.nom.grid(row=5, column=0, sticky="w", padx=20, pady=(0, 10))
        self.nom_entry = ctk.CTkEntry(frame_carre_noir)
        self.nom_entry.grid(row=6, column=0, columnspan=3, sticky="w", padx=20)

        self.age_label = ctk.CTkLabel(frame_carre_noir, text="Âge")
        self.age_label.grid(row=5, column=1, sticky="w", padx=20, pady=(0, 10))
        self.age_entry = ctk.CTkEntry(frame_carre_noir)
        self.age_entry.grid(row=6, column=1, sticky="w", padx=20)

        self.taille_label = ctk.CTkLabel(frame_carre_noir, text="Taille (cm)")
        self.taille_label.grid(row=7, column=0, sticky="w", padx=20, pady=(0, 10))
        self.taille_entry = ctk.CTkEntry(frame_carre_noir)
        self.taille_entry.grid(row=8, column=0, sticky="w", padx=20)

        self.poids_label = ctk.CTkLabel(frame_carre_noir, text="Poids (kg)")
        self.poids_label.grid(row=7, column=1, sticky="w", padx=20, pady=(0, 10))
        self.poids_entry = ctk.CTkEntry(frame_carre_noir)
        self.poids_entry.grid(row=8, column=1, sticky="w", padx=20)

        self.sexe_label = ctk.CTkLabel(frame_carre_noir, text="Sexe")
        self.sexe_label.grid(row=7, column=2, sticky="w", padx=20, pady=(0, 10))

        self.sexe_var = ctk.StringVar(value="Homme")

        self.boutton_sexe1 = ctk.CTkRadioButton(
            frame_carre_noir, text="Homme", variable=self.sexe_var, value="Homme"
        )
        self.boutton_sexe1.grid(row=8, column=2, sticky="w", padx=20)

        self.boutton_sexe2 = ctk.CTkRadioButton(
            frame_carre_noir, text="Femme", variable=self.sexe_var, value="Femme"
        )
        self.boutton_sexe2.grid(row=8, column=2, sticky="w", padx=120)

        self.objectif_label = ctk.CTkLabel(
            frame_carre_noir, text="Objectif poids (kg)"
        )
        self.objectif_label.grid(row=9, column=0, sticky="w", padx=20, pady=(0, 10))

        self.objectif_var = ctk.StringVar()

        vcmd = (self.register(self._validate_float), "%S")
        self.objectif_Entry = ctk.CTkEntry(
            frame_carre_noir,
            textvariable=self.objectif_var,
            placeholder_text="Objectif de Poids",
            validate="key",
            validatecommand=vcmd,
        )
        self.objectif_Entry.grid(row=10, column=0, sticky="w", padx=20, pady=(0, 10))

        self.boutton_valider = ctk.CTkButton(frame_carre_noir, text="Créer le profil")
        self.boutton_valider.grid(row=11, column=2, sticky="w", padx=20, pady=(10, 20))

    def _validate_float(self, char):
        """Accepte uniquement les chiffres et virgule/point à la saisie"""
        if char == "":
            return True
        return char.isdigit() or char in ",."
