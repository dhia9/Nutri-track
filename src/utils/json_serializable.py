import json
import typing
from typing import Any, Type, TypeVar, get_type_hints

T = TypeVar("T", bound="JsonSerializable")


def _origin(hint) -> Any:
    """Retourne l'origine générique d'un type hint (ex : list, Union)."""
    return getattr(hint, "__origin__", None)


def _args(hint) -> tuple:
    """Retourne les arguments de type d'un hint générique (ex : (str,) pour list[str])."""
    return getattr(hint, "__args__", ()) or ()


def _is_list_hint(hint) -> bool:
    return _origin(hint) in (list, typing.List)


def _is_union_hint(hint) -> bool:
    return _origin(hint) is typing.Union


def _unwrap_optional(hint):
    """
    Si le hint est Optional[X] (c.-à-d. Union[X, None]), retourne X.
    Sinon, retourne le hint inchangé.
    """
    if _is_union_hint(hint):
        non_none = [a for a in _args(hint) if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return hint


def _is_serializable_class(cls) -> bool:
    return isinstance(cls, type) and issubclass(cls, JsonSerializable)


class JsonSerializable:
    """
    Héritez de cette classe pour obtenir serialize(path) / deserialize(path).

    Tous les attributs publics d'instance sont sérialisés.
    Les annotations de type dans __init__ pilotent la désérialisation
    des objets imbriqués et des listes d'objets.
    """

    # ── Sérialisation ────────────────────────────────────────────────────────

    def serialize(self, path: str, *, indent: int = 2) -> None:
        """Écrit cet objet en JSON dans *path*."""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self._to_dict(), fh, indent=indent)

    def _to_dict(self) -> dict:
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                result[key] = _serialize_value(value)
        return result

    # ── Désérialisation ───────────────────────────────────────────────────────

    @classmethod
    def deserialize(cls: Type[T], path: str) -> T:
        """Lit un fichier JSON situé à *path* et retourne une instance de *cls*."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise TypeError(f"Objet JSON attendu, obtenu {type(data).__name__!r}.")
        return cls._from_dict(data)

    @classmethod
    def _from_dict(cls: Type[T], data: dict) -> T:
        hints = _collect_hints(cls)
        instance = cls.__new__(cls)
        for key, raw_value in data.items():
            hint = hints.get(key)
            setattr(instance, key, _deserialize_value(raw_value, hint))
        return instance


# Fonctions utilitaires pour la sérialisation / désérialisation
def _collect_hints(cls: type) -> dict:
    """
    Fusionne les annotations de type de la classe et de __init__ afin que
    les hints définis de l'une ou l'autre manière soient disponibles
    lors de la désérialisation.
    """
    hints: dict = {}
    try:
        hints.update(get_type_hints(cls))
    except Exception:
        pass
    try:
        hints.update(get_type_hints(cls.__init__))
    except Exception:
        pass
    hints.pop("return", None)
    return hints


def _serialize_value(value: Any) -> Any:
    """Convertit récursivement une valeur en un type compatible JSON."""
    if isinstance(value, JsonSerializable):
        return value._to_dict()
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(
        f"La valeur de type {type(value).__name__!r} n'est pas sérialisable."
    )


def _deserialize_value(raw: Any, hint) -> Any:
    """Reconstruit une valeur à partir de données JSON brutes en utilisant son type."""
    if hint is None:
        return raw  # pas de hint → retour tel quel

    # Déballer Optional[X] → X (et conserver None tel quel)
    hint = _unwrap_optional(hint)
    if raw is None:
        return None

    # list[SomeClass] ou list[str] etc.
    if _is_list_hint(hint):
        item_hint = _args(hint)[0] if _args(hint) else None
        return [_deserialize_value(item, item_hint) for item in raw]

    # JsonSerializable imbriqué
    if _is_serializable_class(hint) and isinstance(raw, dict):
        return hint._from_dict(raw)

    return raw
