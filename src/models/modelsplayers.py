from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class Player:
    nom: str
    prenom: str
    datenaissance : str
    ine: str

    # permet de créer un player depuis le menu
    @staticmethod
    def from_dict(d: dict):
        """Crée un Joueur depuis un dictionnaire"""
        return Player(
            d["nom"],
            d["prenom"],
            d["datenaissance"],
            d["ine"]
        )

    # permet de créer un dictionnaire depuis un json
    def to_dict(self):
        """Convertit l’objet Player en dictionnaire"""
        return asdict(self)

    # permet de svg les players dans un json
    @classmethod
    def save_all(cls, players: List["Player"], filename: str):
        """Sauvegarde une liste de joueurs dans un fichier JSON"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in players], f, indent=4, ensure_ascii=False)

    # permet de révuper les players depuis le json
    @classmethod
    def load_all(cls, filename: str):
        """Charge une liste de joueurs depuis un fichier JSON"""
        path = Path(filename)
        if path.stat().st_size == 0:
            return []  # aucun fichier → pas de joueurs
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [cls.from_dict(d) for d in data]