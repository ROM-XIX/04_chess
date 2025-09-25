from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from models.modelstournaments import RoundTournament, Tournament


class TournamentController:
    # ---------- Création / liste / accès ----------
    def add_tournament(
        self,
        nom: str,
        lieu: str,
        nbr_rounds: int = 4,
        list_players: List[Dict[str, Any]] | None = None,
        notes: str = "",
    ) -> Tournament:
        """
        Crée un tournoi. Règles:
        - date_start = maintenant
        - date_end = None (fixée quand le dernier round est clôturé)
        """
        list_players = list_players or []

        tournois = Tournament.load_all()
        if any(t.nom.strip().lower() == nom.strip().lower() for t in tournois):
            raise ValueError("Un tournoi avec ce nom existe déjà.")

        t = Tournament(
            nom=nom.strip(),
            lieu=lieu.strip(),
            date_start=datetime.now(),
            date_end=None,
            nbr_rounds=nbr_rounds,
            current_round=0,
            all_rounds=[],
            list_players=list_players,
            notes=notes,
        )
        tournois.append(t)
        Tournament.save_all(tournois)
        return t

    def list_tournaments(self) -> List[Tournament]:
        return Tournament.load_all()

    def get_tournament(self, nom: str) -> Tournament:
        tournois = Tournament.load_all()
        for t in tournois:
            if t.nom.strip().lower() == nom.strip().lower():
                return t
        raise ValueError("Tournoi introuvable.")

    def _save_updated(self, updated: Tournament) -> None:
        tournois = Tournament.load_all()
        for i, t in enumerate(tournois):
            if t.nom.strip().lower() == updated.nom.strip().lower():
                tournois[i] = updated
                break
        else:
            tournois.append(updated)
        Tournament.save_all(tournois)

    # ---------- Rounds ----------
    def generate_round(self, nom_tournoi: str) -> RoundTournament:
        """
        Crée et démarre un nouveau round :
        - name = "Round N"
        - start_time = maintenant, end_time = None
        - matches = [] (à remplir si tu génères des appariements)
        - append dans Tournament.all_rounds (liste d'objets)
        - current_round = N
        """
        t = self.get_tournament(nom_tournoi)

        if t.current_round >= t.nbr_rounds:
            raise ValueError("Tous les rounds ont déjà été générés.")

        next_index = t.current_round + 1
        r = RoundTournament(name=f"Round {next_index}", start_time=datetime.now(), end_time=None, matches=[])

        # TODO: Générer les appariements ici, remplis r.matches avec des tuples:
        # r.matches = [ (["AB12345", 0.0], ["CD67890", 0.0]), ... ]

        t.all_rounds.append(r)
        t.current_round = next_index

        self._save_updated(t)
        return r

    def add_round_result(
        self,
        nom_tournoi: str,
        round_index: int,  # 1-based (Round 1 -> 1)
        match_index: int,  # 0-based
        s1: float,
        s2: float,
    ) -> None:
        """
        Met à jour le résultat d'un match dans un round.
        Match format: ( [player1, score1], [player2, score2] )
        Scores autorisés typiques: 1.0/0.0, 0.0/1.0, 0.5/0.5
        """
        if (s1, s2) not in ((1.0, 0.0), (0.0, 1.0), (0.5, 0.5)):
            raise ValueError("Scores valides: 1-0, 0-1, 0.5-0.5.")

        t = self.get_tournament(nom_tournoi)
        if not (1 <= round_index <= len(t.all_rounds)):
            raise IndexError("Round inexistant.")

        r = t.all_rounds[round_index - 1]  # objet RoundTournament
        if not (0 <= match_index < len(r.matches)):
            raise IndexError("Match inexistant.")

        (p1, _old1), (p2, _old2) = r.matches[match_index]
        r.matches[match_index] = (
            [p1[0], float(s1)] if isinstance(p1, list) else [p1, float(s1)],
            [p2[0], float(s2)] if isinstance(p2, list) else [p2, float(s2)],
        )

        self._save_updated(t)

    def close_round(self, nom_tournoi: str, round_index: int) -> None:
        """
        Clôture un round :
        - end_time = maintenant
        - si c'est le dernier round prévu (== nbr_rounds), on fixe aussi tournament.date_end = maintenant
        """
        t = self.get_tournament(nom_tournoi)
        if not (1 <= round_index <= len(t.all_rounds)):
            raise IndexError("Round inexistant.")

        r = t.all_rounds[round_index - 1]
        if r.end_time is not None:
            raise ValueError("Ce round est déjà clôturé.")

        r.end_time = datetime.now()

        if round_index == t.nbr_rounds:
            t.date_end = datetime.now()

        self._save_updated(t)
