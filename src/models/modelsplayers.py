from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import List
from config import PLAYERS_FILE

@dataclass
class Player:
    nom: str
    prenom: str
    datenaissance : str
    ine: str

    # permet de créer un player depuis le menu
    @staticmethod
    def from_dict(d: dict):
        """Crée l'objet Joueur depuis un dictionnaire"""
        return Player(
            d["nom"],
            d["prenom"],
            d["datenaissance"],
            d["ine"]
        )

    # permet de créer un dictionnaire depuis un json
    def to_dict(self):
        """Crée un dictionnaire depuis un object"""
        return asdict(self)

    # permet de svg les players dans un json
    @classmethod
    def save_all(cls, players: List["Player"]):
        """Sauvegarde une liste de joueurs dans un fichier JSON"""
        with PLAYERS_FILE.open("w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in players], f, indent=4, ensure_ascii=False)

    # permet de révuper les players depuis le json
    @classmethod
    def load_all(cls):
        """Charge une liste de joueurs depuis un fichier JSON"""

        if PLAYERS_FILE.stat().st_size == 0:
            return []  # aucun fichier → pas de joueurs
        with PLAYERS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [cls.from_dict(d) for d in data]