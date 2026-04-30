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

        self.bind("<FocusOut>", lambda e: self.destroy()) # ferme la fenetre si un appuie en dehors

        self.grab_set()


# Utilisation
if __name__ == "__main__":
    CTkMessageBox(title="Info", message="Profil créé avec succès !")
