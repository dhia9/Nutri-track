import customtkinter as ctk


class CTkMessageBox(ctk.CTkToplevel):
    def __init__(self, title="", message="", button_text="OK"):
        super().__init__()
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        label = ctk.CTkLabel(self, text=message, wraplength=250)
        label.pack(pady=20, padx=20)

        button = ctk.CTkButton(self, text=button_text, command=self.destroy)
        button.pack(pady=10)

        # Centrer la messagebox l'écran
        self.update_idletasks()  # update les dimensions de la fenêtre avant de calculer la position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 150 
        y = (screen_height // 2) - 75 
        self.geometry(f"+{x}+{y}")

        self.grab_set()
        self.wait_window() # Empèche l'utilisateur d'interagir avec la fenêtre principale tant que le message box est ouvert


# Utilisation
if __name__ == "__main__":
    CTkMessageBox(title="Info", message="Profil créé avec succès !")
