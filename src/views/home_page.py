import customtkinter as ctk


class Home_View(ctk.CTkFrame):
    def __init__(self):
        super().__init__()
        self.label1=ctk.CTkLabel(self,text='Bienvenue sur NutriTrack 🥗',font=ctk.CTkFont(size=26,weight='bold'))
        self.label1.pack(anchor="w")
        
        self.label2=ctk.CTkLabel(self,text='Sélectionner un profil ou créez-enun nouveau pour commencer',font=ctk.CTkFont(size=20))
        self.label2.pack(anchor="w")