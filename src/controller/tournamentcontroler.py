from __future__ import annotations
from datetime import datetime
from models.modelstournaments import Tournament
from typing import Any, Dict, List


class TournamentController:
    def add_tournament(
        self,
        nom: str,
        lieu: str,
        date_start: datetime,
        date_end: datetime,
        nbr_rounds: int = 3,  # valeur par défaut
        current_round: int = 1,
        all_rounds: List[Dict[str, Any]] = None,
        list_players: List[Dict[str, Any]] = None,
        notes: str = "",
    ):
        """Ajouter un nouveau Tournoi et le sauvegarder"""
        # vérification de birthdate
        birthdate_ = birthdate
        try:
            datetime.strptime(birthdate_, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date de naissance invalide (format attendu: YYYY-MM-DD).")

        # vérification de ine
        ine_ = ine.strip().upper()
        if len(ine_) != 7 or not ine_[:2].isalpha() or not ine_[2:].isdigit():
            raise ValueError("Identifiant national invalide (format attendu: 2 lettres + 5 chiffres, ex. AB12345).")

        # charger les joueurs déjà existant dans le json
        joueurs_charges = Tournament.load_all()

        # vérification que le joueur n'existe pas déja dans les données
        if any(p.ine.upper() == ine_ for p in joueurs_charges):
            raise ValueError("Un joueur avec ce même identifiant existe déjà.")
        _tournament = Tournament(
            nom=last_name.strip(),
            prenom=first_name.strip(),
            datenaissance=birthdate.strip(),
            ine=ine,
        )
        joueurs_charges.append(_tournament)
        Tournament.save_all(joueurs_charges)

        return player

    def list_tournaments(self):
        """Liste tous les joueurs déjà inscrits list(objets Player)."""
        return Player.load_all()
        # return Player.load_all(filename)

    def generate_round(self):
        pass

    def add_round_result(self):
        pass

    def close_round(self):
        pass
