import os
import appdirs
import shutil
import json

def add_example_profile():
    """Crée un fichier settings.json d'exemple pour illustrer correctement l'application Nutritrack. 
    """
    file = "./src/assets/examples/profile_example.json"
    path = os.path.join(appdirs.user_data_dir("Nutritrack"), "settings.json")
    
    with open(file, "r") as example_file:
        example = json.load(example_file)
        profile_data = example["profiles"][0]  # Prendre le premier profil d'exemple
    
    if os.path.isfile(path): # Si le dossier/fichier existe
        with open(path, "r") as settings_file:
            settings_data = json.load(settings_file)
        
        # Vérifier si le profil d'exemple existe déjà dans les paramètres
        if any(p["name"] == profile_data["name"] for p in settings_data.get("profiles", [])):
            print(f"Le profil d'exemple existe déjà dans les paramètres ou le nom \"{profile_data['name']}\" est déjà utilisé.")
            return
        else:
            settings_data["profiles"].append(profile_data)  # Ajouter le profil d'exemple
            with open(path, "w") as settings_file:
                json.dump(settings_data, settings_file, indent=4)
            print("Le profil d'exemple a été ajouté aux paramètres.")
            input("Appuyez sur Entrée pour continuer...")
    else: # Si le dossier/fichier n'existe pas
        os.makedirs(appdirs.user_data_dir("Nutritrack"), exist_ok=True) # Création du dossuer s'il n'existe pas
        shutil.copy(file, path)  # Copier le fichier d'exemple comme nouveau settings.json dans le dossier crée
        print("Le fichier settings.json d'exemple a été créé.")
        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    add_example_profile()