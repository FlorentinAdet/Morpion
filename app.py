import tkinter as tk
import tkinter.messagebox as messagebox
import pickle
import os

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
    def __init__(self, root, joueur1, joueur2, taille, tableau=None, symbole_courant='X'):
        self.root = root
        self.root.title("Morpion")
        self.root.protocol("WM_DELETE_WINDOW", self.confirmer_fermeture)

        self.joueur1 = joueur1
        self.joueur2 = joueur2

        self.taille = taille
        self.symbole_courant = symbole_courant

        if tableau is None:
            self.tableau = TableauDeJeu(taille)
        else:
            self.tableau = tableau

        self.boutons = [[None for _ in range(taille)] for _ in range(taille)]

        for ligne in range(taille):
            for col in range(taille):
                self.boutons[ligne][col] = tk.Button(root, text=self.tableau.tableau[ligne][col],
                                                     font=('normal', 20), width=4, height=2,
                                                     command=lambda l=ligne, c=col: self.cliquer_case(l, c))
                self.boutons[ligne][col].grid(row=ligne, column=col)

    def cliquer_case(self, ligne, colonne):
        if self.tableau.jouer(ligne, colonne, self.symbole_courant):
            self.boutons[ligne][colonne].config(text=self.symbole_courant)
            if self.tableau.check_victoire(self.symbole_courant):
                self.afficher_message_victoire()
                self.reinitialiser_partie()
            elif self.tableau.est_rempli():
                self.afficher_message_match_nul()
                self.reinitialiser_partie()
            else:
                self.symbole_courant = 'O' if self.symbole_courant == 'X' else 'X'

    def afficher_message_victoire(self):
        gagnant = self.joueur1 if self.symbole_courant == 'X' else self.joueur2
        pseudo = gagnant.pseudo
        gagnant.nombre_victoires += 1
        messagebox.showinfo("Partie terminée", f"Le joueur {pseudo} a gagné!")
        self.fin_partie()

    def afficher_message_match_nul(self):
        messagebox.showinfo("Partie terminée", "Match nul!")
        self.fin_partie()

    def reinitialiser_partie(self):
        self.tableau = TableauDeJeu(self.taille)
        self.symbole_courant = 'X'

        for ligne in range(self.taille):
            for col in range(self.taille):
                self.boutons[ligne][col].config(text='')

    def demander_rejouer(self):
        choix = messagebox.askquestion("Rejouer", "Voulez-vous rejouer?")
        return choix == 'yes'

    def sauvegarder_partie(self):
        etat_partie = {
            'taille': self.taille,
            'tableau': self.tableau.tableau,
            'symbole_courant': self.symbole_courant
            # Ajoutez d'autres informations d'état si nécessaire
        }

        with open('sauvegarde_partie.pkl', 'wb') as fichier_sauvegarde:
            pickle.dump(etat_partie, fichier_sauvegarde)

    def mettre_a_jour_interface(self):
        for ligne in range(self.taille):
            for col in range(self.taille):
                self.boutons[ligne][col].config(text=self.tableau.tableau[ligne][col])

    def fin_partie(self):
        if self.demander_rejouer():
            self.reinitialiser_partie()
        else:
            os.remove('sauvegarde_partie.pkl')
            self.root.destroy()

    def confirmer_fermeture(self):
        self.sauvegarder_partie()
        self.root.destroy()

class InterfaceConfiguration:
    def __init__(self, root, save=False):
        if save:
            self.charger_partie()
        else:
            self.root = root
            self.root.title("Configuration du jeu")

            self.taille_grille = 3

            self.label_taille = tk.Label(root, text="Taille de la grille :")
            self.label_taille.pack()

            self.entry_taille = tk.Entry(root)
            self.entry_taille.insert(0, "3")
            self.entry_taille.pack()

            self.bouton_lancer = tk.Button(root, text="Lancer le jeu", command=self.lancer_jeu)
            self.bouton_lancer.pack()

    def lancer_jeu(self):
        taille = int(self.entry_taille.get())
        joueur1 = Joueur("Joueur1")
        joueur2 = Joueur("Joueur2")
        self.root.destroy()  # Ferme la fenêtre de configuration pour lancer le jeu
        root = tk.Tk()
        MorpionGUI(root, joueur1, joueur2, taille)

    def charger_partie(self):
        try:
            with open('sauvegarde_partie.pkl', 'rb') as fichier_sauvegarde:
                etat_partie = pickle.load(fichier_sauvegarde)
            taille = etat_partie['taille']
            joueur1 = Joueur("Joueur1")
            joueur2 = Joueur("Joueur2")
            tableau = TableauDeJeu(taille)
            tableau.tableau = etat_partie['tableau']
            symbole_courant = etat_partie['symbole_courant']
            root = tk.Tk()
            MorpionGUI(root, joueur1, joueur2, taille, tableau, symbole_courant)
            # Ajoutez d'autres informations d'état si nécessaires
            # MorpionGUI.mettre_a_jour_interface()
        except FileNotFoundError:
            pass

# Interface de configuration
root_config = tk.Tk()
if os.path.exists('sauvegarde_partie.pkl'):
    charger_sauvegarde = messagebox.askyesno("Charger la sauvegarde", "Une sauvegarde existe. Voulez-vous la charger?")
    if charger_sauvegarde:
        interface_config = InterfaceConfiguration(root_config, True)
    else:
        os.remove('sauvegarde_partie.pkl')
        interface_config = InterfaceConfiguration(root_config)
else:
    interface_config = InterfaceConfiguration(root_config)

root_config.mainloop()
