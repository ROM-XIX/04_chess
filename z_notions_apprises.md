# 04_chess — notions apprises


Ce README détaille, les notions vus et apprises au travers de ce projet:


## Glossaire - en construction

## Les décorateurs

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

#### Avec une ```**@staticmethod**```

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