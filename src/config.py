from pathlib import Path

# Racine du projet = dossier où se trouve le script principal (ex: main.py)
BASE_DIR = Path(__file__).resolve().parent
# Sous-dossier pour les données
DATA_DIR = BASE_DIR / "datas"
# Chemins vers les fichiers JSON
PLAYERS_FILE = DATA_DIR / "players" / "players.json"
TOURNAMENTS_FILE = DATA_DIR / "tournaments" / "tournaments.json"

# Création automatique des dossiers
DATA_DIR.mkdir(parents=True, exist_ok=True)
PLAYERS_FILE.parent.mkdir(parents=True, exist_ok=True)
TOURNAMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
