# 04_chess — notions apprises


Ce README détaille, les notions vus et apprises au travers de ce projet:


## Glossaire - en construction

- I. Les décorateurs
- I.1. **@dataclass**
- I.2. **@staticmethod**
- I.3. **@classemethode**
- II. Configuration des chemins de fichiers.
- II.1. Centraliser la configuration des chemins
- II.2. Importer config.py 
- II.3. Avantages
- III. Annotations 
- III.1. Utilisation de ```from __future__ import annotations```
- III.2. comparatif avec et sans ```from __future__ import annotations```
- III.3. Utilisation de ```from typing import Any, Dict, List```

## I. Les décorateurs

### 1. **@dataclass**

C’est un décorateur fourni par le module standard dataclasses en Python (depuis la version 3.7).
Il sert à générer automatiquement du code répétitif dans une classe qui sert surtout à stocker des données (un “sac d’attributs”).

voici un compartif avec et sans le decorateur.

**Sans @dataclass**
```py
class Joueur:
    def __init__(self, nom, prenom, identifiant):
        self.nom = nom
        self.prenom = prenom
        self.id = identifiant

    def __repr__(self):
        return f"Joueur(nom={self.nom}, prenom={self.prenom}, id={self.id})"
```

**Avec @dataclass**
```py
from dataclasses import dataclass

@dataclass
class Joueur:
    nom: str
    prenom: str
    id: int
```
- Avantages :

    - Génère automatiquement :
    - __init__() (constructeur)
    - __repr__() (affichage lisible)
    - __eq__() (comparaison des objets)
    - Beaucoup plus concis, plus lisible, moins d’erreurs.

#### utiliser une @dataclass


- ✅ Donc en résumé :
    - avec ```j = Joueur("Dupont", "Jean", 1)```
    - ```print(j)``` → affiche directement grâce au __repr__.
    - ```j.nom, j.prenom, j.id``` → accès individuel.
    - ```vars(j) ou asdict(j)``` → dictionnaire de tous les attributs.
        - avec ```from dataclasses import asdict```


### 2. **@staticmethod**

Ajoutons @staticmethod à la classe ```Joueur``` pour voir ce que ça apporte concrètement.

#### La classe actuelle
```py
from dataclasses import dataclass

@dataclass
class Joueur:
    nom: str
    prenom: str
    id: int
```

- 👉 Pour l’instant, elle ne fait que stocker des données.
- Tu peux créer un joueur directement :
```py
j = Joueur("Dupont", "Jean", 1)
```

#### Avec une ```@staticmethod```

- Une méthode statique te permet d’ajouter des utilitaires liés à la classe, sans dépendre d’une instance (```self```).
- Exemple : créer un joueur depuis un dictionnaire (par exemple chargé depuis du JSON).

```py
from dataclasses import dataclass

@dataclass
class Joueur:
    nom: str
    prenom: str
    id: int

    @staticmethod
    def from_dict(d: dict) -> "Joueur":
        """Crée un joueur à partir d’un dictionnaire"""
        return Joueur(d["nom"], d["prenom"], d["id"])
```

#### Utilisation
```py
# Données venant d’un JSON ou d’une API
data = {"nom": "Martin", "prenom": "Alice", "id": 2}

# Création d’un joueur avec la méthode statique
j = Joueur.from_dict(data)

print(j)       # Joueur(nom='Martin', prenom='Alice', id=2)
print(j.nom)   # Martin
```

#### Pourquoi c’est utile ?

- Lisibilité : ```Joueur.from_dict(data)``` est plus clair que ```Joueur(data["nom"], data["prenom"], data["id"])```.

- Éviter la répétition : tu centralises la logique de transformation dans la classe.

- Validation : tu pourrais ajouter des vérifs avant de créer l’objet (ex. s’assurer que l’id est bien un int, que nom n’est pas vide, etc.).


👉 En gros, ```@staticmethod``` te permet d’enrichir ta classe avec des outils pratiques, mais qui n’ont pas besoin d’utiliser ```self```.

Tu ranges la logique “qui appartient à Joueur” dans Joueur, plutôt que d’avoir une fonction qui traîne dans ton fichier Python.

### 3. **@classemethode**

