from src.models.settings import Settings

settings = Settings()
settings.deserialize("app.json")
settings.serialize("fichier.json")
