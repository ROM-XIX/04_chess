import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List
from config import TOURNAMENTS_FILE


@dataclass
class Tournament:
    nom: str
    lieu: str
    date_start: datetime
    date_end: datetime
    nbr_rounds: int = 3  # valeur par défaut
    current_round: int = 1
    all_rounds: List[Dict[str, Any]] = None
    list_players: List[Dict[str, Any]] = None
    notes: str = ""

    # permet de créer un player depuis le menu
    @staticmethod
    def from_dict(d: dict[str, Any]):
        """Crée l'objet Joueur depuis un dictionnaire"""
        return Tournament(
            nom=d["nom"],
            lieu=d["lieu"],
            date_start=datetime.strptime(d["date_start"], "%Y-%m-%d %H:%M:%S"),
            date_end=datetime.strptime(d["date_end"], "%Y-%m-%d %H:%M:%S"),
            nbr_rounds=d.get("nbr_rounds", 3),
            current_round=d.get("current_round", 1),
            all_rounds=d.get("all_rounds", []),
            list_players=d.get("list_players", []),
            notes=d.get("notes", ""),
        )

    # Convertir l'objet Tournament en dict (pour sauvegarde JSON)
    # on utilise pas asdict comme pour player car on a datetime qui n'est pas un type primitif.
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_start": self.date_start.strftime("%Y-%m-%d %H:%M:%S"),
            "date_end": self.date_end.strftime("%Y-%m-%d %H:%M:%S"),
            "nbr_rounds": self.nbr_rounds,
            "current_round": self.current_round,
            "all_rounds": self.all_rounds,
            "list_players": self.list_players,
            "notes": self.notes,
        }

    # permet de svg les players dans un json
    @classmethod
    def save_all(cls, _tournaments):
        """Sauvegarde une liste d'objet Tournament dans un fichier JSON"""
        with TOURNAMENTS_FILE.open("w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in _tournaments], f, indent=4, ensure_ascii=False)

    # permet de révuper les players depuis le json
    @classmethod
    def load_all(cls):
        """Charge une liste d'objet Tournament depuis un fichier JSON"""
        if TOURNAMENTS_FILE.stat().st_size == 0:
            return []  # aucun fichier → pas de joueurs
        with TOURNAMENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [cls.from_dict(d) for d in data]
