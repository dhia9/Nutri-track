import json

from src.models.model import Model


class JsonSerializable(Model):
    """
    Héritez de cette classe pour obtenir serialize(path).
    Tous les attributs publics d'instance sont sérialisés.
    """

    def serialize(self, path: str, indent: int = 2) -> None:
        """
        Sérialise la classe en JSON et stocke le fichier dans le chemin spécifié.
        :param path: Chemin où stocker le fichier JSON
        :param indent: Indentation du fichier JSON (2 par défaut)
        :return: None
        """
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=indent)
