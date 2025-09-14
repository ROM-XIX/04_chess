from __future__ import annotations

from typing import List

from chess_center.models.player import Player, PlayerId
from chess_center.repositories.base import PlayerRepository
from chess_center.utils.validators import validate_player_id


class PlayerController:
    def __init__(self, repo: PlayerRepository):
        self.repo = repo

    def create_player(self, pid: str, last: str, first: str, birth: str) -> Player:
        validate_player_id(pid)
        p = Player(id=PlayerId(pid), last_name=last, first_name=first, birth_date=birth)
        self.repo.add(p)
        return p

    def list_players_alpha(self) -> List[Player]:
        return sorted(self.repo.list_all(), key=lambda p: (p.last_name.lower(), p.first_name.lower()))
