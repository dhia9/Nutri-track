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
        self.history = self.controller.generate_history(30)
        self.period = 7
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        self.table_rows = []
        # Récupérer les couleurs du thème
        self.theme_colors = self.main_controller.theme_colors
        self.update_matplotlib_colors()

        self._build()

    def update_matplotlib_colors(self):
        """Met à jour les couleurs matplotlib selon le thème actuel."""
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
        """
        for child in self.winfo_children():
            child.destroy()

        self.profile = self.controller.get_current_profile()
        self.history = self.controller.generate_history(30)
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
        self.table_rows = []

        # Mettre à jour les couleurs du thème
        self.theme_colors = self.main_controller.theme_colors
        self.update_matplotlib_colors()

        self._build()

    def _create_card(self, parent, title):
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
        card.pack(fill="x", pady=10)
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 5))
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_colors.get("text", "#F1F1F1"),
        ).pack(anchor="w")
        return card

    def _embed(self, fig, parent):
        """Insère un graphique matplotlib dans un widget tkinter.

        Args:
            fig: La figure matplotlib à insérer.
            parent: Le widget parent où ajouter le graphique.
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

    def _build(self):
        """Construit l'interface des statistiques.

        Crée l'entête et les graphiques à afficher.
        """
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
        """Affiche tous les graphiques de statistiques.

        Crée et affiche les graphiques de calories, caractéristiques,
        et macros (pie et bar).
        """
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
        self._chart_mesure_corpo(row)

    def _chart_calories(self, data):
        """Crée un graphique d'évolution des calories.

        Args:
            data: Dictionnaire des calories par date.
        """
        card = self._create_card_Version(
            self.scroll,
            "Évolution calories",
            buttons=[
                {
                    "text": "Tout",
                    "command": lambda: self.controller.change_period(None, "calor"),
                },
                {
                    "text": "30 dernier",
                    "command": lambda: self.controller.change_period(30, "calor"),
                },
                {
                    "text": "7 dernier",
                    "command": lambda: self.controller.change_period(7, "calor"),
                },
            ],
        )
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
            dates = [parser.parse(d) for d in data.keys()]
            calories = list(data.values())
            duree = self.controller.duree["calor"]
            if duree:
                combined = list(zip(dates, calories))
                combined.sort(key=lambda x: x[0])
                combined = combined[-duree:]
                dates, calories = map(list, zip(*combined))
            ax.plot(
                dates,
                calories,
                color=self.main_controller.settings.theme,
                linewidth=2.5,
                label="Calories",
            )
            ax.fill_between(
                dates, calories, alpha=0.15, color=self.main_controller.settings.theme
            )
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
        """Crée un graphique en camembert des macros du dernier repas.

        Args:
            parent: Widget parent où afficher le graphique.
        """
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
        """Crée un graphique en barres pour comparer les macros du dernier repas.

        Args:
            parent: Widget parent où afficher le graphique.
        """
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
        """Crée un graphique d'évolution des macros (protéines, lipides, glucides)."""
        card = self._create_card_Version(
            self.scroll,
            "Évolution macros",
            buttons=[
                {
                    "text": "Tout",
                    "command": lambda: self.controller.change_period(None, "macro"),
                },
                {
                    "text": "30 dernier",
                    "command": lambda: self.controller.change_period(30, "macro"),
                },
                {
                    "text": "7 dernier",
                    "command": lambda: self.controller.change_period(7, "macro"),
                },
            ],
        )
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
            dates = [d for d in self.macrosDated["proteins"].keys()]
            dates = [parser.parse(d) for d in dates]
            carbohydrate = list(self.macrosDated["proteins"].values())
            proteins = list(self.macrosDated["proteins"].values())
            fats = list(self.macrosDated["fats"].values())
            duree = self.controller.duree["macro"]
            if duree:
                combined = list(zip(dates, carbohydrate, proteins, fats))
                combined.sort(key=lambda x: x[0])
                combined = combined[-duree:]
                dates, carbohydrate, proteins, fats = map(list, zip(*combined))

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
        date_frame = ctk.CTkFrame(
            top_row,
            fg_color=self.theme_colors.get("frame", "#2A2D30"),
            corner_radius=10,
        )
        date_frame.pack(side="right")

        self.button_previous = ctk.CTkButton(
            date_frame,
            text="◀",
            width=30,
            text_color=self.theme_colors.get("text", "#2A2D30"),
            fg_color=self.theme_colors.get("frame", "#2A2D30"),
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=self.theme_colors.get("button_hover", "#35393D"),
            corner_radius=10,
        )
        self.button_previous.pack(side="left", padx=6, pady=4)
        self.button_previous.bind("<Button-1>", self.controller.previous_day)

        self.date_label = ctk.CTkLabel(
            date_frame,
            text=self.controller.current_date.strftime("  %A %d %B %Y  ").capitalize(),
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=10,
        )
        self.date_label.pack(side="left", padx=18, pady=4)

        self.button_next = ctk.CTkButton(
            date_frame,
            text="▶",
            width=30,
            text_color=self.theme_colors.get("text", "#2A2D30"),
            fg_color=self.theme_colors.get("frame", "#2A2D30"),
            font=ctk.CTkFont(size=12, weight="bold"),
            hover_color=self.theme_colors.get("button_hover", "#35393D"),
            corner_radius=10,
        )
        self.button_next.pack(side="left", padx=6, pady=4)
        self.button_next.bind("<Button-1>", self.controller.next_day)

        # Boutton ajouter
        boutton_ajouter = ctk.CTkButton(
            top_row,
            text="Ajouter une mesure corporelle",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=10,
            text_color=self.main_controller.theme_colors["text"],
            fg_color=self.main_controller.settings.theme,
            hover_color=self.main_controller.darken_color(
                self.main_controller.settings.theme
            ),
        )
        boutton_ajouter.pack(side="left")
        boutton_ajouter.bind("<Button-1>", self._on_add_mesure)

        # Frame pour les labels
        labels_frame = ctk.CTkFrame(card, fg_color="transparent")
        labels_frame.pack(fill="x", padx=15, pady=(10, 0))

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
        entries_frame.pack(fill="x", padx=15, pady=(5, 15))

        # Création des validateurs (pour n'entrer que des floats)
        float_vcmd = (self.register(self.main_controller.validate_float), "%P")

        self.poids_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Poids en kg",
            validate="key",
            validatecommand=float_vcmd,
        )
        self.poids_entry.pack(side="left", expand=True, padx=5)

        self.taille_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Tour de taille en cm",
            validate="key",
            validatecommand=float_vcmd,
        )
        self.taille_entry.pack(side="left", expand=True, padx=5)

        self.bras_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Tour de bras en cm",
            validate="key",
            validatecommand=float_vcmd,
        )
        self.bras_entry.pack(side="left", expand=True, padx=5)

        self.graisse_entry = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Masse grasse en %",
            validate="key",
            validatecommand=float_vcmd,
        )
        self.graisse_entry.pack(side="left", expand=True, padx=5)

        # Label historique
        historique_header = ctk.CTkFrame(card, fg_color="transparent")
        historique_header.pack(fill="x", padx=14, pady=(10, 0))
        ctk.CTkLabel(
            historique_header,
            text="Historique des mesures corporelles",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_colors.get("text", "#F1F1F1"),
        ).pack(anchor="w")

        # Tableau de l'historique
        self.tableau_frame = ctk.CTkFrame(
            card, fg_color=self.theme_colors.get("frame", "#2A2D30"), corner_radius=10
        )
        self.tableau_frame.pack(fill="x", padx=15, pady=10)
        self.ligne_tableau = 1
        headers = [
            "Date",
            "Poids (kg)",
            "Tour de taille (cm)",
            "Tour de bras (cm)",
            "Masse grasse (%)",
        ]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.tableau_frame, text=header, font=ctk.CTkFont(weight="bold")
            )
            label.grid(row=0, column=col, padx=35, pady=5)

        self.table_rows = []
        mesures_existantes = self.controller.get_mesures_corporelles() or []
        for mesure in reversed(mesures_existantes):
            self.controller._create_ligne_mesure(mesure)

    def ajouter_mesure(self):
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
        values = [
            mesure.date,
            mesure.poids,
            mesure.tour_de_taille,
            mesure.tour_de_bras,
            mesure.masse_grasse,
        ]
        mesure_date = mesure.date

        # Trouver la bonne position pour insérer la mesure (ordre décroissant par date)
        insert_position = 0
        for i, row in enumerate(self.table_rows):
            # Récupérer la date de la ligne existante (première cellule)
            row_date_label = row[0]
            row_date = row_date_label.cget("text")

            # Si la nouvelle date est plus récente, insérer avant cette ligne
            if mesure_date > row_date:
                insert_position = i
                break
            insert_position = i + 1

        # Décaler les lignes après la position d'insertion
        for row in self.table_rows[insert_position:]:
            for widget in row:
                current_info = widget.grid_info()
                widget.grid_configure(row=current_info["row"] + 1)

        # Créer la nouvelle ligne à la bonne position
        row_widget = []
        for col, value in enumerate(values):
            label = ctk.CTkLabel(self.tableau_frame, text=value)
            label.grid(row=insert_position + 1, column=col, padx=35, pady=5)
            row_widget.append(label)

        self.table_rows.insert(insert_position, row_widget)

        # Supprimer la ligne la plus ancienne si on dépasse 10 lignes
        if len(self.table_rows) > 10:
            for widget in self.table_rows[-1]:
                widget.destroy()
            self.table_rows.pop()

    def _chart_mesure_corpo(self, parent):
        """
        Génère un graphique multi-axes (4 sous-graphiques) représentant l'évolution
        des mesures corporelles d'un profil.
        Args:
            parent (tkinter widget / CTkFrame):
                Le conteneur dans lequel le graphique Matplotlib sera intégré.
        Returns:
            None
        """
        card = self._create_card_Version(
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
        fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
        fig.subplots_adjust(hspace=0.5)

        mesures = getattr(self.profile, "mesures_corporelles", [])
        if not mesures:
            for ax in axes:
                ax.text(0.5, 0.5, "Aucune donnée disponible", ha="center", va="center")
                ax.set_axis_off()
            self._embed(fig, card)
            return

        dates = []
        poids, taille, bras, masse_grasse = [], [], [], []

        for m in mesures:
            try:
                # Vérifier et convertir tous les éléments avant d'ajouter à la liste
                date_val = m.date
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

                # Ajouter à la liste seulement si tout est valide
                dates.append(date_val)
                poids.append(poids_val)
                taille.append(taille_val)
                bras.append(bras_val)
                masse_grasse.append(masse_grasse_val)

            except Exception:
                continue

        if not dates:
            for ax in axes:
                ax.text(0.5, 0.5, "Données invalides", ha="center", va="center")
                ax.set_axis_off()
            self._embed(fig, card)
            return
        duree = self.controller.duree["corpo"]
        if duree:
            # méthode utile pour trier les listes de la même manière
            combined = list(zip(dates, poids, taille, bras, masse_grasse))
            combined.sort(key=lambda x: x[0])
            dates, poids, taille, bras, masse_grasse = map(list, zip(*combined))
            dates = self.controller.last_n_elements(dates, duree)
            poids = self.controller.last_n_elements(poids, duree)
            taille = self.controller.last_n_elements(taille, duree)
            bras = self.controller.last_n_elements(bras, duree)
            masse_grasse = self.controller.last_n_elements(masse_grasse, duree)
        dates = [parser.parse(d) for d in dates]
        axes[0].plot(dates, poids, color=C_GREEN, label="Poids corporel")
        axes[0].set_title("Évolution du poids")
        axes[0].set_ylabel("Poids (kg)")
        axes[0].legend()
        axes[0].grid(True, linestyle="--", alpha=0.3)

        axes[1].plot(dates, taille, color=C_BLUE, label="Tour de taille")
        axes[1].set_title("Évolution du tour de taille")
        axes[1].set_ylabel("Tour de taille (cm)")
        axes[1].legend()
        axes[1].grid(True, linestyle="--", alpha=0.3)

        axes[2].plot(dates, bras, color=C_ORANGE, label="Tour de bras")
        axes[2].set_title("Évolution du tour de bras")
        axes[2].set_ylabel("Tour de bras (cm)")
        axes[2].legend()
        axes[2].grid(True, linestyle="--", alpha=0.3)

        axes[3].plot(dates, masse_grasse, color=C_RED, label="Masse grasse")
        axes[3].set_title("Évolution du taux de masse grasse")
        axes[3].set_ylabel("Pourcentage (%)")
        axes[3].legend()
        axes[3].grid(True, linestyle="--", alpha=0.3)

        # axe x commun
        axes[3].set_xlabel("Date de mesure")
        axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        fig.autofmt_xdate()

        self._embed(fig, card)

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

    def _create_card_Version(self, parent, title, buttons=None):
        """Crée une carte pour afficher un graphique."""

        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme_colors.get("frame", "#2A2D30"),
            corner_radius=14,
        )
        card.pack(fill="x", pady=10)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 5))

        # Partie gauche : titre
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.theme_colors.get("text", "#F1F1F1"),
        )
        title_label.pack(side="left")

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
