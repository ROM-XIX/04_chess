
# 1. Initial

## User Story :
```
 « En tant que <acteur>, je souhaite pouvoir <action> [dans le but de <raison>]. »
```

## Critères d’acceptation sous forme de scenario ( langage Gherkin) :
```
Scenario : <User story>
« Étant donné que <situation initial> 
Lorsque <action> 
Alors <résolution> .»
```

# 2. User Story du Projet :


| ID | User Story |
|----|-------------|
| US01 | En tant qu'**administrateur**, je souhaite **ajouter un joueur** afin de pouvoir l'inscrire à un tournoi. |
| US02 | En tant qu'**administrateur**, je souhaite **voir la liste des joueurs** afin de consulter les informations des membres du club. |
| US03 | En tant qu'**administrateur**, je souhaite **créer un tournoi** afin d'organiser des compétitions officielles. |
| US04 | En tant qu'**administrateur**, je souhaite **ajouter des joueurs à un tournoi** afin de constituer la liste des participants. |
| US05 | En tant qu'**arbitre**, je souhaite **gérer les rondes d'un tournoi** afin de suivre son bon déroulement. |
| US06 | En tant qu'**arbitre**, je souhaite **enregistrer les résultats des matchs** afin de mettre à jour le classement. |
| US07 | En tant qu'**administrateur**, je souhaite **générer un rapport sur les joueurs** afin d’avoir une vue d’ensemble des membres du club. |
| US08 | En tant qu'**administrateur**, je souhaite **générer un rapport sur les tournois** afin de suivre l’historique et les résultats. |
| US09 | En tant qu'**utilisateur**, je souhaite **quitter l’application facilement** afin de pouvoir fermer le programme proprement. |


# 3. Critères d'acceptation (Scénarios) — Projet Gestion de Tournoi d'Échecs

> Format :  
> **Scenario : &lt;User Story&gt;**  
> « **Étant donné que** &lt;situation initiale&gt;  
> **Lorsque** &lt;action&gt;  
> **Alors** &lt;résolution&gt;. »

