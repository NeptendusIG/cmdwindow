{TITRE}

Auteur(s) :           {}
Création :            {date}
MODIFICATION :        {date}
Résultats :           {but/résultat du programme}


— SCÉNARIOS D'UTILISATION —
    1. Fenêtre de déverrouillage (psw)
    2. Fenêtre des commandes
        -Accéder/Ajouter/Quitter
    3. Fenêtre de verrouillage & sauvegarde (psw)


— REQUIREMENTS —
os, logging, sys, datetime
Tkinter, ttkbootstrap


— CARACTÉRISTIQUES INTÉRESSANTES / RECOMMANDATIONS -
	CHIFFREMENT XOR.
[...]
	TKINTER.
Tkinter fonctionne sur une boucle de fenêtre principale (tk.TK) et des fenêtre secondaires (tk.Toplevel).
Détruire la fenêtre principale cause des dysfonctionnements (ex. sur filedialogs)
On peut attribuer une boucle mainloop() individuellement à chaque fenêtre.	


- AMÉLIORATIONS POSSIBLES -
Système de recherche de compte plus pratique.
[...]


— VERSIONS ET MODIFICATIONS —
[...]
