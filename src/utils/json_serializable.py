import json


class JsonSerializable:
    """
    Héritez de cette classe pour obtenir serialize(path).
    Tous les attributs publics d'instance sont sérialisés.
    """

    # ── Sérialisation ────────────────────────────────────────────────────────

    def serialize(self, path: str, *, indent: int = 2) -> None:
        """Écrit cet objet en JSON dans *path*."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self._to_dict(), fh, indent=indent)

    def _to_dict(self) -> dict:
        """
        Convertit la classe en un dictionnaire pour stocker la classe en JSON
        :return: Un dictionnaire représentant les attributs publics de la classe
        """
        result = {}
        # les attributs de la classe sont stockés dans __dict__, on parcourt tous les attributs de la classe
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                # si l'attribut est une classe pouvant être sauvegardée en JSON
                if isinstance(value, JsonSerializable):
                    result[key] = value._to_dict()
                # si l'attribut est une liste, vérifier pour chaque élément son type et appliquer la même logique
                elif isinstance(value, list):
                    result[key] = [
                        item._to_dict() if isinstance(item, JsonSerializable) else item
                        for item in value
                    ]
                # sinon, si l'attribut est un type de base (int, str, etc.), on le stocke directement
                else:
                    result[key] = value
        return result
