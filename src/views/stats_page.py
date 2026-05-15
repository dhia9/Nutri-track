import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

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


class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, main_controller):
        super().__init__(parent, fg_color="transparent")
        self.main_controller = main_controller
        self.controller = self.main_controller.controllers["Stats"]
        self.controller.view = self
        self.profile = self.controller.get_current_profile()
        self.history = self.controller.generate_history(30)
        self.period = 7
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
        data = self.history[-self.period :]
        self._chart_calories(data)
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", pady=10)
        self._chart_macros_pie(data, row)
        self._chart_macros_bar(data, row)
        self._chart_salt_sugar(data)

    def _chart_calories(self, data):
        card = self._create_card(self.scroll, "Évolution calories")
        fig, ax = plt.subplots(figsize=(8, 3))
        dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in data]
        calories = [d["calories"] for d in data]
        ax.plot(dates, calories, color=C_GREEN, linewidth=2.5, label="Calories")
        ax.fill_between(dates, calories, alpha=0.15, color=C_GREEN)
        ax.set_xlabel("Date", labelpad=12)
        ax.set_ylabel("Calories", labelpad=10)
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        self._embed(fig, card)

    def _chart_macros_pie(self, data, parent):
        card = self._create_card(parent, "Macros")
        avg_p = self.controller.mesure_avg(data, "proteins")
        avg_c = self.controller.mesure_avg(data, "carbs")
        avg_f = self.controller.mesure_avg(data, "fats")
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(
            [avg_p, avg_c, avg_f],
            colors=[C_PURPLE, C_BLUE, C_ORANGE],
            startangle=90,
            wedgeprops={"edgecolor": "#1D1F21"},
        )
        ax.set_position([0.20, 0.1, 0.6, 0.8])
        fig.tight_layout()
        ax.legend(
            ["Protéines", "Glucides", "Lipides"],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )
        self._embed(fig, card)

    def _chart_macros_bar(self, data, parent):
        card = self._create_card(parent, "Comparaison")
        avg_p = self.controller.mesure_avg(data, "proteins")
        avg_c = self.controller.mesure_avg(data, "carbs")
        avg_f = self.controller.mesure_avg(data, "fats")
        fig, ax = plt.subplots(figsize=(4, 4))
        bars = ax.bar(
            [1, 2, 3], [avg_p, avg_c, avg_f], color=[C_PURPLE, C_BLUE, C_ORANGE]
        )
        ax.set_xticks([])
        ax.set_xlabel("Macronutriments", labelpad=12)
        ax.set_ylabel("Quantité moyenne", labelpad=10)
        ax.legend(bars, ["Protéines", "Glucides", "Lipides"])
        ax.grid(True, axis="y", alpha=0.2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        self._embed(fig, card)

    def _chart_salt_sugar(self, data):
        card = self._create_card(self.scroll, "Sel & Sucre")
        fig, ax = plt.subplots(figsize=(8, 3))
        dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in data]
        salt = [d["salt"] for d in data]
        sugar = [d["sugar"] for d in data]
        ax.plot(dates, salt, color=C_RED, label="Sel", linewidth=2)
        ax.plot(dates, sugar, color=C_ORANGE, label="Sucre", linewidth=2)
        ax.fill_between(dates, salt, alpha=0.08, color=C_RED)
        ax.fill_between(dates, sugar, alpha=0.08, color=C_ORANGE)
        ax.set_xlabel("Date", labelpad=12)
        ax.set_ylabel("Grammes", labelpad=10)
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        self._embed(fig, card)
