def addplayer():
    print("\n=== Ajout du Nouveau joueur ===")
    pid = input("Identifiant (AA12345): ").strip().upper()
    last = input("Nom: ").strip()
    first = input("Prénom: ").strip()
    birth = input("Date de naissance (YYYY-MM-DD): ").strip()
    return {"pid": pid, "last": last, "first": first, "birth": birth}
