# -*- coding: utf-8 -*-

import numpy as np
from colorama import Fore, Style

# A='abcdefghist'   chaines utilisées pour effectuer des tests.
# B='abcdfghixt'


class Ruler:
    """ 
    Cette classe permet de comprer deux séquences d'ADN ou de chaines de caractères.
    Elle permet de calculer la distance entre les chaines. 
    Le cout de l'insertion, substitution et match entre les deux chaine peut 
    être modifié.
    Elle permet égalemnent de comparer visuellement les deux chaines après 
    optimisation des alignements, avec en rouge les modifications apportées.

    """

    cout_substitution = 1  # On peut modiffier ses couts comme désiré
    cout_insertion = 1
    cout_reussite = 0

    def __init__(self, S, P):
        self.S = S
        self.P = P
        self.s = len(self.S)
        self.p = len(self.P)
        self.cout_substitution = 1 # malus de substitution
        self.cout_insertion = 1 # malus d'insertion
        self.cout_reussite = 0 # pas de malus alignement
        self.distance = 0

    def red_text(self, text):
        """
        permet d'écrire un text en rouge, utilisé pour les modifications
        """
        return f"{Fore.RED}{text}{Style.RESET_ALL}"

    def est_egal(self, a, b):
        """
        permet de comparer a et b et de retourner le cout correspondant 
        respectivement à une reussite ou bien à une substitution
        """
        if a == b:
            return self.cout_reussite
        else:
            return self.cout_substitution

    def compute(self):
        """
        Cette méthode permet de construire la matrice M qui est ensuite utilisée
        pour optimisé le chemin à suivre.
        """

        M = np.zeros((self.p+1, self.s+1)) # Cette matrice indiquera les couts 
        # lors de la realisation des chaines modiffiées
        for k in range(self.p+1): # Nous complétons la première colonne de la matrice
            M[k][0] = k*self.cout_insertion
        for h in range(self.s+1): # Nous complétons la première ligne de la matrice
            M[0][h] = h*self.cout_insertion

        for i in range(1, self.p+1): #On s'occupe de l'intèrieur de la matrice
            for j in range(1, self.s+1):

                valeur1 = M[i-1][j-1] + self.est_egal(self.P[i-1], self.S[j-1])
                valeur2 = M[i-1][j] + self.cout_insertion
                valeur3 = M[i][j-1] + self.cout_insertion

                M[i][j] = min(valeur1, valeur2, valeur3)
        self.M = M
        self.distance = self.M[self.p][self.s] # correspond au cout minimal

    def report(self):
        """
        Permet de remonter dans la matrice et de comparer les deux chaines
        de caractère après modification, sous forme de string top et bottom
        """

        top = []
        bottom = []
        i = self.p
        j = self.s

        while i > 0 and j > 0:  # nous allons parcourir la matrice en partant du bas droit
            score_current = self.M[i][j] # pour arriver à un bord haut ou gauche
            score_diagonal = self.M[i-1][j-1]
            score_sup = self.M[i][j-1]
            score_gauche = self.M[i-1][j]
            # Nous allons maintenant remonter la matrice 
            if score_current == score_diagonal and self.est_egal(self.S[j-1], self.P[i-1]) == self.cout_reussite:
                top.insert(0, self.S[j-1])
                bottom.insert(0, self.P[i-1])
                i -= 1
                j -= 1
            elif score_current == (score_diagonal + self.cout_substitution):

                top.insert(0, f"{self.red_text(self.S[j-1])}")
                bottom.insert(0, f"{self.red_text(self.P[i-1])}")
                i -= 1
                j -= 1
            elif score_current == (score_sup + self.cout_insertion):
                top.insert(0, self.S[j-1])
                bottom.insert(0, f"{self.red_text('=')}")
                j -= 1
            elif score_current == (score_gauche + self.cout_insertion):
                top.insert(0, f"{self.red_text('=')}")
                bottom.insert(0, self.P[i-1])
                i -= 1

        while j > 0:
            top.insert(0, self.S[j-1])
            bottom.insert(0, f"{self.red_text('=')}")
            j -= 1
        while i > 0:
            top.insert(0, f"{self.red_text('=')}")
            bottom.insert(0, self.P[i-1])
            i -= 1
         # Ces deux dernières boucles permettent de revenir à l'extrémité haute
         # et gaucge de notre matrice.

        top = f''.join(top)
        bottom = f''.join(bottom)

        return top, bottom


"""

ruler=Ruler(A,B)   #code utilisé pour effectuer les tests sur le programme.

ruler.compute()

print(ruler.distance)


top,bottom = ruler.report()

print(top) 
print(bottom)
        
"""
