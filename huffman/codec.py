# -*- coding: utf-8 -*-


text = "a dead dad ceded a bad babe a beaded abaca bed"


class TreeBuilder:
    """
    classe capable de construire un arbre binaire
    """

    def __init__(self, text):
        self.text = text

    def occurence(self):   # créé un dictionnaire avec les
        # occurences des différents caractères
        text_occurence = dict()

        for elem in self.text:

            if elem not in text_occurence:  # s'il n'est pas dans le dict, on l'y met
                text_occurence[elem] = 1

            else:  # sinon on incrèmente son occurence
                text_occurence[elem] += 1

        return text_occurence

    List_leaf = []  # la liste des feuilles et noeuds de notre arbre

    def tree(self):
        """
        Renvoie une liste de liste correspondant chaquune à une feuille de l'arbre
        avce les informations suivantes: chaine de charactères, occurance, père,
        bit, fils gauche, fils droit
        """

        text_occurence = self.occurence()
        # trions le dictionnaire par valeur en formant une liste
        text_occurence = sorted(text_occurence.items(), key=lambda x: x[1])

        List_leaf = []  # Nous donnons comme information pour chaque feuille
        # la chaine, l'occurence, le père, le bit et un indice qui
        # sert pour retrouver les fils

        while len(text_occurence) > 1:

            # nous récupérons les infos des deux feuilles
            chain1 = text_occurence[0][0]
            occurence1 = text_occurence[0][1]  # de plus petites occurences
            chain2 = text_occurence[1][0]
            occurence2 = text_occurence[1][1]
            new_chain = chain1+chain2  # il s'agit du père de ces feuilles
            new_occurence = occurence1+occurence2  # voici son occurence

            text_occurence = text_occurence[2:]+[(new_chain, new_occurence)]
            # nous créons les nouvelles feuilles avec les informations voulues
            List_leaf.append([chain1, occurence1, new_chain, 0, 2])
            List_leaf.append([chain2, occurence2, new_chain, 1, 2])
            # l'indice 2 nous aidera pour retrouver les fils
            text_occurence = sorted(text_occurence, key=lambda x: x[1])
            # trions le nouveau dictionnaire

        root = [text_occurence[0][0], text_occurence[0][1], None, None, 2]
        # il s'agit de la racine de notre arbre
        List_leaf.append(root)

        # Nous souhaitons maintenant avoir les fils associés à chaque feuilles
        # lorsqu il y en a.

        List_tree = []

        for fils1 in List_leaf:

            if len(fils1[0]) == 1:

                # La feuille finale n'a pas de fils
                List_tree.append(fils1[:4]+[None, None])
                fils1[4] = 3

            for fils2 in List_leaf:

                for node in List_leaf:

                    if fils1[0]+fils2[0] == node[0] and node[4] == 2:

                        List_tree.append(node[:4]+[fils1[0], fils2[0]])
                        node[4] = 3
        # L'indice 2 ou 3 permet de savoir si le noeud a déjà été traité ou non.
        # nous chercons une correspondance entre les chaines pour trouver les fils

        return List_tree


class Codec():
    """
    Cette class permetrra de coder ou de décoder un text
    en utilisant en entrée un arbre créer avec la class TreeBuilder
    """

    def __init__(self, binary_tree):

        self.binary_tree = binary_tree

    def encode(self, text):
        """
        Cette methode permet de coder un text qui lui est donné en entrée
        """

        Codes = dict()  # nous créons un dictionnaire qui contiendra le code de chaque lettre

        for elem in self.binary_tree:

            if len(elem[0]) == 1:

                code = str(elem[3])
                Codes[elem[0]] = code
                father = elem[2]

                while father != None:  # Nous allons chercher tous les parents en remontant
                    # dans l'arbre
                    for node in self.binary_tree:

                        # nous cherchons des liens de parentés
                        if father == node[0] and node[2] != None:

                            Codes[elem[0]] = str(node[3])+Codes[elem[0]]
                            father = node[2]

                        elif node[2] == None:

                            father = node[2]

        text_encoded = ''
        for elem in text:  # il sufit maintenant d'utiliser le dictionnaire pour

            text_encoded += Codes[elem]  # coder le text

        return int(text_encoded)

    def decode(self, text):
        """
        Cette methode permet de décoder un text donné en entrée
        """

        tree = sorted(self.binary_tree, key=lambda x: x[1])
        # En triant la liste nous sommes sûr d'avoir la racine en derniere position
        text_decoded = ''
        k = 0  # nous alons parcourir l'arbre de haut en bas
        L = list(str(text))  # pour pouvoir conter le nombre de bits du text
        n = len(L)

        while k < (n-1):

            elem = int(L[k])
            # le père sera toujours la racine principale une
            father = tree[-1][0]
            # fois que nous avons parcourus l'arbre jusqu'à une de ses extrèmitès
            for node in tree:  # Nous cherchons le fils correpondant au code du text

                if node[3] == elem and node[2] == father:

                    leaf = node
            k += 1
            while leaf[-1] != None:  # Il faut que la feuille finale n'ai pas de fils

                # nous rennons un nouvel élemnent du text de départ
                elem = int(L[k])
                father = leaf[0]  # nous décendons d'un crant dans l'arbre

                for node in tree:  # Nous chercons le fils correspondant au code du text

                    if node[3] == elem and node[2] == father:
                        leaf = node  # nous avons trouvé la nouvelle feuille
                k += 1
            text_decoded += leaf[0]

        return int(text_decoded)
