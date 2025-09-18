from __future__ import annotations
from models.modelsplayers import Player
from datetime import datetime
from pathlib import Path


filename = "/home/athena6/Documents/OpenClasseRooms/04_echec/projet_04/src/datas/players/players.json"
# DATA_Joueurs = Path("datas/players/players.json")


class PlayerController:
    def add_player(self, last_name: str, first_name: str, birthdate: str, ine: str):
        """Ajouter un nouveau joueur et le sauvegarder"""

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
        joueurs_charges = Player.load_all(filename)

        # vérification que le joueur n'existe pas déja dans les données
        if any(p.ine.upper() == ine_ for p in joueurs_charges):
            raise ValueError("Un joueur avec ce même identifiant existe déjà.")
        player = Player(
            nom=last_name.strip(),
            prenom=first_name.strip(),
            datenaissance=birthdate.strip(),
            ine=ine,
        )
        joueurs_charges.append(player)
        Player.save_all(joueurs_charges , filename)

        return player

    # def list_players(self) -> List[Player]:
    #     """Return all players sorted alphabetically (last_name, first_name)."""
    #     players = load_players()
    #     return sorted(players, key=lambda p: (p.last_name.lower(), p.first_name.lower()))
