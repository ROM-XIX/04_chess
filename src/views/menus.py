from tabulate import tabulate

from controller.playercontroller import PlayerController
from controller.tournamentcontroler import TournamentController


class Menus:
    def __init__(self):
        self
        self.playerscontroller = PlayerController()
        self.tournamentscontroller = TournamentController()

    def run(self):
        while True:
            # os.system('clear')
            print("\n")
            print("=" * 45)
            print(" Club d'Echecs Anonime — Menu principal")
            print("=" * 45)
            print("  1. Gestion des Joueurs")
            print("  2. Gestion des tournois")
            print("  3. Rapports")
            print("-" * 45)
            print(" 00. Quitter")
            print("-" * 45)
            choice = input(" > Votre choix : ").strip()
            if choice == "1":
                print("choix 1")
                self.menu_players()
            elif choice == "2":
                print("choix 2")
                self.menu_tournaments()
            elif choice == "3":
                print("choix 3")
                self.menu_rapports()
            elif choice == "00":
                break
            else:
                self.erreur_saisie(choice)

    # ----------------------- Players -----------------------
    def menu_players(self):
        while True:
            print("\n" + "=" * 20)
            print("[JOUEURS]")
            print("=" * 20)
            print("1. Ajouter Player")
            print("2. Liste Des Players")
            print("-" * 20)
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
        print("\n" + "=" * 20)
        print("[MENU TOURNOIS]")
        print("=" * 20)
        print(" 1. Créer Tournoi")
        print(" 2. Inscrire joueurs")
        print(" 3. Démarrer Ronde")
        print(" 4. Afficher la Ronde")
        print(" 5. Saisir résultat")
        print(" 6. Clôturer Ronde")
        print(" 7. Lister Tournois")
        print("-" * 20)
        print(" 0. Retour")
        choice = input("> ").strip()

        if choice == "1":
            nom = input("Nom: ").strip()
            lieu = input("lieu: ").strip()
            try:
                nbr_rounds = int(input("Nombre de Rounds total: ").strip())
            except ValueError:
                print("Nombre de rounds invalide.")
                return
            notes = input("Notes (optionnel): ").strip()

            # Sélection des joueurs existants (optionnel)
            joueurs = self.playerscontroller.list_players()
            tableau_joueurs = [j.to_dict() for j in joueurs]
            if tableau_joueurs:
                print(tabulate(tableau_joueurs, headers="keys", tablefmt="grid", showindex=True))
                selection = input("Indices des joueurs à inscrire (ex: 0,2,5) ou vide pour aucun: ").strip()
                list_players = []
                if selection:
                    try:
                        idxs = [int(x) for x in selection.split(",")]
                        for idx in idxs:
                            if 0 <= idx < len(joueurs):
                                list_players.append(joueurs[idx].to_dict())
                            else:
                                print(f"Indice {idx} ignoré (hors liste).")
                    except Exception:
                        print("Sélection invalide, aucun joueur pré-inscrit.")
                        list_players = []
            else:
                print("Aucun joueur enregistré pour le moment.")
                list_players = []

            try:
                t = self.tournamentscontroller.add_tournament(nom, lieu, nbr_rounds, list_players, notes)
                print(f"Tournoi '{t.nom}' créé avec {len(t.list_players)} joueurs.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "2":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
            except Exception as e:
                print(f"Erreur: {e}")
                return

            joueurs = self.playerscontroller.list_players()
            tableau_joueurs = [j.to_dict() for j in joueurs]
            if not tableau_joueurs:
                print("Aucun joueur disponible.")
                return
            print(tabulate(tableau_joueurs, headers="keys", tablefmt="grid", showindex=True))
            selection = input("Indices des joueurs à ajouter (ex: 0,2,5): ").strip()
            try:
                idxs = [int(x) for x in selection.split(",")] if selection else []
                for idx in idxs:
                    if 0 <= idx < len(joueurs):
                        t.list_players.append(joueurs[idx].to_dict())
                self.tournamentscontroller._save_updated(t)
                print(f"{len(idxs)} joueur(s) ajouté(s) au tournoi '{t.nom}'.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "3":
            nom = input("Nom du tournoi: ").strip()
            try:
                r = self.tournamentscontroller.generate_round(nom)
                print(f"Round généré: {r.name}. Début: {r.start_time}")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "4":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
                if t.current_round == 0 or t.current_round > len(t.all_rounds):
                    print("Aucun round en cours.")
                    return
                r = t.all_rounds[t.current_round - 1]
                print(f"{r.name} — Début: {r.start_time} — Fin: {r.end_time}")
                # Afficher les matchs
                if not r.matches:
                    print("Aucun match saisi.")
                else:
                    rows = []
                    for i, m in enumerate(r.matches):
                        (p1, s1), (p2, s2) = m

                        # p1/p2 peuvent être [ine, score] ou [player_dict, score]
                        def label(p):
                            val = p[0]
                            if isinstance(val, dict):
                                return f"{val.get('nom','')} {val.get('prenom','')} ({val.get('ine','')})"
                            return str(val)

                        rows.append(
                            {
                                "Match": i,
                                "Joueur 1": label((p1, s1)),
                                "Score 1": s1,
                                "Joueur 2": label((p2, s2)),
                                "Score 2": s2,
                            }
                        )
                    print(tabulate(rows, headers="keys", tablefmt="grid"))
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "5":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
            except Exception as e:
                print(f"Erreur: {e}")
                return
            try:
                round_index = int(input("Numéro du round (1-based): ").strip())
                match_index = int(input("Index du match (0-based): ").strip())
                s1 = float(input("Score joueur 1 (1.0/0.5/0.0): ").strip())
                s2 = float(input("Score joueur 2 (1.0/0.5/0.0): ").strip())
                self.tournamentscontroller.add_round_result(nom, round_index, match_index, s1, s2)
                print("Résultat enregistré.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "6":
            nom = input("Nom du tournoi: ").strip()
            try:
                round_index = int(input("Numéro du round (1-based): ").strip())
                self.tournamentscontroller.close_round(nom, round_index)
                print("Round clôturé.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "7":
            try:
                tournois = self.tournamentscontroller.list_tournaments()
                rows = []
                for t in tournois:
                    rows.append(
                        {
                            "Nom": t.nom,
                            "Lieu": t.lieu,
                            "Rounds": f"{t.current_round}/{t.nbr_rounds}",
                            "Début": t.date_start,
                            "Fin": t.date_end,
                            "Joueurs": len(t.list_players) if t.list_players else 0,
                        }
                    )
                if rows:
                    print(tabulate(rows, headers="keys", tablefmt="grid"))
                else:
                    print("Aucun tournoi.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "0":
            return
        else:
            self.erreur_saisie(choice)

    # ----------------------- Rapports -----------------------
    def menu_rapports(self):
        print("\n" + "=" * 70)
        print("[MENU DES RAPPORTS DE TOURNOIS]")
        print("=" * 70)
        print(" 1. Listes de tous les joueurs par ordre alphabétique")  # 1
        print(" 2. Liste de tous les tournois")  # 2
        print(" 3. nom et dates d’un tournoi donné")  # 3
        print(" 4. liste des joueurs du tournoi par ordre alphabétique")  # 4
        print(" 5. liste de tous les tours du tournoi et de tous les matchs du tour")  # 5
        print("-" * 70)
        print(" 0. Retour")
        choice = input("> ").strip()

        if choice == "1":
            joueurs = self.playerscontroller.list_players()
            tableau_joueurs_ = sorted(
                [j.to_dict() for j in joueurs], key=lambda x: (x.get("nom", ""), x.get("prenom", ""))
            )
            print(tabulate(tableau_joueurs_, headers="keys", tablefmt="grid"))

        elif choice == "2":
            try:
                tournois = self.tournamentscontroller.list_tournaments()
                rows = []
                for t in tournois:
                    rows.append(
                        {
                            "Nom": t.nom,
                            "Lieu": t.lieu,
                            "Rounds": f"{t.current_round}/{t.nbr_rounds}",
                            "Début": t.date_start,
                            "Fin": t.date_end,
                            "Joueurs": len(t.list_players) if t.list_players else 0,
                        }
                    )
                if rows:
                    print(tabulate(rows, headers="keys", tablefmt="grid"))
                else:
                    print("Aucun tournoi.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "3":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
                print(f"Tournoi: {t.nom} — Début: {t.date_start} — Fin: {t.date_end}")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "4":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
                rows = sorted(t.list_players or [], key=lambda x: (x.get("nom", ""), x.get("prenom", "")))
                if rows:
                    print(tabulate(rows, headers="keys", tablefmt="grid"))
                else:
                    print("Aucun joueur inscrit.")
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "5":
            nom = input("Nom du tournoi: ").strip()
            try:
                t = self.tournamentscontroller.get_tournament(nom)
                for i, r in enumerate(t.all_rounds, 1):
                    print(f"\n--- {r.name} (début: {r.start_time}, fin: {r.end_time}) ---")
                    if not r.matches:
                        print("  Aucun match.")
                    else:
                        rows = []
                        for j, m in enumerate(r.matches):
                            (p1, s1), (p2, s2) = m

                            def label(val):
                                if isinstance(val, dict):
                                    return f"{val.get('nom','')} {val.get('prenom','')} ({val.get('ine','')})"
                                return str(val)

                            rows.append(
                                {
                                    "Match": j,
                                    "Joueur 1": label(p1),
                                    "Score 1": s1,
                                    "Joueur 2": label(p2),
                                    "Score 2": s2,
                                }
                            )
                        print(tabulate(rows, headers="keys", tablefmt="grid"))
            except Exception as e:
                print(f"Erreur: {e}")

        elif choice == "0":
            return
        else:
            self.erreur_saisie(choice)
        return

    def erreur_saisie(self, choice_):
        self.choice_ = choice_
        print("\n" + "*" * 45)
        print(f"""votre choix {choice_} n'est pas valide !!!!""")
        print("*" * 45)
