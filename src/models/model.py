class Model:
    """
    Cette classe permet de signifier clairement ce qu'est un Modèle dans l'implémentation de l'architecture MVC. La méthode to_dict() est utilisée pour convertir les classes héritant de Model en dictionnaire, ce qui facilite la sérialisation en JSON.
    """

    def to_dict(self) -> dict:
        """
        Convertit la classe en un dictionnaire pour stocker la classe en JSON
        :return: Un dictionnaire représentant les attributs publics de la classe
        """
        result = {}
        # les attributs de la classe sont stockés dans __dict__, on parcourt tous les attributs de la classe
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                # si l'attribut est une classe pouvant être sauvegardée en JSON
                if isinstance(value, Model):
                    result[key] = value.to_dict()
                # si l'attribut est une liste, vérifier pour chaque élément son type et appliquer la même logique
                elif isinstance(value, list):
                    result[key] = [
                        item.to_dict() if isinstance(item, Model) else item
                        for item in value
                    ]
                # sinon, si l'attribut est un type de base (int, str, etc.), on le stocke directement
                else:
                    result[key] = value
        return result