- Différence entre ```self``` et ```cls```

    - ```self``` = représente l’instance (un objet déjà créé).

    - ```cls``` = représente la classe elle-même (pas encore d’instance).

- 👉 Donc :

    - Les méthodes d’instance (```self```) s’utilisent quand tu manipules un objet existant.

    - Les méthodes de classe (```cls```, avec ```@classmethod```) s’utilisent quand tu veux créer de nouveaux objets depuis la classe.

#### Exemple concret

**Avec @classmethod**
```py
@dataclass
class Player:
    nom: str
    prenom: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d["nom"], d["prenom"])
```

Utilisation :
```py
data = {"nom": "Dupont", "prenom": "Jean"}
p = Player.from_dict(data)  # ✔ marche directement
```

Ici, ```cls``` = ```Player```. La méthode **fabrique un nouvel objet**.

**Sans décorateur, avec ```self```**
```py
@dataclass
class Player:
    nom: str
    prenom: str

    def from_dict(self, d: dict):
        return Player(d["nom"], d["prenom"])
```

Utilisation :

```py
data = {"nom": "Dupont", "prenom": "Jean"}
# ❌ ça ne marche pas directement :
p = Player.from_dict(data)  # TypeError: from_dict() missing 1 required positional argument: 'self'
```

- 👉 Pourquoi ? Parce que Python s’attend à ce que tu appelles from_dict sur une instance déjà existante :
```py
tmp = Player("", "")        # tu dois d’abord créer un Player vide
p = tmp.from_dict(data)     # puis recréer un Player depuis le dict
```

➡️ Pas pratique, illogique, et ça oblige à avoir un "faux joueur" juste pour appeler la méthode.

🎯 Conclusion

- Si tu veux créer des objets à partir de données externes (JSON, dict, CSV, etc.), il faut utiliser @classmethod avec cls.

- Si tu remplaces par self, ça ne marche pas car tu n’as pas encore d’objet pour appeler la méthode.

👉 Donc ```@classmethod``` ≠ méthode normale avec ```self``` : ce ne sont pas des alternatives interchangeables, elles ont des usages différents.

## II. Configuration des chemins de fichiers.

Quand tu définis des constantes comme BASE_DIR, DATA_DIR, etc., il est important de pouvoir les réutiliser partout dans ton projet (dans tes modèles, tes contrôleurs, tes vues), sans les réécrire à chaque fois.

### 1. Centraliser la configuration des chemins

Tu peux créer un petit module config.py à la racine de ton projet (à côté de main.py) :
```
mon_projet/
│
├── main.py
├── config.py   👈
├── controllers/
├── models/
├── views/
└── datas/
```

Exemple config.py
```py
from pathlib import Path

# Chemin de base = racine du projet
BASE_DIR = Path(__file__).resolve().parent

# Répertoire datas/
DATA_DIR = BASE_DIR / "datas"

# Fichiers JSON
PLAYERS_FILE = DATA_DIR / "players" / "players.json"
TOURNAMENTS_DIR = DATA_DIR / "tournaments"

# Création automatique des dossiers
DATA_DIR.mkdir(parents=True, exist_ok=True)
PLAYERS_FILE.parent.mkdir(parents=True, exist_ok=True)
TOURNAMENTS_DIR.mkdir(parents=True, exist_ok=True)
```
ici

Ici :

```Path(__file__).resolve()``` = ```/.../projet_04/src/config.py```

```.parent``` = ```/.../projet_04/src```

```.parent.parent``` = ```/.../projet_04``` ✅ (la racine du projet, au-dessus de src).

Du coup ```PLAYERS_FILE``` devient :
```
/home/personnal_user/Documents/OpenClasseRooms/04_echec/projet_04/datas/players/players.json
```
### 2. Importer config.py 

dans tes paquets
Dans models/modelsplayers.py
```py
import json
from pathlib import Path
from typing import List
from dataclasses import dataclass, asdict

from config import PLAYERS_FILE  # 👈 import du chemin

@dataclass
class Player:
    nom: str
    prenom: str
    datenaissance: str
    ine: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def save_all(cls, players: List["Player"]):
        with PLAYERS_FILE.open("w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in players], f, indent=4, ensure_ascii=False)

    @classmethod
    def load_all(cls) -> List["Player"]:
        if not PLAYERS_FILE.exists():
            return []
        with PLAYERS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [cls(**d) for d in data]
```

