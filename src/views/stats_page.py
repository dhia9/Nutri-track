import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import math
import matplotlib.dates as mdates

plt.rcParams.update(
    {
        "figure.facecolor": "#1D1F21",
        "axes.facecolor": "#1D1F21",
        "axes.edgecolor": "#2A2D30",
        "axes.labelcolor": "#A8AFB6",
        "xtick.color": "#A8AFB6",
        "ytick.color": "#A8AFB6",
        "grid.color": "#2A2D30",
        "grid.alpha": 0.5,
        "text.color": "#F1F1F1",
        "legend.facecolor": "#1D1F21",
        "legend.edgecolor": "#2A2D30",
    }
)
C_CARD = "#1D1F21"
C_GREEN = "#2DBA7F"
C_ORANGE = "#F59E0B"
C_RED = "#EF4444"
C_BLUE = "#3B82F6"
C_PURPLE = "#8B5CF6"
C_GRAY = "#A8AFB6"
MACRO_PROTEIN_LABEL = "Protéines"
MACRO_CARB_LABEL = "Glucides"
MACRO_FAT_LABEL = "Lipides"
MACRO_LABELS = (MACRO_PROTEIN_LABEL, MACRO_CARB_LABEL, MACRO_FAT_LABEL)


class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, main_controller):
        super().__init__(parent, fg_color="transparent")
        self.main_controller = main_controller
        self.controller = self.main_controller.controllers["Stats"]
        self.controller.view = self
        self.profile = self.controller.get_current_profile()
        self.history = self.controller.generate_history(30)
        self.period = 7
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        self.table_rows = []
        
        

        
        
        

       

        self._build()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        self.profile = self.controller.get_current_profile()
        self.history = self.controller.generate_history(30)
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        self.table_rows = []
        self._build()

    def _create_card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=C_CARD, corner_radius=14)
        card.pack(fill="x", pady=10)
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 5))
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F1F1F1",
        ).pack(anchor="w")
        return card

    def _embed(self, fig, parent):
        fig.patch.set_facecolor("#1D1F21")
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.25)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg="#1D1F21", highlightthickness=0)
        widget.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        plt.close(fig)

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(
            header,
            text="Statistiques nutritionnelles",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(anchor="w")
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)
        self._render_all_charts()

    def _render_all_charts(self):
        data = self.macrosDated
        calories = data["calories"]
        self._bodyanalys()
        self._chart_calories(calories)
        self._caracteristicsChart()
        # self._chart_salt_sugar(data)
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", pady=10)
        self._chart_macros_pie(row)
        self._chart_macros_bar(row)
        
        

    def _chart_calories(self, data):
        card = self._create_card(self.scroll, "Évolution calories")
        fig, ax = plt.subplots(figsize=(8, 3))
        if not data:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée pour les calories",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        else:
            dates = [
                d for d in data.keys()
            ]
            calories = list(data.values())
            ax.plot(dates, calories, color=C_GREEN, linewidth=2.5, label="Calories")
            ax.fill_between(dates, calories, alpha=0.15, color=C_GREEN)
            ax.set_xlabel("Date", labelpad=12)
            ax.set_ylabel("Calories", labelpad=10)
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.25)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
            fig.autofmt_xdate()
        self._embed(fig, card)

    def _chart_macros_pie(self, parent):
        card = self._create_card(parent, "Macros du dernier repas")
        avg_p = self.macrosToday["proteins"]
        avg_c = self.macrosToday["carbohydrate"]
        avg_f = self.macrosToday["fats"]
        values = [
            avg_p if math.isfinite(avg_p) and avg_p > 0 else 0,
            avg_c if math.isfinite(avg_c) and avg_c > 0 else 0,
            avg_f if math.isfinite(avg_f) and avg_f > 0 else 0,
        ]
        fig, ax = plt.subplots(figsize=(4, 4))
        total = sum(values)
        if total > 0:
            ax.pie(
                values,
                colors=[C_PURPLE, C_BLUE, C_ORANGE],
                startangle=90,
                wedgeprops={"edgecolor": "#1D1F21"},
            )
        else:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée pour le dernier repas",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        ax.set_position((0.20, 0.1, 0.6, 0.8))
        fig.tight_layout()
        if total > 0:
            ax.legend(MACRO_LABELS, loc="center left", bbox_to_anchor=(1, 0.5))
        self._embed(fig, card)

    def _chart_macros_bar(self, parent):
        card = self._create_card(parent, "Comparaison pour le dernier repas")
        avg_p = self.macrosToday["proteins"]
        avg_c = self.macrosToday["carbohydrate"]
        avg_f = self.macrosToday["fats"]
        values = [
            avg_p if math.isfinite(avg_p) and avg_p > 0 else 0,
            avg_c if math.isfinite(avg_c) and avg_c > 0 else 0,
            avg_f if math.isfinite(avg_f) and avg_f > 0 else 0,
        ]
        fig, ax = plt.subplots(figsize=(4, 4))
        total = sum(values)
        if total > 0:
            bars = ax.bar([1, 2, 3], values, color=[C_PURPLE, C_BLUE, C_ORANGE])
            ax.set_xticks([])
            ax.set_xlabel("Macronutriments", labelpad=12)
            ax.set_ylabel("Quantité moyenne", labelpad=10)
            ax.legend(bars, MACRO_LABELS)
            ax.grid(True, axis="y", alpha=0.2)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        else:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée pour le dernier repas",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        self._embed(fig, card)

    def _caracteristicsChart(self):
        card = self._create_card(self.scroll, "Évolution macros")
        fig, ax = plt.subplots(figsize=(8, 3))
        if not self.macrosDated["proteins"]:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée pour les macros",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        else:
            dates = [
                d
                for d in self.macrosDated["proteins"].keys()
            ]
            carbohydrate = list(self.macrosDated["proteins"].values())
            proteins = list(self.macrosDated["proteins"].values())
            fats = list(self.macrosDated["fats"].values())
            ax.plot(
                dates, carbohydrate, color="green", linewidth=2.5, label="carbohydrate"
            )
            ax.fill_between(dates, carbohydrate, alpha=0.1, color="green")
            ax.plot(
                dates, proteins, color="blue", linewidth=2.5, label=MACRO_PROTEIN_LABEL
            )
            ax.plot(dates, fats, color="red", linewidth=2.5, label=MACRO_FAT_LABEL)
            ax.set_xlabel("Date", labelpad=12)
            ax.set_ylabel("Valeurs", labelpad=10)
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.25)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
            fig.autofmt_xdate()
        self._embed(fig, card)

       
    def _bodyanalys(self):
        
        # création de la card 
        card = self._create_card(self.scroll, "Mesures corporelles")

        # Ajout d'une frame sur la meme ligne 
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=10)

        # Ajout de la date
        date_frame = ctk.CTkFrame(top_row, fg_color="#000000", corner_radius=10)
        date_frame.pack(side="right")

        self.button_previous = ctk.CTkButton(
            date_frame,
            text="◀",
            width=30,
            fg_color="#000000",
            font=ctk.CTkFont(size=14),
            hover_color="#F1F1F1",
            corner_radius=10,
        )
        self.button_previous.pack(side="left", padx=6, pady=4)
        self.button_previous.bind("<Button-1>", self.controller.previous_day)
        

        self.date_label = ctk.CTkLabel(date_frame,text=self.controller.current_date.strftime("  %A %d %B %Y  ").capitalize(),font=ctk.CTkFont(size=13, weight="bold"),corner_radius=10,)
        self.date_label.pack(side="left", padx=18, pady = 4)

        self.button_next = ctk.CTkButton(date_frame,text="▶",width=30,fg_color="#0F0A0A",font=ctk.CTkFont(size=14),hover_color="#F1F1F1",corner_radius=10,)
        self.button_next.pack(side="left", padx=6, pady=4)


        
        #Boutton ajouter
        boutton_ajouter = ctk.CTkButton(top_row, text="Ajouter une mesure corporelle")
        boutton_ajouter.pack(side="left")
        boutton_ajouter.bind("<Button-1>", self.ajouter_mesure)




        
        #Frame pour les labels 
        labels_frame = ctk.CTkFrame(card, fg_color="transparent")
        labels_frame.pack(fill="x", padx=15, pady=(10,0))

        poids_label = ctk.CTkLabel(labels_frame, text="Poids en kg")
        poids_label.pack(side="left", expand=True)

        taille_label = ctk.CTkLabel(labels_frame, text="Tour de taille en cm")
        taille_label.pack(side="left", expand=True)

        bras_label = ctk.CTkLabel(labels_frame, text="Tour de bras en cm")
        bras_label.pack(side="left", expand=True)

        graisse_label = ctk.CTkLabel(labels_frame, text="Masse grasse en %")
        graisse_label.pack(side="left", expand=True)




        # Frame pour les entries 
        entries_frame = ctk.CTkFrame(card, fg_color="transparent")
        entries_frame = ctk.CTkFrame(card, fg_color="transparent")
        entries_frame.pack(fill="x", padx=15, pady=(5,15))

        self.poids_entry = ctk.CTkEntry(entries_frame, placeholder_text="Poids en kg")
        self.poids_entry.pack(side="left", expand=True, padx=5)

        self.taille_entry = ctk.CTkEntry(entries_frame, placeholder_text="Tour de taille en cm")
        self.taille_entry.pack(side="left", expand=True, padx=5)

        self.bras_entry = ctk.CTkEntry(entries_frame, placeholder_text="Tour de bras en cm")
        self.bras_entry.pack(side="left", expand=True, padx=5)

        self.graisse_entry = ctk.CTkEntry(entries_frame, placeholder_text="Masse grasse en %")
        self.graisse_entry.pack(side="left", expand=True, padx=5)

        # Label historique 
        ctk.CTkLabel(
            card,
            text="Historique des mesures corporelles",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F1F1F1",
        ).pack(anchor="w")

        # Tableau de l'historique 
        self.tableau_frame = ctk.CTkFrame(card, fg_color="#000000", corner_radius=10)
        self.tableau_frame.pack(fill="x", padx=15, pady=10)
        self.ligne_tableau = 1
        headers = ["Date", "Poids (kg)", "Tour de taille (cm)", "Tour de bras (cm)", "Masse grasse (%)"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.tableau_frame, text= header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=col, padx=35, pady=5)
        
        # Charger et afficher les mesures existantes depuis le profil
        mesures_existantes = self.controller.get_mesures_corporelles()
        # Afficher les mesures en ordre inverse (plus récentes en haut)
        for mesure in reversed(mesures_existantes):
            self.ajouter_ligne_mesure(mesure)
        

       

    
    def ajouter_mesure(self,event):
        mesure = {
            "date": self.controller.current_date.strftime("%Y-%m-%d"),
            "poids": self.poids_entry.get(),
            "taille": self.taille_entry.get(),
            "bras": self.bras_entry.get(),
            "graisse": self.graisse_entry.get()
        }


        self.controller.ajouter_mesure(mesure)
        self.ajouter_ligne_mesure(mesure)


    def ajouter_ligne_mesure(self,mesure):
        values = [mesure["date"], mesure["poids"], mesure["taille"], mesure["bras"], mesure["graisse"]]
        # Descendre toutes les anciennes lignes
        for row in self.table_rows:
            for widget in row:
                current_info = widget.grid_info()
                widget.grid_configure(row=current_info["row"] + 1)

        # Nouvelle ligne en haut
        row_widget = []
        for col, value in enumerate(values):
            label = ctk.CTkLabel(self.tableau_frame,text=value)
            label.grid(row=1,column=col,padx=35,pady=5)
            row_widget.append(label)
        self.table_rows.insert(0, row_widget)

        if len(self.table_rows) >10 :
            for widget in self.table_rows[-1]:
                widget.destroy()
            self.table_rows.pop()