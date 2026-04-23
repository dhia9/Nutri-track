import customtkinter as ctk


class HomeView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        

        self.titre = ctk.CTkLabel(
            self,
            text="Bienvenue sur NutriTrack",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        self.titre.grid(row=0, column=0, columnspan=3, sticky="w", padx=20)

        self.profil = ctk.CTkLabel(
            self,
            text="Selectionner un profil ou créez-en un nouveau pour commencer",
            font=ctk.CTkFont(size=13),
            text_color="#A8AFB6",
        )
        self.profil.grid(row=1, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 10))

        self.label3 = ctk.CTkLabel(
            self,
            text="Profils existants",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label3.grid(row=2, column=0, columnspan=3, sticky="w", padx=20, pady=(10, 5))

  
        self.label4 = ctk.CTkLabel(
            self,
            text="Créer un nouveau profil",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.label4.grid(row=4, column=0, columnspan=3, sticky="w", padx=20, pady=(300, 10))


        frame_carre_bleu = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E293B")
        frame_carre_bleu.grid(row=5, rowspan=5, column=0, columnspan=3, padx=20, sticky="ew")





        self.nom= ctk.CTkLabel(frame_carre_bleu, text="Prénom et nom")
        self.nom.grid(row=5,column=0,sticky="w",padx=20, pady=(0,10))
        self.nom2= ctk.CTkEntry(frame_carre_bleu)
        self.nom2.grid(row=6,column=0,columnspan= 3 ,sticky="w",padx=20)

        self.age= ctk.CTkLabel(frame_carre_bleu, text="Âge")
        self.age.grid(row=5,column=1,sticky="w",padx=20, pady=(0,10))
        self.age2= ctk.CTkEntry(frame_carre_bleu)
        self.age2.grid(row=6,column=1,sticky="w",padx=20)

        self.taille= ctk.CTkLabel(frame_carre_bleu, text="Taille (cm)")
        self.taille.grid(row=7,column=0,sticky="w",padx=20, pady=(0,10))
        self.taille2= ctk.CTkEntry(frame_carre_bleu)
        self.taille2.grid(row=8,column=0,sticky="w",padx=20)

        self.poids= ctk.CTkLabel(frame_carre_bleu, text="Poids (kg)")
        self.poids.grid(row=7,column=1,sticky="w",padx=20, pady=(0,10))
        self.poids2= ctk.CTkEntry(frame_carre_bleu)
        self.poids2.grid(row=8,column=1,sticky="w",padx=20)

        self.sexe= ctk.CTkLabel(frame_carre_bleu, text="Sexe")
        self.sexe.grid(row=7,column=2,sticky="w",padx=20, pady=(0,10))

        self.sexe_var = ctk.StringVar(value="Homme") 

        self.boutton_sexe1= ctk.CTkRadioButton(frame_carre_bleu,text="Homme",variable=self.sexe_var,value="Homme")
        self.boutton_sexe1.grid(row=8,column=2,sticky="w",padx=20)

        self.boutton_sexe2= ctk.CTkRadioButton(frame_carre_bleu,text="Femme",variable=self.sexe_var,value="Femme")
        self.boutton_sexe2.grid(row=8,column=2,sticky="w",padx=120)



        self.objectif= ctk.CTkLabel(frame_carre_bleu, text="Objectif physique")
        self.objectif.grid(row=9,column=0,sticky="w",padx=20, pady=(0,10))
        self.objectif=ctk.CTkOptionMenu(frame_carre_bleu, values=["Perte de poids", "Maintien du poids", "Prise de poids"])
        self.objectif.grid(row=10,column=0,sticky="w",padx=20, pady=(0,10))

        self.boutton_valider= ctk.CTkButton(frame_carre_bleu, text="Créer le profil")
        self.boutton_valider.grid(row=11,column=2,sticky="w",padx=20, pady=(10,20))
