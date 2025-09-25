# 04_chess — Procédure de création de projet Python

Ce README détaille, étape par étape, la création d’un projet Python avec un environnement virtuel, la mise en place de **Black**, **Flake8** (longueur de ligne 119), **isort**, et la publication sur GitHub via SSH (`git@github.com:bob_BOBY/04_chess.git`).

---

## 0) Prérequis

- **Python** 3.10+ (recommandé : 3.11 ou 3.12)
- **Git**
- Accès **SSH** à GitHub (une clé ajoutée à votre compte)

Vérifications rapides :

```bash
python3 --version
pip --version
git --version
ssh -T git@github.com
```

> Si la dernière commande affiche un message vous saluant par votre pseudo, votre SSH est OK.

---

## 1) Créer le dossier du projet

```bash
mkdir 04_chess && cd 04_chess
```

Arborescence de base (proposée) :

```
04_chess/
├── src/
│   └── chess_app/__init__.py
└── tests/
```

```bash
mkdir -p src/chess_app tests
touch src/chess_app/__init__.py
```

---

## 2) Créer et activer l’environnement virtuel

### macOS / Linux (Bash/Zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Mettre à jour `pip` :
```bash
python -m pip install --upgrade pip
```

---

## 3) Installer les outils de qualité de code

Installez **Black**, **Flake8** et **isort** (et, en option, **pytest** pour les tests) :

```bash
pip install black flake8 isort
# optionnel
pip install pytest
```

Vous pouvez enregistrer ces dépendances dans un fichier dédié au dev :
```bash
echo -e "black\nflake8\nisort" > requirements-dev.txt
```

Installation depuis le fichier (ultérieurement) :
```bash
pip install -r requirements-dev.txt
```

---

## 4) Configurer Black, isort et Flake8

### 4.1 `pyproject.toml` (Black & isort)
Créez un fichier **pyproject.toml** à la racine :

```toml
[tool.black]
line-length = 119
target-version = ["py311", "py312"]  # adaptez à votre version
include = "\\.pyi?$"
exclude = """
/(\n  \\.venv\n  | \\.git\n  | __pycache__\n  | build\n  | dist\n)/
"""

[tool.isort]
profile = "black"
line_length = 119
py_version = 311
skip = [
  ".venv",
  "build",
  "dist",
]
```

> **Pourquoi `profile = "black"` ?** Pour que isort et Black aient un style cohérent. On force aussi `line_length = 119` pour correspondre à la contrainte demandée.

- **Note :**

  Le fichier pyproject.toml sert à centraliser la configuration de tes outils Python (ici Black et isort). Détaillons :

  - Partie [tool.black]

    - line-length = 119 → Black reformate ton code pour que chaque ligne fasse max 119 caractères.
    - target-version = ["py311"] → Indique à Black quelle version de Python tu utilises (ici 3.11).
    - Ça peut influencer certains détails de syntaxe.
    - include = "\.pyi?$" → Black ne s’occupe que des fichiers *.py et *.pyi.
    - exclude = """ ... """ → Black ignore certains dossiers (env virtuel, .git, __pycache__, etc.).

  ⚠️ En pratique, include et exclude sont déjà gérés par défaut par Black. Donc tu n’es pas obligé de les écrire, sauf si tu veux personnaliser.

  - Partie [tool.isort]

    - profile = "black" → isort formate les imports de façon compatible avec Black.
    - line_length = 119 → même limite que Black.
    - py_version = 311 → précise la version de Python (ici 3.11).
    - skip = [...] → ignore certains dossiers (.venv, build, dist).

  > possibilité de simpléfier le fichier par 

  ```toml
  [tool.black]
  line-length = 119
  target-version = ["py311"]

  [tool.isort]
  profile = "black"
  line_length = 119
  ``` 

### 4.2 `.flake8`
Créez un fichier **.flake8** à la racine :

```ini
[flake8]
max-line-length = 119
extend-ignore = E203, W503
exclude =
    .venv,
    .git,
    __pycache__,
    build,
    dist
per-file-ignores =
    __init__.py: F401
```

> `E203` et `W503` sont ignorés pour être compatibles avec le formatage de Black.

- **Note :** 

  - 🔎 Détail des erreurs
    - E203 – Whitespace before ‘:’
    - Exemple :
      ```
      # Erreur E203
      if x[1 : 3]:  
          print("ok")
      ```

      - Flake8 (via pycodestyle) considère qu’il ne faut pas d’espace avant : dans une slice.
      - Black, lui, formate avec un espace → x[1 : 3].
      - Pour éviter un faux positif entre Flake8 et Black, on ignore E203.

    - W503 – Line break before binary operator
    - Exemple :
      ```
      # Erreur W503
      result = (a
                + b)
      ```

      - Flake8 considère que c’est incorrect de mettre le retour à la ligne avant l’opérateur (+).
      - Mais PEP 8 moderne recommande l’inverse → retour à la ligne avant l’opérateur plutôt qu’après.
      - Black applique cette convention moderne, donc pour rester cohérent, on ignore W503.

    - ✅ En résumé

      - E203 : conflit avec la manière dont Black gère les slices.
      - W503 : conflit avec la manière dont Black gère les retours à la ligne avec opérateurs.

    C’est pourquoi quasiment tous les projets utilisant Black ajoutent extend-ignore = E203, W503 dans .flake8.



