import customtkinter as ctk

class NutritionView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)


        self.title = ctk.CTkLabel(self,text="Gestion nutritionnelle", font=ctk.CTkFont(size=26, weight="bold"))
        self.title.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(10,0))

        self.tiltle2 = ctk.CTkLabel(self,text="Profil : ", font=ctk.CTkFont(size=13), text_color="#A8AFB6")
        self.tiltle2.grid(row=1, column=0, columnspan=3, sticky="w", padx=20)


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
        self.lipides_label.grid(row=0, column=0, sticky="w",    padx=15, pady=(10,0))   

        

        

        




