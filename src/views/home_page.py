import customtkinter as ctk


class HomeView(ctk.CTkFrame):
    def __init__(self):
        super().__init__()
        self.label1=ctk.CTkLabel(self,text='Bienvenue sur NutriTrack 🥗',font=ctk.CTkFont(size=26,weight='bold'))
        self.label1.pack(anchor="w")
        
        self.label2=ctk.CTkLabel(self,text='Sélectionner un profil ou créez-enun nouveau pour commencer',font=ctk.CTkFont(size=20), text_color=C_GRAY)
        self.label2.pack(anchor="w",pady=(4,0))


        self.label3=ctk.CTkLabel(self,text='Profils existants',font=ctk.CTkFont(size=16), weight="bold")
        self.label3.pack(anchor="w", pady=(0, 12))

        self.label4=ctk.CTkLabel(self,text='Créer un nouveau profil',font=ctk.CTkFont(size=16),weight="bold")
        self.label4.pack(anchor="w", padx=30, pady=(0, 15))