Dans controllers/playercontroller.py
```py
from datetime import datetime
from models.modelsplayers import Player

class PlayerController:
    def add_player(self, nom: str, prenom: str, datenaissance: str, ine: str):
        try:
            datetime.strptime(datenaissance, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date invalide (format attendu: YYYY-MM-DD).")

        ine = ine.strip().upper()
        if len(ine) != 7 or not ine[:2].isalpha() or not ine[2:].isdigit():
            raise ValueError("INE invalide (format attendu: 2 lettres + 5 chiffres).")

        joueurs = Player.load_all()
        if any(p.ine.upper() == ine for p in joueurs):
            raise ValueError("Un joueur avec ce même identifiant existe déjà.")

        joueur = Player(nom=nom.strip(), prenom=prenom.strip(),
                        datenaissance=datenaissance.strip(), ine=ine)
        joueurs.append(joueur)
        Player.save_all(joueurs)
        return joueur
```

### 3. Avantages

- Tu définis une seule fois les chemins dans config.py.
- Tes modèles et tes contrôleurs importent simplement PLAYERS_FILE ou TOURNAMENTS_DIR.
- Si demain tu veux changer datas/ en data/, tu modifies juste config.py, tout le reste continue à marcher.

## III. Annotations 

Il existe une façon d'ajouter des annotations dans le code, comme des commentaires mais de façon plus spécifique.

```py
from __future__ import annotations
from typing import Any, Dict, List
```


Quand tu définis des constantes comme BASE_DIR, DATA_DIR, etc., il est important de pouvoir les réutiliser partout dans ton projet (dans tes modèles, tes contrôleurs, tes vues), sans les réécrire à chaque fois.

### 1. Utilisation de ```from __future__ import annotations```

Sert à **différer l’évaluation des annotations de type** (les ```: str```, ```-> Player```, etc.) → au lieu de les transformer immédiatement en objets Python, elles restent des **chaînes de caractères (des strings)**, et seront résolues plus tard seulement si besoin.

#### 1.1. Référencer une classe qui n’est pas encore définie

Dans ta classe ```Player```, tu as écrit :
```py 
def j_from_dict(d: dict) -> "Player":
    ...
```

Ici ```"Player"``` est mis entre guillemets, car au moment où Python lit cette ligne, la classe ```Player``` n’est pas encore complètement connue → sinon tu aurais une erreur de NameError.

👉 Avec ```from __future__ import annotations```, tu peux écrire directement :
```py
def j_from_dict(d: dict) -> Player:
    ...
```

- ➡️ Plus besoin des guillemets, ça devient plus lisible.

#### 1.2.Performances

- Sans cette importation, Python doit créer des objets de type réels pour chaque annotation → plus lourd.
- Avec cette importation, Python stocke les annotations **comme des chaînes** et les résout uniquement quand tu y accèdes (par exemple via ```typing.get_type_hints```).
- Donc c’est **plus rapide à charger et plus léger en mémoire**.

#### 1.3 Compatibilité avec les nouvelles versions de Python

Depuis **Python 3.10**, cet import est recommandé car il prépare le terrain à la **PEP 563** et **PEP 649**, qui rendent ce comportement par défaut.

Et à partir de **Python 3.11/3.12**, il est de plus en plus inutile car les annotations différées sont déjà le comportement par défaut.

🔹 Exemple concret

Sans l’import, il faut écrire en string :
```py
@dataclass
class Player:
    nom: str
    prenom: str

    @staticmethod
    def j_from_dict(d: dict) -> "Player":  # obligé de mettre des guillemets
        return Player(d["nom"], d["prenom"])
```
Avec l’import :
```py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Player:
    nom: str
    prenom: str

    @staticmethod
    def j_from_dict(d: dict) -> Player:  # plus besoin des guillemets ✅
        return Player(d["nom"], d["prenom"])
```

🎯 Résumé

