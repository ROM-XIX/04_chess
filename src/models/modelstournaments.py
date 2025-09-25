from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from config import TOURNAMENTS_FILE  # Path vers datas/tournaments/tournaments.json (comme PLAYERS_FILE)


# -------------------- Tournament (modèle) --------------------
@dataclass
class Tournament:
    nom: str
    lieu: str
    date_start: datetime  # fixé à la création (add_tournament)
    date_end: Optional[datetime] = None  # fixé à la clôture du dernier round
    nbr_rounds: int = 4
    current_round: int = 0  # 0 = aucun round commencé ; sinon N = round en cours/dernier créé
    all_rounds: List[RoundTournament] = None  # liste D'OBJETS RoundTournament
    list_players: List[Dict[str, Any]] = None  # à toi de définir la structure (INE/ID, etc.)
    notes: str = ""

    # permet de créer un objet Tournament depuis des données (ex:le menu)

    def __post_init__(self) -> None:
        if self.all_rounds is None:
            self.all_rounds = []
        if self.list_players is None:
            self.list_players = []

    # --------- (dé)sérialisation ---------
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Tournament":
        """Crée l'objet Joueur depuis un dictionnaire"""
        return Tournament(
            nom=d["nom"],
            lieu=d["lieu"],
            date_start=datetime.strptime(d["date_start"], "%Y-%m-%d %H:%M:%S"),
            date_end=datetime.strptime(d["date_end"], "%Y-%m-%d %H:%M:%S"),
            # date_end=datetime.strptime(d["date_end"], "%Y-%m-%d %H:%M:%S") if d.get("date_end") else None,
            nbr_rounds=d.get("nbr_rounds", 4),
            current_round=d.get("current_round", 0),
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

    # permet de récupérer les players depuis le json
    @classmethod
    def load_all(cls) -> List["Tournament"]:
        """Charge une liste d'objet Tournament depuis un fichier JSON"""
        if TOURNAMENTS_FILE.stat().st_size == 0:
            return []  # aucun fichier → pas de joueurs
        with TOURNAMENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [cls.from_dict(d) for d in data]


# -------------------- Round (objet) --------------------
@dataclass
class RoundTournament:
    """
    Représente un tour :
    - name: "Round 1", "Round 2", etc.
    - start_time / end_time: datetimes (None tant que non démarré/terminé)
    - matches: liste de matchs ; chaque match = tuple( [joueur1, score1], [joueur2, score2] )
      Ex: (["AB12345", 1.0], ["CD67890", 0.0])
    """

    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    matches: List[Tuple[List[Any], List[float]]] = None  # tuple de 2 listes [player, score]

    def __post_init__(self) -> None:
        if self.matches is None:
            self.matches = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
            "matches": self.matches,  # déjà JSON-serializable
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RoundTournament":
        return RoundTournament(
            name=d["name"],
            start_time=datetime.strptime(d["start_time"], "%Y-%m-%d %H:%M:%S") if d.get("start_time") else None,
            end_time=datetime.strptime(d["end_time"], "%Y-%m-%d %H:%M:%S") if d.get("end_time") else None,
            matches=d.get("matches", []),
        )
