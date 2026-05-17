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
        self._build()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()

        self.profile = self.controller.get_current_profile()
        self.history = self.controller.generate_history(30)
        self.macrosDated = self.controller.macros_by_date()
        self.macrosToday = self.controller.macros_today(datetime.date.today())
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
                datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in data.keys()
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
                datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
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
