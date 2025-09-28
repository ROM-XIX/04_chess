# I. L'objectif du code :

L'objectif du code, de ce projet est décrit dans le fichier ```Spécification+technique_Développez+un+programme+logiciel+en+Python.pdf``` dans le répertoire docs.

# II. Procédure d'utilisation :

## 1. Récupérer le repo depuis github :

Téléchargez le dépôt GitHub depuis le lien du dépôt github.

Pour cela une fois sur la page du dépôt github, dans la barre au dessous du nom du dépôt, cliquez sur le bouton **<>CODE** puis, dans l’onglet local, cliquez sur  **DownloadZIP**,
enregistrez le fichier ZIP à l’emplacement souhaité sur votre ordinateur.

Puis extraire le zip. Vous aurez l'ensemble des fichiers pour l'utilisation du code.

## 2.  Créer un environnement Python :

### 2.1. <ins>Ouvrir un terminal</ins>
Ouvrez une fenêtre de terminal sur votre système Linux.

### 2.2 <ins>Vérifier la version de Python installée</ins>
Vérifiez que Python 3 est installé en exécutant :
```bash
python3 --version
```
Vous devriez voir une version du type ` Python 3.x.x. `
Si ce n’est pas le cas, installez Python 3 avec la commande adaptée à votre distribution (par exemple : sudo apt install python3).

### 2.3 <ins>Créer un environnement dans le projet</ins>
Afin de ne pas corrompre votre système, nous allons créer un environnement dans le projet.

Allez dans le répertoire du projet avec la commande :
```bash
cd /mon_chemin_d_acces_local/../04_chess
```

Créez un environnement virtuel avec la commande :
```bash
python3 -m venv .env
```
Ici, `.env` est le nom de l’environnement. Vous pouvez le modifier si besoin.

### 2.4 <ins>Activer l’environnement virtuel</ins>

Activez l’environnement avec :
```bash
source .env/bin/activate
```

Vous devriez voir le nom de l’environnement (`(.env)`) apparaître au début de la ligne de commande.
```bash
>(.env) user@pcname :/mon_chemin_d_acces_local/../04_chess
```

### 2.5 <ins>Vérifier que l’environnement est vide</ins>
Listez les paquets installés :
```bash
pip list
```

Vous ne devriez voir que `pip`, `setuptools` et `wheel`.

### 2.6 <ins>Installer les dépendances du projet</ins>
Installez les dépendances utiles au bon fonctionnement du code avec la commande suivantee :
```bash
pip install -r requirements.txt
```

### 2.7 <ins>Pour désactiver l'environnement</ins>
une fois que vous aurez fini d'utiliser le code vous pourrez déactiver l'environnement avec la commande suivante:
```bash
deactivate
```

## 3. Lancer le code Python.

Nous pouvons lancer l'exécution du code Python à partir du fichier `main.py`.  
Pour cela, dans le terminal, exécutez les commandes suivantes :

```bash
# placez-vous dans le répertoire contenant main.py
cd /mon_chemin_d_acces_local/../04_chess/src

# exécutez le fichier main.py avec la commande suivante
python3 -m main
```
Dans votre terminal vous devriez voir apparaître le premier menu de l'applications comme suite :

```
=============================================
 Club d'Echecs Anonime — Menu principal
=============================================
  1. Gestion des Joueurs
  2. Gestion des tournois
  3. Rapports
---------------------------------------------
 00. Quitter
---------------------------------------------
 > Votre choix :
```

#  III. Utiliser et Générer un nouveau fichier flake8-html.   

Une fois dans l'environnement virtuel. afin de générer un nouveau fichier ```html``` du rapport flake8 dans un répertoire ```flake-report```

```bash
$ flake8 --format=html --htmldir=flake-report
```