---

## 5) Lancer les outils

Formater et trier les imports :
```bash
isort .
black .
```

Analyser avec Flake8 :
```bash
flake8
```

Conseil : vous pouvez ajouter des scripts pratiques dans un **Makefile** (optionnel) :
```makefile
format:
	isort . && black .

lint:
	flake8

test:
	pytest -q
```

- **Note :**

  Ajouter un fichier `Makefile` à la racine du projet comme le fichier `.flake8`
  - Qu’est-ce qu’un Makefile ?
    
    - Un Makefile contient des cibles (targets) avec des commandes à exécuter.
    - On lance une cible avec `make <cible>`, p. ex. `make format`.
    - Important : les lignes de commande doivent commencer par une tabulation (pas des espaces), sinon make râle.


---

## 6) (Optionnel mais conseillé) Hooks `pre-commit`

Pour automatiser le formatage et le lint à chaque commit :

```bash
pip install pre-commit
```

Créez **.pre-commit-config.yaml** :
```yaml
exclude: ^(.env_04|build|venv|.venv])

repos:
  - repo: local
    hooks:
      - id: black
        name: black
        entry: black .
        language: system
        types: [python]
      - id: isort
        name: isort
        entry: isort .
        language: system
        types: [python]
      - id: flake8
        name: flake8
        entry: flake8
        language: system
        types: [python]
```

Activez les hooks :
```bash
pre-commit install
# pour lancer sur tout le repo une première fois
pre-commit run --all-files
```

> Cette configuration "locale" utilise les exécutables de votre venv actif (pas besoin de fixer des versions `rev:`).

- Note : il est possible qu'il faille sauté cette étape et d'initialiser le git avant.

---

## 7) `.gitignore`

Ajoutez un **.gitignore** minimal :

```
# venv
.venv/

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg-info/

# OS/IDE
.DS_Store
.idea/
.vscode/

# Builds
build/
dist/

# Tests/coverage
.pytest_cache/
.coverage
htmlcov/
```

---

## 8) Initialiser le dépôt Git local

```bash
git init
# si besoin, définir la branche principale comme "main"
git branch -M main

git add .
git commit -m "Init Python project: black/flake8/isort (line length 119)"
```

---

## 9) Lier le dépôt local au dépôt GitHub (SSH)

URL fournie : `git@github.com:bob_BOBY/04_chess.git`

```bash
git remote add origin git@github.com:bob_BOBY/04_chess.git
git remote -v
```

Premier push :
```bash
git push -u origin main
```

> Si la branche distante s’appelle `master`, adaptez : `git push -u origin master`.

---

## 10) Vérification rapide

- Black et isort respectent bien une **longueur de ligne = 119**.
- `flake8` ne remonte pas d’erreurs (ou des erreurs attendues).
- Le dépôt est en ligne sur GitHub et accessible en SSH.

---

## 11) Commandes utiles (mémo)

```bash
# Activer l’environnement
source .venv/bin/activate            # macOS/Linux
.\.venv\Scripts\Activate.ps1        # Windows PowerShell

# Qualité de code
isort . && black .
flake8

# Git
git status
git add -A
git commit -m "message"
git pull --rebase origin main
git push origin main
```

Bon code ! 🎯

## 12) Déindexer et supprimer .venv du GITHUB

j'ai mon répertoire .venv/ qui est dans mon .gitignore et qui et pourtant dans mon github j'ai push mon .venv. comment supprimer mon .venv de mon github et des indexer min .venv ? 

Pas de panique 🙂
```bash.gitignore``` n’agit **que sur les fichiers non suivis**. Si tu as déjà commit ton ```bash.venv/```bash, il faut le **désindexer** (arrêter de le suivre) puis pousser la suppression.

Étapes rapides (sans toucher à tes fichiers locaux)

1. Vérifie que la règle ignore est correcte (à la racine du repo) :
```bash
.venv/
```

2. Désindexe le dossier (le supprime de l’index Git, sans supprimer tes fichiers locaux) :
```bash
git rm -r --cached .venv
```

3. Confirme que .gitignore est pris en compte et ajoute-le s’il a changé :
```bash
git add .gitignore
```

4. Commit la suppression côté Git :
```bash
git commit -m "Stop tracking .venv (ignored)"
```

5. Pousse vers GitHub :
```bash
git push
```

Après ça, le dossier ```.venv/``` disparaîtra du dépôt à **partir de ce commit**, et Git ne le suivra plus.

**Pourquoi c’est arrivé ?**

- ```.gitignore``` n’enlève pas de l’index ce qui a déjà été ajouté/commit auparavant.
- Il faut donc un ```git rm --cached``` pour “désindexer”.

**Vérifications utiles**

Tester qu’un fichier de ```.venv/``` est bien ignoré :
```bash
git check-ignore -v .venv/pyvenv.cfg
```

(La sortie doit montrer la règle qui l’ignore.)