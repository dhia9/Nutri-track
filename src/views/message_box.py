import customtkinter as ctk


class CTkMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title="", message="", button_text="OK"):
        super().__init__()
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        # Établir la relation parent-enfant pour rendre la fenêtre modale
        self.transient(parent)
        self.attributes("-topmost", True)

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=20, padx=20)

        button = ctk.CTkButton(self, text=button_text, command=self.destroy)
        button.pack(pady=10)

        # Centrer la messagebox sur l'écran
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 150
        y = (screen_height // 2) - 75
        self.geometry(f"+{x}+{y}")

        # Empêche de cliquer en dehors de la messagebox pour la fermer
        self.grab_set()
        self.wait_window()  # Empèche l'utilisateur d'interagir avec la fenêtre principale tant que le message box est ouvert


# Utilisation
if __name__ == "__main__":
    CTkMessageBox(title="Info", message="Profil créé avec succès !")
