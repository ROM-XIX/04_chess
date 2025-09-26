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
        - Round 1 : appariement aléatoire
        - Rounds suivants : type suisse (scores proches) + pas de revanche
        - BYE attribué si nombre impair
        """
        t = self.get_tournament(nom_tournoi)

        if t.current_round >= t.nbr_rounds:
            raise ValueError("Tous les rounds ont déjà été générés.")
        if not t.list_players:
            raise ValueError("Aucun joueur inscrit dans ce tournoi.")

        scores, deja_joues = self._compute_scores_and_history(t)
        next_index = t.current_round + 1
        r = RoundTournament(name=f"Round {next_index}", start_time=datetime.now(), end_time=None, matches=[])

        if next_index == 1:
            # Pairing aléatoire
            pairs = self._pair_first_round(t.list_players)
            r.matches = self._build_matches(pairs)
        else:
            # Pairing type suisse
            pairs_ids, ids_map = self._pair_next_round(t.list_players, scores, deja_joues)
            r.matches = self._build_matches(pairs_ids, ids_map)

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

    # --- Helpers pairing / scores / historique / tools ---
    def _player_id(self, player_obj_or_id):
        """Retourne l'INE du joueur, que l'on reçoive un dict joueur ou un id direct."""
        if isinstance(player_obj_or_id, dict):
            return player_obj_or_id.get("ine")
        return player_obj_or_id

    def _compute_scores_and_history(self, t):
        """
        Calcule les scores cumulés et l'historique des affrontements pour un tournoi.
        Retourne (scores: dict[ine->float], deja_joues: set[frozenset{id1,id2}]).
        """
        scores = {p.get("ine"): 0.0 for p in (t.list_players or [])}
        deja_joues = set()

        for rnd in t.all_rounds or []:
            for m in rnd.matches or []:
                (p1, s1), (p2, s2) = m
                id1, id2 = self._player_id(p1), self._player_id(p2)
                if id1 is not None:
                    scores[id1] = scores.get(id1, 0.0) + float(s1)
                if id2 is not None and id2 != "BYE":
                    scores[id2] = scores.get(id2, 0.0) + float(s2)
                if id1 and id2 and id1 != "BYE" and id2 != "BYE":
                    deja_joues.add(frozenset({id1, id2}))

        return scores, deja_joues

    def _pair_first_round(self, players):
        """
        Appariement aléatoire pour le 1er round.
        Retourne une liste de paires [(playerA, playerB)|BYE, ...]
        """
        import random

        pool = players[:]
        random.shuffle(pool)

        pairs = []
        while len(pool) >= 2:
            a = pool.pop(0)
            b = pool.pop(0)
            pairs.append((a, b))
        if len(pool) == 1:
            pairs.append((pool.pop(0), "BYE"))
        return pairs

    def _sort_key_for_swiss(self, p, scores):
        """Clé de tri pour ‘type suisse’: score desc puis nom/prénom pour stabilité."""
        return (-scores.get(p.get("ine"), 0.0), p.get("nom", ""), p.get("prenom", ""))

    def _candidate_order(self, p_ine, remaining, scores, ids_map, deja_joues):
        """
        Candidats autorisés pour p_ine dans remaining (jamais rencontrés),
        triés par écart de score croissant puis nom/prénom.
        """
        base = scores.get(p_ine, 0.0)
        cands = []
        for q_ine, _ in remaining:
            if frozenset({p_ine, q_ine}) in deja_joues:
                continue
            diff = abs(scores.get(q_ine, 0.0) - base)
            cands.append((q_ine, diff, ids_map[q_ine].get("nom", ""), ids_map[q_ine].get("prenom", "")))
        cands.sort(key=lambda x: (x[1], x[2], x[3]))
        return [x[0] for x in cands]

    def _backtrack_pairs(self, pool, scores, ids_map, deja_joues):
        """
        Backtracking léger pour appairer sans revanche, en privilégiant
        les scores proches. pool = [(ine, score), ...] trié.
        Retourne list[(ineA, ineB)] ou None si échec.
        """

        def rec(remaining, acc):
            if not remaining:
                return acc[:]
            p_ine, _ = remaining[0]
            rest = remaining[1:]
            for q_ine in self._candidate_order(p_ine, rest, scores, ids_map, deja_joues):
                next_rest = [x for x in rest if x[0] != q_ine]
                acc.append((p_ine, q_ine))
                res = rec(next_rest, acc)
                if res is not None:
                    return res
                acc.pop()
            return None

        return rec(pool, [])

    def _greedy_pairs(self, pool, deja_joues):
        """
        Secours: appariement glouton si le backtracking échoue.
        Essaie d’éviter les re-matches, sinon prend le premier libre.
        """
        pairs = []
        used = set()
        for i, (p_ine, _) in enumerate(pool):
            if p_ine in used:
                continue
            cand = None
            for q_ine, _ in pool[i + 1 :]:
                if q_ine in used:
                    continue
                if frozenset({p_ine, q_ine}) not in deja_joues:
                    cand = q_ine
                    break
            if cand is None:
                for q_ine, _ in pool[i + 1 :]:
                    if q_ine not in used:
                        cand = q_ine
                        break
            if cand is not None:
                pairs.append((p_ine, cand))
                used.add(p_ine)
                used.add(cand)
        return pairs

    def _pair_next_round(self, players, scores, deja_joues):
        """
        Appariement type suisse (scores proches, pas de revanche).
        Retourne list[(ineA, ineB|"BYE")].
        """
        joueurs_sorted = sorted(players, key=lambda p: self._sort_key_for_swiss(p, scores))
        ids_map = {p["ine"]: p for p in joueurs_sorted}
        pool = [(p["ine"], scores.get(p["ine"], 0.0)) for p in joueurs_sorted]

        pairs_ids = self._backtrack_pairs(pool, scores, ids_map, deja_joues)
        if pairs_ids is None:
            pairs_ids = self._greedy_pairs(pool, deja_joues)

        # BYE s’il reste un non apparié
        paired = {x for ab in pairs_ids for x in ab}
        if len(joueurs_sorted) % 2 == 1:
            rest = [ine for ine, _ in pool if ine not in paired]
            if rest:
                pairs_ids.append((rest[0], "BYE"))

        return pairs_ids, ids_map

    def _build_matches(self, pairs, ids_map=None):
        """
        Construit la liste `matches` conforme au modèle:
        [ ([player|ine, 0.0], [player|ine|"BYE", 0.0]), ... ]
        Ici on privilégie le stockage du joueur complet (dict) pour l’affichage.
        """
        matches = []
        for a, b in pairs:
            if isinstance(a, dict):
                a_obj = a
            else:
                a_obj = ids_map[a] if ids_map else a
            if b == "BYE":
                matches.append(([a_obj, 0.0], ["BYE", 1.0]))
            else:
                b_obj = ids_map[b] if ids_map and not isinstance(b, dict) else b
                matches.append(([a_obj, 0.0], [b_obj, 0.0]))
        return matches
