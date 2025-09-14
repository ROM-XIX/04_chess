# import os


class MainMenu:
    def __init__(self):
        player = 5
        self.player = player
        # players: PlayerController, tournaments: TournamentController):
        # self.players = players
        # self.tournaments = tournaments

    def run(self) -> None:
        while True:
            # os.system('clear')
            print("\n========================================")
            print(" Centre Échecs — Menu principal")
            print("========================================")
            print(" 1) Ajouter un joueur")
            print(" 2) Lister les joueurs (alphabétique)")
            print(" 3) Créer un tournoi")
            print(" 4) Lister les tournois")
            print(" 5) Démarrer un round")
            print(" 6) Clôturer le round (saisir les résultats)")
            print(" 7) Détails d’un tournoi")
            print("----------------------------------------")
            print(" 0) Quitter")
            print("----------------------------------------")
            choice = input(" > Votre choix : ").strip()
            try:
                if choice == "1":
                    print("choix 1")
                elif choice == "2":
                    print("choix 1")
                elif choice == "3":
                    print("choix 1")
                elif choice == "4":
                    print("choix 1")
                elif choice == "5":
                    print("choix 1")
                elif choice == "6":
                    print("choix 1")
                elif choice == "7":
                    print("choix 1")
                elif choice == "0":
                    break
            except Exception as e:
                print(f"Erreur: {e}")