- ```from __future__ import annotations``` permet de **reporter l’évaluation des annotations**.
- Avantages :
    - plus besoin de guillemets ```"Player"``` pour référencer une classe définie plus bas,
    - gain de performances,
    - préparation à l’évolution de Python (où ça sera le comportement par défaut).


### 2. Comparatif avec et sans ```from __future__ import annotations```

#### 🔹 Exemple sans from __future__ import annotations
from dataclasses import dataclass
```py
@dataclass
class Player:
    nom: str
    equipe: "Team"   # obligé de mettre des guillemets sinon ça plante

@dataclass
class Team:
    nom: str
    joueur: Player   # ❌ Erreur ici si on ne met pas de guillemets
```

➡️ Sans guillemets → **NameError** car ```Player``` ou ```Team``` ne sont pas encore définies au moment où Python lit les annotations.

#### 🔹 Exemple avec ```from __future__ import annotations```
```py
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Player:
    nom: str
    equipe: Team   # ✅ pas besoin de guillemets

@dataclass
class Team:
    nom: str
    joueur: Player  # ✅ ça marche aussi
```

➡️ Ici ça fonctionne : les annotations sont stockées comme **chaînes de caractères** (```"Team"```, ```"Player"```) et résolues plus tard, donc l’ordre de définition n’a plus d’importance.

#### 🔹 Exemple d’utilisation
```py
p = Player("Jean", None)
t = Team("Les Bleus", p)
p.equipe = t

print(p)
print(t)
```

Résultat :
```py
Player(nom='Jean', equipe=Team(nom='Les Bleus', joueur=...))
Team(nom='Les Bleus', joueur=Player(nom='Jean', equipe=...))
```

#### ✅ Conclusion :

```from __future__ import annotations``` rend le code plus simple et lisible dans les cas :
- d’auto-référence (une classe qui se réfère elle-même dans ses annotations),
- de références croisées entre classes (Player ↔ Team),
- et évite de jongler avec des guillemets partout.


### 3. Utilisation de ```from typing import Any, Dict, List```

#### 🔹 1. ```Any```

- Signifie **“n’importe quel type”**.
- Utile quand tu ne connais pas ou ne veux pas contraindre le type.

Exemple :
```py
from typing import Any

def affiche(val: Any) -> None:
    print(val)

affiche(42)         # int
affiche("Bonjour")  # str
affiche([1, 2, 3])  # list
```

#### 🔹 2. ```Dict```

- Représente un dictionnaire typé.
- Syntaxe : ```Dict[TypeClef, TypeValeur]```.

Exemple :
```py
from typing import Dict

def notes_etudiants() -> Dict[str, float]:
    return {
        "Alice": 15.5,
        "Bob": 12.0,
        "Jean": 18.2
    }
```

➡️ Ici, la clé est une ```str```, la valeur un ```float```.

#### 🔹 3. ```List```

- Représente une liste typée.
- Syntaxe : ```List[TypeDesElements]```.

Exemple :
```py
from typing import List

def joueurs() -> List[str]:
    return ["Jean", "Alice", "Pierre"]
```

➡️ Ici, c’est une liste de ```str```.

🔹 Exemple combiné

Tu peux les combiner pour typer des structures complexes, comme un JSON (liste de dictionnaires) :
```py
from typing import Any, Dict, List

# Une liste de dictionnaires (chaînes -> n'importe quoi)
def charger_json() -> List[Dict[str, Any]]:
    return [
        {"nom": "Dupont", "age": 20, "actif": True},
        {"nom": "Martin", "age": 25, "actif": False},
    ]
```

Ici :
- ```List[...]``` → on attend une liste,
- ```Dict[str, Any]``` → chaque élément est un dictionnaire avec des clés ```str``` et des valeurs de type quelconque (```Any```).

🔹 Résumé

- ```Any``` → valeur de type indéterminé.
- ```Dict[K, V]``` → dictionnaire dont les clés sont du type ```K``` et les valeurs du type ```V```.
- ```List[T]``` → liste contenant des éléments de type ```T```.

💡 À noter : à partir de Python 3.9, tu peux utiliser directement les types natifs :
- ```list[int]``` au lieu de ```List[int]```
- ```dict[str, float]``` au lieu de ```Dict[str, float]```
- mais ```Any``` reste dans ```typing```.