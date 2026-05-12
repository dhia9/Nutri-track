import customtkinter as ctk

from datetime import datetime, timedelta

from distributed import progress
from flask import app

class NutritionView(ctk.CTkFrame):
    def __init__(self, parent, controller=None): 
        super().__init__(parent)
        self.controller = controller
        self.current_date = datetime.now()
        
        #self.profile = controller.current_profile
        #self.menu = controller.current_menu                a voir comment c'est appeler dans le main controller
        
        
        
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        
        self.grid_rowconfigure(0, weight=0)

        self.title = ctk.CTkLabel(self,text="🍽️Gestion nutritionnelle", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.grid(row=0, column=0, columnspan=3, sticky="w", padx=20)

        self.tiltle2 = ctk.CTkLabel(self,text="Profil : ", font=ctk.CTkFont(size=13), text_color="#A8AFB6")
        self.tiltle2.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(50,0))


        self.frame_carre_noir1 = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_carre_noir1.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        
        for i in range(10):
            self.frame_carre_noir1.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir1.grid_rowconfigure(i, weight=1)
        
        self.frame_carre_noir2 = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_carre_noir2.grid(row=2, column=2, columnspan=3, padx=10, pady=20, sticky="ew")

        for i in range(10):
            self.frame_carre_noir2.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir2.grid_rowconfigure(i, weight=1)

        self.frame_carre_noir3 = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_carre_noir3.grid(row=2, column=5, columnspan=3, padx=10, pady=20, sticky="ew")   

        for i in range(10):
            self.frame_carre_noir3.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir3.grid_rowconfigure(i, weight=1)   

        self.frame_carre_noir4 = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_carre_noir4.grid(row=2, column=8, columnspan=2, padx=10, pady=20, sticky="ew")      

        for i in range(10): 
            self.frame_carre_noir4.grid_columnconfigure(i, weight=1)
            self.frame_carre_noir4.grid_rowconfigure(i, weight=1)

        self.calories_label = ctk.CTkLabel(self.frame_carre_noir1, text="Calories", font=ctk.CTkFont(size=13))
        self.calories_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10,0))

        self.proteines_label = ctk.CTkLabel(self.frame_carre_noir2, text="Protéines", font=ctk.CTkFont(size=13))
        self.proteines_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10,0))

        self.glucides_label = ctk.CTkLabel(self.frame_carre_noir3, text="Glucides", font=ctk.CTkFont(size=13))
        self.glucides_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10,0))

        self.lipides_label = ctk.CTkLabel(self.frame_carre_noir4, text="Lipides", font=ctk.CTkFont(size=13))
        self.lipides_label.grid(row=0, column=0, sticky="w",padx=15, pady=(10,0))   

        
        
        
        
        date_frame = ctk.CTkFrame(self, fg_color="#000000", corner_radius=10)
        date_frame.grid(row=0, column=8, sticky="w", padx=10, pady=5)

        self.button_previous=ctk.CTkButton(date_frame, text="◀", width=30, fg_color="#000000",
                        font=ctk.CTkFont(size=14), hover_color="#F1F1F1",corner_radius=10)
        self.button_previous.grid(row=0, column=0, padx=4)
        
        self.button_previous.bind("<Button-1>", self.previous_day)  
        
        self.date_label = ctk.CTkLabel(
            date_frame,
            text=datetime.now().strftime("  %A %d %B %Y  ").capitalize(),
            font=ctk.CTkFont(size=13, weight="bold"),corner_radius=10
        )
        self.date_label.grid(row=0, column=1, padx=4)
        
        self.button_next=ctk.CTkButton(date_frame, text="▶", width=30, fg_color="#0F0A0A",
                      font=ctk.CTkFont(size=14), hover_color="#F1F1F1",corner_radius=10) 
        self.button_next.grid(row=0, column=2, padx=4)
        self.button_next.bind("<Button-1>", self.next_day)

        self.frame_ajout = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_ajout.grid(row=5, column=0, columnspan=3, rowspan= 10, padx=10, pady=20, sticky="ew")
        
        self.bouton_aliment=ctk.CTkButton(self.frame_ajout, text="✚ Ajouter un aliment ", font=ctk.CTkFont(size=18, weight="bold"), text_color="#A8AFB6")
        self.bouton_aliment.grid(row=0, column=0, sticky="w", padx=15, pady=(10,0))

        self.frame_aliment = ctk.CTkFrame(self, corner_radius=15, fg_color="#35393D")
        self.frame_aliment.grid(row=5, column=3, columnspan=10, rowspan= 10, padx=10, pady=20, sticky="ew")

        self.menu=ctk.CTkLabel(self.frame_aliment, text="📋 Aliments du jour", font=ctk.CTkFont(size=18, weight="bold"), text_color="#A8AFB6")
        self.menu.grid(row=0, column=0, sticky="w", padx=15, pady=(10,0))

        self.progress_calories= ctk.CTkProgressBar(
        self.frame_carre_noir1,
        width=300,
        height=10,
        corner_radius=5,
        progress_color="#4CAF50",   
        fg_color="#2A2A4A"          
        )
        self.progress_calories.grid(row=1, column=0, sticky="ew", padx=15, pady=(10,0))

        self.progress_protéine= ctk.CTkProgressBar(
        self.frame_carre_noir2,
        width=300,
        height=10,
        corner_radius=5,
        progress_color="#4CAF50",   
        fg_color="#2A2A4A"          
        )
        self.progress_protéine.grid(row=1, column=0, sticky="ew", padx=15, pady=(10,0))

        self.progress_glucides= ctk.CTkProgressBar(
        self.frame_carre_noir3,
        width=300,
        height=10,
        corner_radius=5,
        progress_color="#4CAF50",   
        fg_color="#2A2A4A"          
        )
        self.progress_glucides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10,0))

        self.progress_lipides= ctk.CTkProgressBar(
        self.frame_carre_noir4,
        width=300,
        height=10,
        corner_radius=5,
        progress_color="#4CAF50",   
        fg_color="#2A2A4A"          
        )
        self.progress_lipides.grid(row=1, column=0, sticky="ew", padx=15, pady=(10,0))

        













    def update_date(self):
        #Mettre a jour sur la vue la date affiché dans le label
        self.date_label.configure(text=self.current_date.strftime("  %A %d %B %Y  ").capitalize())


    def previous_day(self,event):
        #Mettre a jour la date en mettant la date d'avant et ensuite mettre a jour le label
        self.current_date -=timedelta(days=1)
        self.update_date()

    def next_day(self,event):
        #Mettre a jour la date en mettant la date d'après et ensuite mettre a jour le label
        self.current_date +=timedelta(days=1)
        self.update_date()




        

        




