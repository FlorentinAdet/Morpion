# Présentation de mon code du projet

Note : mon code comporte volontairement peu de commentaire car pour moi il parle de lui même. Un code qui a des variables et des méthodes bien nommées définissent ce qu’elles font de par leurs noms.

## **Classes**

### **1. `Joueur`**

- **Description**: Représente un joueur du jeu Morpion. Pour le cas de cet exercice la classe joueur prend que un pseudo en paramètres. Mais cette classe a pour but surtout en cas de mise à jour futur du code si l’on souhaite par exemple implémenter un système de scoring. Cela sera plus facile pour les développeur en ayant déjà pensé à cette mise à jour potentielle.
- **Attributs**:
    - **`pseudo`**: Le pseudo du joueur.
    - **`nombre_victoires`**: Le nombre de victoires du joueur.

### **2. `TableauDeJeu`**

- **Description**: Représente le tableau de jeu du Morpion en back. De plus le tableau est créé en fonction du paramètre taille.

- **Attributs**:
    - **`taille`**: La taille du tableau de jeu.
    - **`tableau`**: Une matrice représentant l'état actuel du jeu. Elle est remplit des caractères vides
- **Méthodes**:
    - **`jouer(ligne, colonne, symbole)`**: Joue un coup dans la case spécifiée par les indices **`ligne`** et **`colonne`** avec le symbole donné. Le coup est joué si seulement la case du tableau est vide.

    
    - **`est_rempli()`**: Vérifie si le tableau est entièrement rempli.

        
    - **`check_victoire(symbole)`**: Vérifie s'il y a une victoire pour le symbole donné. Cette fonction parcours le tableau du jeu pour savoir si toutes les cellules à l’horizontale sont les mêmes, puis en verticale et enfin en diagonales.
        
        

### **3. `MorpionGUI`**

- **Description**: Gère l'interface graphique du jeu Morpion.
- **Attributs**:
    - **`root`**: La fenêtre principale de l'interface.
    - **`joueur1`**, **`joueur2`**: Les instances des joueurs.
    - **`taille`**: La taille du tableau de jeu.
    - **`symbole_courant`**: Le symbole du joueur actuel.
    - **`tableau`**: L'instance du tableau de jeu au cas où le joueur reprend une sauvegarde
    - **`boutons`**: Une matrice de boutons représentant le tableau de jeu dans l'interface.
- **Méthodes**:
    - **`cliquer_case(ligne, colonne)`**: Gère le clic sur une case, met à jour le tableau et vérifie s'il y a une victoire ou un match nul. Gère l’affichage graphique en fonction des différents événement
    
    - **`afficher_message_victoire()`**: Affiche un message de victoire avec le nom du joueur gagnant.
    - **`afficher_message_match_nul()`**: Affiche un message en cas de match nul.
    - **`reinitialiser_partie()`**: Réinitialise le tableau de jeu et le symbole courant.
    - **`demander_rejouer()`**: Demande aux joueurs s'ils veulent rejouer.
    - **`sauvegarder_partie()`**: Sauvegarde l'état actuel du jeu dans un fichier .plk. Sauvegarde des éléments : taille, tableau et le symbole
    
    - **`mettre_a_jour_interface()`**: Met à jour l'interface graphique avec l'état actuel du tableau.
    - **`fin_partie()`**: Gère la fin d'une partie en proposant de rejouer ou de quitter.

### **4. `InterfaceConfiguration`**

- **Description**: Gère l'interface de configuration du jeu Morpion.
- **Attributs**:
    - **`root`**: La fenêtre principale de l'interface.
    - **`taille_grille`**: La taille par défaut du tableau de jeu.
- **Méthodes**:
    - **`lancer_jeu()`**: Lance le jeu avec la taille spécifiée par l'utilisateur, la création de deux objets “joueur”
    - **`charger_partie()`**: Charge une partie sauvegardée grâce aux données présentes dans le fichier.
    

Au lancement du jeu on cherche si une sauvegarde existe. Si une sauvegarde existe on demande aux joueurs s’ils veulent la charger sinon il accède à la fenêtre qui demande la taille du plateau.
