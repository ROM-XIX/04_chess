from controller.playercontroller import PlayerController
from tabulate import tabulate

class Menus:
    def __init__(self):
        self
        self.playerscontroller = PlayerController()

    def run(self):
        while True:
            # os.system('clear')
            print("\n")
            print("="*45)
            print(" Club d'Echecs Anonime — Menu principal")
            print("="*45)
            print("  1. Gestion des Joueurs")
            print("  2. Gestion des tournois")
            print("  3. Rapports")
            print("-"*45)
            print(" 00. Quitter")
            print("-"*45)
            choice = input(" > Votre choix : ").strip()
            if choice == "1":
                print("choix 1")
                self.menu_players()
            elif choice == "2":
                print("choix 2")
                self.menu_tournaments()
            elif choice == "3":
                print("choix 3")
            elif choice == "00":
                break
            else:
                self.erreur_saisie(choice)

    # ----------------------- Players -----------------------
    def menu_players(self):
        while True:
            print("\n"+"="*20)
            print("[JOUEURS]")
            print("="*20)
            print("1. Ajouter Player")
            print("2. Liste Des Players")
            print("-"*20)
            print("0. Retour")
            choice = input("> ").strip()

            if choice == "1":
                nom = input("Nom: ").strip()
                prenom = input("Prénom: ").strip()
                datenaissance = input("Date de naissance (YYYY-MM-DD): ").strip()
                ine = input("Identifiant national (AB12345): ").strip().upper()
                try:
                    self.playerscontroller.add_player(nom, prenom, datenaissance, ine)
                    print("Joueur ajouté.")
                except Exception as e:  # noqa: BLE001
                    print(f"Erreur: {e}")

            elif choice == "2":
                joueurs = self.playerscontroller.list_players()
                tableau_joueurs = [j.to_dict() for j in joueurs]
                print(tabulate(tableau_joueurs, headers="keys", tablefmt="grid"))

            elif choice == "0":
                return

            else:
                self.erreur_saisie(choice)

    # ----------------------- Tournaments -----------------------
    def menu_tournaments(self):

        print("\n"+"="*20)
        print("[MENU TOURNOIS]")
        print("="*20)
        print(" 1. Créer Tournoi")
        print(" 2. Inscrire joueurs")
        print(" 3. Démarrer Ronde")
        print(" 4. Saisir résultat")
        print(" 5. Clôturer Ronde")
        print(" 6. Lister Tournoi  ")
        print("-"*20)
        print(" 0. Retour")
        choice = input("> ").strip()

        if choice == "1":
            # nom = input("Nom: ").strip()
            # prenom = input("Prénom: ").strip()
            # datenaissance = input("Date de naissance (YYYY-MM-DD): ").strip()
            # ine = input("Identifiant national (AB12345): ").strip().upper()
            # try:
            #     self.playerscontroller.add_player(nom, prenom, datenaissance, ine)
            #     print("Joueur ajouté.")
            # except Exception as e:  # noqa: BLE001
            #     print(f"Erreur: {e}")
            True
        # elif choice == "2":
        #     # True
        #     # for p in self.players.list_players():
        #     # print(f"- {p.last_name} {p.first_name} ({p.birthdate}) [{p.national_id}]")

        # elif choice == "3":
        #     True
        # elif choice == "4":

        # elif choice == "5":

        # elif choice == "6":

        elif choice == "0":
            return
        else:
            self.erreur_saisie(choice)

        return

    def erreur_saisie(self , choice_):
        self.choice_ = choice_
        print("\n"+"*"*45)
        print(f"votre choix {choice_} n'est pas valide !!!!")
        print("*"*45)
