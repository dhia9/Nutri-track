import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import math
import matplotlib.dates as mdates
from src.models.mesures_corporelles import MesuresCorporelles
from dateutil import parser

# Constantes pour les couleurs des macros
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
        self.period = 7
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        # attribut utile pour le tableau
        self.table_rows = []
        # Récupérer les couleurs du thème
        self.theme_colors = self.main_controller.theme_colors
        self.update_matplotlib_colors()
        # attributs utiles pour refresh les graphs 
        self.calories_canvas = None
        self.calories_widget = None
        self.macro_canvas = None
        self.macro_widget = None
        self.corpo_canvas = None
        self.corpo_widget = None
        self.corpo_card = None
        self._build()

    def update_matplotlib_colors(self):
        """
        Met à jour les couleurs matplotlib selon le thème actuel.

        Returns:
            None"""
        bg_color = self.theme_colors.get("bg", "#1D1F21")
        content_color = self.theme_colors.get("content", "#17191B")
        frame_color = self.theme_colors.get("frame", "#2A2D30")
        text_color = self.theme_colors.get("text", "#F1F1F1")
        text_secondary = self.theme_colors.get("text_secondary", "#A8AFB6")

        plt.rcParams.update(
            {
                "figure.facecolor": bg_color,
                "axes.facecolor": bg_color,
                "axes.edgecolor": frame_color,
                "axes.labelcolor": text_secondary,
                "xtick.color": text_secondary,
                "ytick.color": text_secondary,
                "grid.color": frame_color,
                "grid.alpha": 0.5,
                "text.color": text_color,
                "legend.facecolor": bg_color,
                "legend.edgecolor": frame_color,
            }
        )

    def refresh(self):
        """Rafraîchit l'affichage des statistiques avec les données actuelles.

        Detruit et recrée tous les graphiques et éléments de l'interface.

        Returns:
            None
        """
        for child in self.winfo_children():
            child.destroy()

        self.profile = self.controller.get_current_profile()
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        self.table_rows = []

        # Mettre à jour les couleurs du thème
        self.theme_colors = self.main_controller.theme_colors
        self.update_matplotlib_colors()

        self._build()

    def _create_card(self, parent, title, center_title=False, buttons=None):
        """Crée une carte pour afficher un graphique.

        Args:
            parent: Widget parent où ajouter la carte.
            title: Titre de la carte.

        Returns:
            Un frame CTkFrame formatté comme carte.
        """
        card = ctk.CTkFrame(
            parent, fg_color=self.theme_colors.get("frame", "#2A2D30"), corner_radius=14
        )
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 5))
        label_title = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_colors.get("text", "#F1F1F1"),
        )
        if not center_title:
            label_title.pack(side="left")
        else:
            label_title.pack(anchor="center")
        # Partie droite : boutons
        if buttons:
            buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
            buttons_frame.pack(side="right")

            for btn in buttons:
                button = ctk.CTkButton(
                    buttons_frame,
                    text=btn["text"],
                    width=32,
                    height=32,
                    corner_radius=10,
                    text_color=self.main_controller.theme_colors["text"],
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=self.main_controller.settings.theme,
                    hover_color=self.main_controller.darken_color(
                        self.main_controller.settings.theme
                    ),
                    command=btn["command"],
                )
                button.pack(side="left", padx=4)
        return card

    def _embed(self, fig, parent):
        """Insère un graphique matplotlib dans un widget tkinter.

        Args:
            fig: La figure matplotlib à insérer.
            parent: Le widget parent où ajouter le graphique.

        Returns:
            Le widget canvas contenant le graphique.
        """
        bg_color = self.theme_colors.get("bg", "#1D1F21")
        fig.patch.set_facecolor(bg_color)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.25)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg=bg_color, highlightthickness=0)
        widget.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        plt.close(fig)

        return canvas, widget

    def _build(self):
        """Construit l'interface des statistiques en format dashboard.

        Crée l'entête et une grille de graphiques pour optimiser l'espace.

        Returns:
            None

        """
        # Entête
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(
            header,
            text="Statistiques nutritionnelles",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(anchor="w")

        # Frame principal avec scrollbar
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)

        # Grille principale pour le layout du dashboard
        self.dashboard_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.dashboard_grid.pack(fill="both", expand=True)

        self._render_all_charts()

    def _render_all_charts(self):
        """Affiche tous les graphiques en format dashboard.

        Crée et affiche les graphiques de calories, caractéristiques,
        et macros (pie et bar).

        Returns:
            None
        Layout:
        - Row 0: Mesures corporelles (pleine largeur)
        - Row 1: Calories (60%), Pie chart (40%)
        - Row 2: Bar chart (40%), Évolution macros (60%)
        - Row 3: Historique des mesures (pleine largeur)
        """
        # Configure les colonnes pour avoir des proportions
        self.dashboard_grid.columnconfigure(0, weight=3)
        self.dashboard_grid.columnconfigure(1, weight=2)
        self.dashboard_grid.rowconfigure(0, weight=0)
        self.dashboard_grid.rowconfigure(1, weight=1)
        self.dashboard_grid.rowconfigure(2, weight=1)
        self.dashboard_grid.rowconfigure(3, weight=1)

        # Row 0: Mesures corporelles (pleine largeur)
        self._bodyanalys_compact(self.dashboard_grid, row=0)

        # Row 1: Calories et Pie chart
        self._chart_calories_grid(self.dashboard_grid, row=2, col=0)
        self._chart_macros_pie_grid(self.dashboard_grid, row=2, col=1)

        # Row 2: Bar chart et Évolution macros
        self._chart_macros_bar_grid(self.dashboard_grid, row=3, col=1)
        self._caracteristicsChart_grid(self.dashboard_grid, row=3, col=0)

        # Row 3 : Evolution mesures corporelles
        self._chart_mesure_corpo_grid(self.dashboard_grid, row=1)

    def _chart_calories_grid(self, parent, row, col):
        """Crée un graphique d'évolution des calories en grille.

        Args:
            parent: Widget parent (grille).
            row: Numéro de ligne dans la grille.
            col: Numéro de colonne dans la grille.
        """
        data = self.macrosDated["calories"]
        card = self._create_card(
            parent,
            "Évolution calories",
            buttons=[
                {
                    "text": "Tout",
                    "command": lambda: self.controller.change_period(None, "calor"),
                },
                {
                    "text": "30 derniers",
                    "command": lambda: self.controller.change_period(30, "calor"),
                },
                {
                    "text": "7 derniers",
                    "command": lambda: self.controller.change_period(7, "calor"),
                },
            ],
        )
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        self.calories_card = card

        self._draw_calories_chart(card, data)

    def _draw_calories_chart(self, card, data):
        fig, ax = plt.subplots(figsize=(6, 2.5))
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
            dates = sorted(data.keys())
            calories = [data[d] for d in dates]
            duree = self.controller.duree["calor"]
            if duree:
                dates = dates[-duree:]
                calories = calories[-duree:]

            ax.plot(dates, calories, color=C_GREEN, linewidth=2.5, label="Calories")
            ax.fill_between(dates, calories, alpha=0.15, color=C_GREEN)
            ax.set_xlabel("Date", labelpad=7, fontsize=9)
            ax.set_ylabel("Calories", labelpad=10, fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True, linestyle="--", alpha=0.25)
            ax.spines["top"].set_visible(False) # rendre bordure haut non visible
            ax.spines["right"].set_visible(False)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
            fig.autofmt_xdate(rotation=45)#rotation de l'axe date pour eviter chevauchement
            ax.tick_params(labelsize=8)#taille de police des valeurs et les titres des axes
        self.calories_canvas, self.calories_widget = self._embed(fig, card)

    def _chart_macros_pie_grid(self, parent, row, col):
        """Crée un graphique en camembert des macros du dernier repas en grille.

        Args:
            parent: Widget parent (grille).
            row: Numéro de ligne dans la grille.
            col: Numéro de colonne dans la grille.
        """
        card = self._create_card(parent, "Macros du dernier repas")
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        proteins = self.macrosToday["proteins"]
        carbohydrate = self.macrosToday["carbohydrate"]
        fats = self.macrosToday["fats"]
        values = [
            proteins if math.isfinite(proteins) and proteins > 0 else 0,
            carbohydrate if math.isfinite(carbohydrate) and carbohydrate > 0 else 0,
            fats if math.isfinite(fats) and fats > 0 else 0,
        ]
        fig, ax = plt.subplots(figsize=(4, 2.5))
        total = sum(values)
        if total > 0:
            ax.pie(
                values,
                colors=[C_PURPLE, C_BLUE, C_ORANGE],
                startangle=90,
                wedgeprops={"edgecolor": "#1D1F21"},
                textprops={"fontsize": 8},
            )
        else:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        ax.set_position((0.15, 0.1, 0.7, 0.8))
        fig.tight_layout()#margin
        if total > 0:
            ax.legend(
                MACRO_LABELS, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8
            )
        self._embed(fig, card)

    def _chart_macros_bar_grid(self, parent, row, col):
        """Crée un graphique en barres pour comparer les macros du dernier repas en grille.

        Args:
            parent: Widget parent (grille).
            row: Numéro de ligne dans la grille.
            col: Numéro de colonne dans la grille.
        """
        card = self._create_card(parent, "Comparaison du dernier repas")
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        proteins = self.macrosToday["proteins"]
        carbohydrate = self.macrosToday["carbohydrate"]
        fats = self.macrosToday["fats"]
        values = [
            proteins if math.isfinite(proteins) and proteins > 0 else 0,
            carbohydrate if math.isfinite(carbohydrate) and carbohydrate > 0 else 0,
            fats if math.isfinite(fats) and fats > 0 else 0,
        ]
        fig, ax = plt.subplots(figsize=(4, 2.5))
        total = sum(values)
        if total > 0:
            bars = ax.bar([1, 2, 3], values, color=[C_PURPLE, C_BLUE, C_ORANGE])
            ax.set_xticks([])
            ax.set_xlabel("Macronutriments", labelpad=10, fontsize=9)
            ax.set_ylabel("Quantité (g)", labelpad=10, fontsize=9)
            ax.legend(bars, MACRO_LABELS, fontsize=8)
            ax.grid(True, axis="y", alpha=0.2)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        else:
            ax.text(
                0.5,
                0.5,
                "Aucune donnée",
                ha="center",
                va="center",
                wrap=True,
            )
            ax.set_axis_off()
        self._embed(fig, card)

    def _caracteristicsChart_grid(self, parent, row, col):
        """Crée un graphique d'évolution des macros en grille.

        Args:
            parent: Widget parent (grille).
            row: Numéro de ligne dans la grille.
            col: Numéro de colonne dans la grille.
        """
        card = self._create_card(
            parent,
            "Évolution macros",
            buttons=[
                {
                    "text": "Tout",
                    "command": lambda: self.controller.change_period(None, "macro"),
                },
                {
                    "text": "30 derniers",
                    "command": lambda: self.controller.change_period(30, "macro"),
                },
                {
                    "text": "7 derniers",
                    "command": lambda: self.controller.change_period(7, "macro"),
                },
            ],
        )
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        self.macros_card = card
        self._draw_caracteristics_chart(card)

    def _draw_caracteristics_chart(self, card):
        #draw all caracteristics  with the option to choose the time delay
        fig, ax = plt.subplots(figsize=(6, 2.5))
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
            carbohydrate, proteins, fats = [], [], []
            data = self.macrosDated
            dates = sorted(data["proteins"].keys())
            for d in dates:
                carbohydrate.append(data["carbohydrate"][d])
                proteins.append(data["proteins"][d])
                fats.append(data["fats"][d])
            duree = self.controller.duree["macro"]
            if duree:
                dates = dates[-duree:]
                carbohydrate = carbohydrate[-duree:]
                proteins = proteins[-duree:]
                fats = fats[-duree:]
            ax.plot(dates, carbohydrate, color="green", linewidth=2, label="Carbs")
            ax.fill_between(dates, carbohydrate, alpha=0.1, color="green")
            ax.plot(dates, proteins, color="blue", linewidth=2, label="Protéines")
            ax.plot(dates, fats, color="red", linewidth=2, label="Lipides")
            ax.set_xlabel("Date", labelpad=7, fontsize=9)
            ax.set_ylabel("Valeurs (g)", labelpad=10, fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True, linestyle="--", alpha=0.25)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
            fig.autofmt_xdate(rotation=45)
            ax.tick_params(labelsize=8)
        self.macro_canvas, self.macro_widget = self._embed(fig, card)

    def _bodyanalys_compact(self, parent, row):
        """Crée une section compacte des mesu   res corporelles dans la grille.

        Args:
            parent: Widget parent (grille).
            row: Numéro de ligne dans la grille.
        """
        button_color = self.theme_colors.get("button", "#2A2D30")
        button_hover = self.theme_colors.get("button_hover", "#35393D")
        content_color = self.theme_colors.get("content", "#17191B")
        text_color = self.theme_colors.get("text", "#F1F1F1")
        text_secondary = self.theme_colors.get("text_secondary", "#A8AFB6")

        # création de la card
        card = self._create_card(parent, "Mesures corporelles", center_title=True)
        card.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Conteneur principal
        main_container = ctk.CTkFrame(card, fg_color="transparent")
        main_container.pack(fill="both", expand=False, padx=15, pady=10)

        # Row 1: Date et boutons
        top_row = ctk.CTkFrame(main_container, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))

        top_row_center = ctk.CTkFrame(top_row, fg_color="transparent")
        top_row_center.pack(anchor="center")
        # Date frame
        date_frame = ctk.CTkFrame(top_row, fg_color=button_color, corner_radius=10)
        date_frame.pack(in_=top_row_center, side="left", padx=(0, 10))

        self.button_previous = ctk.CTkButton(
            date_frame,
            text="◀",
            width=25,
            fg_color=button_color,
            font=ctk.CTkFont(size=12),
            hover_color=button_hover,
            text_color=text_color,
            corner_radius=10,
        )
        self.button_previous.pack(side="left", padx=4, pady=2)
        self.button_previous.bind("<Button-1>", self.controller.previous_day)

        self.date_label = ctk.CTkLabel(
            date_frame,
            text=self.controller.current_date.strftime("%d/%m/%Y").capitalize(),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=text_color,
            corner_radius=10,
        )
        self.date_label.pack(side="left", padx=12, pady=2)

        self.button_next = ctk.CTkButton(
            date_frame,
            text="▶",
            width=25,
            fg_color=button_color,
            font=ctk.CTkFont(size=12),
            hover_color=button_hover,
            text_color=text_color,
            corner_radius=10,
        )
        self.button_next.pack(side="left", padx=4, pady=2)
        self.button_next.bind("<Button-1>", self.controller.next_day)

        # Bouton ajouter
        boutton_ajouter = ctk.CTkButton(
            top_row,
            text="+ Ajouter mesure",
            font=ctk.CTkFont(size=10),
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
            text_color="#FFFFFF",
        )
        boutton_ajouter.pack(in_=top_row_center, side="left")
        boutton_ajouter.bind("<Button-1>", self.ajouter_mesure)

        # Row 2: Entrées compactes
        entries_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        entries_frame.pack(fill="x", pady=(0, 10))

        entries_center = ctk.CTkFrame(entries_frame, fg_color="transparent")
        entries_center.pack(anchor="center")

        self.poids_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Poids (kg)",
            width=80,
            font=ctk.CTkFont(size=10),
            fg_color=content_color,
            border_color=button_color,
            text_color=text_color,
            placeholder_text_color=text_secondary,
        )
        self.poids_entry.pack(in_=entries_center, side="left", padx=3)

        self.taille_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Tour taille",
            width=80,
            font=ctk.CTkFont(size=10),
            fg_color=content_color,
            border_color=button_color,
            text_color=text_color,
            placeholder_text_color=text_secondary,
        )
        self.taille_entry.pack(in_=entries_center, side="left", padx=3)

        self.bras_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Tour bras",
            width=80,
            font=ctk.CTkFont(size=10),
            fg_color=content_color,
            border_color=button_color,
            text_color=text_color,
            placeholder_text_color=text_secondary,
        )
        self.bras_entry.pack(in_=entries_center, side="left", padx=3)

        self.graisse_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Masse grasse %",
            width=80,
            font=ctk.CTkFont(size=10),
            fg_color=content_color,
            border_color=button_color,
            text_color=text_color,
            placeholder_text_color=text_secondary,
        )
        self.graisse_entry.pack(in_=entries_center, side="left", padx=3)

        ctk.CTkLabel(
            main_container,
            text="Historique (5 dernières)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=text_color,
        ).pack(anchor="w", pady=(10, 5))

        self.tableau_scroll = ctk.CTkScrollableFrame(
            main_container, fg_color=content_color, height=120, corner_radius=10
        )
        self.tableau_scroll.pack(fill="x")
        self.ligne_tableau = 1
        for i in range(5):
            self.tableau_scroll.grid_columnconfigure(i, weight=1, uniform="table")
        headers = ["Date", "Poids", "Tour taille", "Tour bras", "Masse grasse"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.tableau_scroll,
                text=header,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color=text_color,
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        mesures_existantes = self.controller.get_mesures_corporelles()
        for mesure in list(reversed(mesures_existantes))[:5]:
            self.ajouter_ligne_mesure(mesure)

    def ajouter_mesure(self, event=None):
        """
        Crée une nouvelle mesure corporelle à partir des champs de saisie de l'interface,
        l'ajoute au contrôleur et met à jour l'affichage du tableau.

        La mesure est construite à partir de la date courante et des valeurs saisies
        dans les champs poids, taille, bras et graisse.

        Params:
            event (tkinter.Event):
                Événement de clic bouton (ignoré dans la logique métier)
        Returns:
            None
        """
        mesure = MesuresCorporelles(
            self.controller.current_date.strftime("%Y-%m-%d"),
            self.poids_entry.get(),
            self.taille_entry.get(),
            self.bras_entry.get(),
            self.graisse_entry.get(),
        )

        self.controller.ajouter_mesure(mesure)
        self.ajouter_ligne_mesure(mesure)

    def ajouter_ligne_mesure(self, mesure):
        """
        Ajoute une nouvelle ligne de mesure dans un tableau sur la vue.

        La méthode insère la nouvelle mesure à la bonne position selon sa date,
        décale les lignes existantes si nécessaire, puis ajoute les widgets associés.

        Parameters:
            mesure : object
                Objet contenant les attributs de mesure :
                - date : str (ou comparable)
                - poids : float
                - tour_de_taille : float
                - tour_de_bras : float
                - masse_grasse : float

        Returns:
            None
        """
        text_color = self.theme_colors.get("text", "#F1F1F1")
        values = [
            mesure.date,
            mesure.poids,
            mesure.tour_de_taille,
            mesure.tour_de_bras,
            mesure.masse_grasse,
        ]
        mesure_date = mesure.date

        insert_position = 0
        for i, row in enumerate(self.table_rows):
            row_date_label = row[0]
            row_date = row_date_label.cget("text")

            if mesure_date > row_date:
                insert_position = i
                break
            insert_position = i + 1

        for row in self.table_rows[insert_position:]:
            for widget in row:
                current_info = widget.grid_info()
                widget.grid_configure(row=current_info["row"] + 1)

        row_widget = []
        for col, value in enumerate(values):
            label = ctk.CTkLabel(self.tableau_scroll, text=value, text_color=text_color)
            label.grid(
                row=insert_position + 1, column=col, padx=35, pady=5, sticky="nsew"
            )
            row_widget.append(label)

        self.table_rows.insert(insert_position, row_widget)

        if len(self.table_rows) > 10:
            for widget in self.table_rows[-1]:
                widget.destroy()
            self.table_rows.pop()


    def _on_add_mesure(self, event):
        """
        Callback déclenché lors de l'ajout d'une nouvelle mesure corporelle.
        Cette fonction sert à:
        - ajouter une nouvelle mesure via le contrôleur
        - déclencher le rafraîchissement des graphiques
        Args:
            event (tkinter.Event):
                Événement de clic bouton (ignoré dans la logique métier)
        Returns:
            None
        """
        self.ajouter_mesure()
        self.controller._update_charts_only()

    def _chart_mesure_corpo_grid(self, parent, row):
        """
        Affiche le graphique des mesures corporelles
        sur toute la largeur de la dernière ligne du dashboard.

        Args:
            parent: widget parent (dashboard_grid)
            row: numéro de ligne dans la grille
        """

        card = self._create_card(
            parent,
            "Évolution des mesures corporelles",
            buttons=[
                {
                    "text": "Tout",
                    "command": lambda: self.controller.change_period(None, "corpo"),
                },
                {
                    "text": "30 dernier",
                    "command": lambda: self.controller.change_period(30, "corpo"),
                },
                {
                    "text": "7 dernier",
                    "command": lambda: self.controller.change_period(7, "corpo"),
                },
            ],
        )

        card.grid(
            row=row,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
        )
        self.corpo_card = card
        self._draw_corpo_chart(card)

    def _draw_corpo_chart(self, card):
        fig, axes = plt.subplots(
            4,
            1,
            figsize=(12, 8),
            sharex=True,
        )

        fig.subplots_adjust(hspace=0.55)

        mesures = getattr(self.profile, "mesures_corporelles", [])

        if not mesures:
            for ax in axes:
                ax.text(
                    0.5,
                    0.5,
                    "Aucune donnée disponible",
                    ha="center",
                    va="center",
                )
                ax.set_axis_off()

            self._embed(fig, card)
            return

        dates = []
        poids = []
        taille = []
        bras = []
        masse_grasse = []

        # Lecture des données
        for m in mesures:
            try:
                date_val = datetime.datetime.fromisoformat(m.date)
                poids_val = float(m.poids) if m.poids not in (None, "") else 0

                taille_val = (
                    float(m.tour_de_taille) if m.tour_de_taille not in (None, "") else 0
                )

                bras_val = (
                    float(m.tour_de_bras) if m.tour_de_bras not in (None, "") else 0
                )

                masse_grasse_val = (
                    float(m.masse_grasse) if m.masse_grasse not in (None, "") else 0
                )

                dates.append(date_val)
                poids.append(poids_val)
                taille.append(taille_val)
                bras.append(bras_val)
                masse_grasse.append(masse_grasse_val)

            except Exception:
                continue

        if not dates:
            for ax in axes:
                ax.text(
                    0.5,
                    0.5,
                    "Données invalides",
                    ha="center",
                    va="center",
                )
                ax.set_axis_off()

            self._embed(fig, card)
            return

        combined = list(
            zip(
                dates,
                poids,
                taille,
                bras,
                masse_grasse,
            )
        )

        combined.sort(key=lambda x: x[0])

        (
            dates,
            poids,
            taille,
            bras,
            masse_grasse,
        ) = map(list, zip(*combined))

        duree = self.controller.duree["corpo"]

        if duree:
            dates = dates[-duree:]
            poids = poids[-duree:]
            taille = taille[-duree:]
            bras = bras[-duree:]
            masse_grasse = masse_grasse[-duree:]

        axes[0].plot(
            dates,
            poids,
            color=C_GREEN,
            linewidth=2.5,
            label="Poids",
        )

        axes[0].fill_between(
            dates,
            poids,
            alpha=0.15,
            color=C_GREEN,
        )

        axes[0].set_title("Évolution du poids")
        axes[0].set_ylabel("Kg")
        axes[0].legend()
        axes[0].grid(True, linestyle="--", alpha=0.3)

        axes[1].plot(
            dates,
            taille,
            color=C_BLUE,
            linewidth=2.5,
            label="Tour taille",
        )

        axes[1].fill_between(
            dates,
            taille,
            alpha=0.15,
            color=C_BLUE,
        )

        axes[1].set_title("Évolution du tour de taille")
        axes[1].set_ylabel("Cm")
        axes[1].legend()
        axes[1].grid(True, linestyle="--", alpha=0.3)

        axes[2].plot(
            dates,
            bras,
            color=C_ORANGE,
            linewidth=2.5,
            label="Tour bras",
        )

        axes[2].fill_between(
            dates,
            bras,
            alpha=0.15,
            color=C_ORANGE,
        )

        axes[2].set_title("Évolution du tour de bras")
        axes[2].set_ylabel("Cm")
        axes[2].legend()
        axes[2].grid(True, linestyle="--", alpha=0.3)

        axes[3].plot(
            dates,
            masse_grasse,
            color=C_RED,
            linewidth=2.5,
            label="Masse grasse",
        )

        axes[3].fill_between(
            dates,
            masse_grasse,
            alpha=0.15,
            color=C_RED,
        )

        axes[3].set_title("Évolution masse grasse")
        axes[3].set_ylabel("%")
        axes[3].legend()
        axes[3].grid(True, linestyle="--", alpha=0.3)

        # Axe X commun
        axes[3].set_xlabel("Date")

        axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

        fig.autofmt_xdate(rotation=45)

        for ax in axes:
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

        locator = mdates.AutoDateLocator()
        formatter = mdates.DateFormatter("%m/%d")

        for ax in axes:
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

        fig.autofmt_xdate(rotation=45)
        self.corpo_canvas, self.corpo_widget = self._embed(fig, card)