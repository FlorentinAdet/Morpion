import tkinter as tk
import json

class Joueur:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.nombre_victoires = 0

class TableauDeJeu:
    def __init__(self, taille):
        self.taille = taille
        self.tableau = [[' ' for _ in range(taille)] for _ in range(taille)]

    def jouer(self, ligne, colonne, symbole):
        if self.tableau[ligne][colonne] == ' ':
            self.tableau[ligne][colonne] = symbole
            return True
        return False

    def est_rempli(self):
        for ligne in self.tableau:
            if ' ' in ligne:
                return False
        return True

    def check_victoire(self, symbole):
        # Vérification des lignes
        for ligne in self.tableau:
            if all(cell == symbole for cell in ligne):
                return True

        # Vérification des colonnes
        for col in range(self.taille):
            if all(self.tableau[row][col] == symbole for row in range(self.taille)):
                return True

        # Vérification des diagonales
        if all(self.tableau[i][i] == symbole for i in range(self.taille)) or \
           all(self.tableau[i][self.taille - 1 - i] == symbole for i in range(self.taille)):
            return True

        return False

class MorpionGUI:
    def __init__(self, root, joueur1, joueur2, taille):
        self.root = root
        self.root.title("Morpion")

        self.joueur1 = joueur1
        self.joueur2 = joueur2

        self.taille = taille
        self.tableau = TableauDeJeu(taille)
        self.symbole_courant = 'X'

        self.boutons = [[None for _ in range(taille)] for _ in range(taille)]

        for ligne in range(taille):
            for col in range(taille):
                self.boutons[ligne][col] = tk.Button(root, text='', font=('normal', 20), width=4, height=2,
                                                      command=lambda l=ligne, c=col: self.cliquer_case(l, c))
                self.boutons[ligne][col].grid(row=ligne, column=col)

    def cliquer_case(self, ligne, colonne):
        if self.tableau.jouer(ligne, colonne, self.symbole_courant):
            self.boutons[ligne][colonne].config(text=self.symbole_courant)

            if self.tableau.check_victoire(self.symbole_courant):
                self.afficher_message_victoire()
                self.enregistrer_scores()
                self.reinitialiser_partie()
            elif self.tableau.est_rempli():
                self.afficher_message_match_nul()
                self.reinitialiser_partie()
            else:
                self.symbole_courant = 'O' if self.symbole_courant == 'X' else 'X'

    def afficher_message_victoire(self):
        gagnant = self.joueur1.pseudo if self.symbole_courant == 'O' else self.joueur2.pseudo
        tk.messagebox.showinfo("Partie terminée", f"Le joueur {gagnant} a gagné!")

    def afficher_message_match_nul(self):
        tk.messagebox.showinfo("Partie terminée", "Match nul!")

    def enregistrer_scores(self):
        scores = {'joueur1': {'pseudo': self.joueur1.pseudo, 'victoires': self.joueur1.nombre_victoires},
                  'joueur2': {'pseudo': self.joueur2.pseudo, 'victoires': self.joueur2.nombre_victoires}}

        with open('scores.json', 'w') as fichier_scores:
            json.dump(scores, fichier_scores, indent=4)

    def reinitialiser_partie(self):
        self.tableau = TableauDeJeu(self.taille)
        self.symbole_courant = 'X'

        for ligne in range(self.taille):
            for col in range(self.taille):
                self.boutons[ligne][col].config(text='')

# Exemple d'utilisation
joueur1 = Joueur("Joueur1")
joueur2 = Joueur("Joueur2")

root = tk.Tk()
morpion_gui = MorpionGUI(root, joueur1, joueur2, taille=3)
root.mainloop()
