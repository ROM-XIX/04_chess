from views.menus import Menus


def main() -> None:
    # player_repo = JsonPlayerRepository(JSONStore(str(PLAYERS_DIR)))
    # tourn_repo = JsonTournamentRepository(JSONStore(str(TOURNEYS_DIR)))
    # pairing = PairingService()

    # players_ctl = PlayerController(player_repo)
    # tourn_ctl = TournamentController(tourn_repo, player_repo, pairing)

    menu = Menus()
    menu.run()


if __name__ == "__main__":
    main()
