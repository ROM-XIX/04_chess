from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class Player:
    nom: str
    prenom: str
    datenaissance: str  # attendu au format "YYYY-MM-DD"
    ine: str            # attendu au format LLDDDDD, ex. "AB12345"

    # créer un Player depuis un dict
    @staticmethod
    def from_dict(d: Dict[str, Any]):
        """Crée un Joueur depuis un dictionnaire."""
        return Player(
            nom=d["nom"],
            prenom=d["prenom"],
            datenaissance=d["datenaissance"],
            ine=d["ine"],
        )

    def to_dict(self):
        """Convertit l’objet Player en dictionnaire."""
        return asdict(self)

    @classmethod
    def save_all(cls, players: List["Player"], filename: str):
        """Sauvegarde une liste de joueurs dans un fichier JSON."""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in players], f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls, filename: str):
        """Charge une liste de joueurs depuis un fichier JSON."""
        path = Path(filename)
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [cls.from_dict(d) for d in data]