| ID | err |Scénario| Critères |
|----|-----|--------|----------|
| US01| | **Scenario : En tant qu'administrateur, je souhaite ajouter un joueur afin de pouvoir l'inscrire à un tournoi.**<br>|« **Étant donné que** je saisis un nom, un prénom, une date de naissance au format `YYYY-MM-DD` et un INE au format `AA99999` qui n’existe pas encore,<br>**Lorsque** je valide l’ajout du joueur,<br>**Alors** le joueur est créé et persiste dans `datas/players/players.json`. » |
| US01|-err1 | **Scenario : format de date invalide rejeté**<br>|« **Étant donné que** je saisis une date de naissance qui n’est pas au format `YYYY-MM-DD`,<br>**Lorsque** je valide l’ajout,<br>**Alors** une erreur est levée et le joueur n’est pas enregistré. » |
| US01|-err2 | **Scenario : format d’INE invalide rejeté**<br>|« **Étant donné que** je saisis un INE qui ne respecte pas `2 lettres + 5 chiffres` (p.ex. longueur ≠ 7),<br>**Lorsque** je valide l’ajout,<br>**Alors** une erreur est levée et le joueur n’est pas enregistré. » |
| US01|-err3 | **Scenario : INE en doublon rejeté**<br>|« **Étant donné que** un joueur avec le même INE (insensible à la casse) existe déjà,<br>**Lorsque** je tente d’ajouter ce joueur,<br>**Alors** une erreur est levée et le joueur n’est pas enregistré. » |
| US02| | **Scenario : En tant qu’administrateur, je souhaite voir la liste des joueurs afin de consulter les informations des membres du club.**<br>|« **Étant donné que** des joueurs existent dans `players.json`,<br>**Lorsque** j’affiche la liste des joueurs,<br>**Alors** la liste des joueurs est chargée depuis le JSON et affichée en tableau. » |
| US02|-empty | **Scenario : pas de joueurs à afficher**<br>|« **Étant donné que** `players.json` est vide ou inexistant,<br>**Lorsque** j’affiche la liste des joueurs,<br>**Alors** une liste vide est retournée (aucune ligne n’est affichée). » |
| US03| | **Scenario : créer un tournoi**<br>|« **Étant donné que** je saisis un nom de tournoi inédit, un lieu, un nombre total de rounds, et éventuellement une sélection de joueurs existants,<br>**Lorsque** je valide la création,<br>**Alors** le tournoi est créé avec `date_start` initialisée à maintenant, `date_end` à `None`, `current_round` à `0`, les joueurs pré-inscrits enregistrés, et le tournoi est sauvegardé dans `datas/tournaments/tournaments.json`. » |
| US03|-err | **Scenario : nom de tournoi déjà utilisé**<br>|« **Étant donné que** un tournoi avec le même nom existe déjà,<br>**Lorsque** je valide la création,<br>**Alors** une erreur est levée et le tournoi n’est pas créé en doublon. » |
| US04| | **Scenario : inscrire des joueurs à un tournoi**<br>|« **Étant donné que** le tournoi existe et que j’affiche la liste des joueurs enregistrés,<br>**Lorsque** je sélectionne des indices valides et confirme l’inscription,<br>**Alors** les joueurs correspondants sont ajoutés au champ `list_players` du tournoi. » |
| US04|-partial | **Scenario : indices invalides ignorés**<br>|« **Étant donné que** certains indices saisis ne correspondent à aucun joueur,<br>**Lorsque** je confirme l’inscription,<br>**Alors** seuls les indices valides sont pris en compte, les autres sont ignorés. » |
| US05|-R1 | **Scenario : démarrer la première ronde (appariement aléatoire)**<br>|« **Étant donné que** un tournoi existe avec au moins 2 joueurs inscrits et que `current_round` = 0,<br>**Lorsque** je génère une ronde,<br>**Alors** un `Round 1` est créé avec `start_time` à maintenant, des matchs appariés aléatoirement (avec BYE si nombre impair) et `current_round` passe à 1. » |
| US05|-Rn | **Scenario : démarrer une ronde suivante (type suisse, pas de revanche)**<br>|« **Étant donné que** le tournoi comporte déjà au moins une ronde et des scores cumulés,<br>**Lorsque** je génère la ronde suivante,<br>**Alors** les appariements sont calculés en type suisse (scores proches) en évitant les re-matchs et un BYE est attribué si nécessaire. » |
| US05|-err1 | **Scenario : impossible de générer au-delà du nombre total de rounds**<br>|« **Étant donné que** `current_round` est égal au nombre total `nbr_rounds`,<br>**Lorsque** je tente de générer une nouvelle ronde,<br>**Alors** une erreur est levée et aucune ronde supplémentaire n’est créée. » |
| US05|-err2 | **Scenario : impossible de générer sans joueurs**<br>|« **Étant donné que** le tournoi n’a aucun joueur inscrit,<br>**Lorsque** je tente de générer une ronde,<br>**Alors** une erreur est levée. » |
| US06| | **Scenario : saisir le résultat d’un match**<br>|« **Étant donné que** un `Round k` existe avec des matchs indexés de `0..n-1`,<br>**Lorsque** je saisis un score parmi `{(1.0,0.0), (0.0,1.0), (0.5,0.5)}` pour un `match_index` valide,<br>**Alors** le score du match est mis à jour et sauvegardé. » |
| US06|-err1 | **Scenario : score invalide rejeté**<br>|« **Étant donné que** je saisis un couple de scores différent de `{(1.0,0.0), (0.0,1.0), (0.5,0.5)}`,<br>**Lorsque** je valide,<br>**Alors** une erreur est levée et le match n’est pas modifié. » |
| US06|-err2 | **Scenario : round inexistant**<br>|« **Étant donné que** j’indique un index de round hors bornes,<br>**Lorsque** j’essaie d’enregistrer un résultat,<br>**Alors** une erreur `IndexError` est levée. » |
| US06|-err3 | **Scenario : match inexistant**<br>|« **Étant donné que** j’indique un `match_index` hors bornes,<br>**Lorsque** j’essaie d’enregistrer un résultat,<br>**Alors** une erreur `IndexError` est levée. » |
| US05|-close | **Scenario : clôturer une ronde**<br>|« **Étant donné que** un round ouvert existe dans le tournoi,<br>**Lorsque** je le clôture,<br>**Alors** `end_time` de la ronde est défini à maintenant ; si c’est la dernière ronde prévue (`round_index == nbr_rounds`), alors `date_end` du tournoi est également définie. » |
| US05|-close-err | **Scenario : clôture double interdite**<br>|« **Étant donné que** une ronde est déjà clôturée,<br>**Lorsque** je tente de la clôturer à nouveau,<br>**Alors** une erreur est levée et aucune modification n’est faite. » |
| US07| | **Scenario : rapport — liste de tous les tournois**<br>|« **Étant donné que** des tournois existent,<br>**Lorsque** j’affiche la liste des tournois,<br>**Alors** un tableau récapitulatif est affiché (nom, lieu, dates, progression `current_round/nbr_rounds`). » |
| US08| | **Scenario : rapport — nom et dates d’un tournoi**<br>|« **Étant donné que** un tournoi existe,<br>**Lorsque** je demande ses informations,<br>**Alors** le nom, la date de début et la date de fin (ou `None`) sont affichés ; si le tournoi n’existe pas, une erreur “Tournoi introuvable.” est renvoyée. » |
| US08|-players | **Scenario : rapport — joueurs d’un tournoi (ordre alphabétique)**<br>|« **Étant donné que** un tournoi existe avec une liste de joueurs,<br>**Lorsque** je demande la liste des joueurs du tournoi,<br>**Alors** la liste est triée par nom puis prénom et affichée ; si la liste est vide, le message “Aucun joueur inscrit.” est affiché. » |
| US08|-rounds | **Scenario : rapport — rounds et matchs d’un tournoi**<br>|« **Étant donné que** un tournoi comporte une ou plusieurs rondes,<br>**Lorsque** je demande l’historique des rondes,<br>**Alors** chaque ronde (nom, start/end) et la liste des matchs avec leurs scores sont affichés. » |
| US09| | **Scenario : quitter l’application**<br>|« **Étant donné que** je me trouve dans le menu principal,<br>**Lorsque** je choisis l’option Quitter,<br>**Alors** l’application se termine proprement. » |