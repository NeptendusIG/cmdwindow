#####################################
#          Titre - Date             #
#####################################
# NOTES :
"""
L'application va se construire autour d'une variable contenant l'entièreté du texte.
-> Donc il ne peut pas y avoir plus d'une fenêtre ouverte à la fois. (sauf pls runtime)
"""
# -- IMPORTS --
# Modules
from utility.utility import GUI
from tkinter import filedialog
import tkinter as tk
import ttkbootstrap as ttk
# Classes
# -- FONCTIONS DÉFINIES --
def ouvrir_fichier(text_bloc):
    """Ouvrir un fichier"""
    if len(text_bloc.get("1.0", tk.END))>5:
        if GUI.ask_yes_no("Le text en cour sera écrasé.", "Voulez-vous enregistrer le fichier avant d'ouvrir un autre?"):
            enregistrer_fichier(text_bloc)
    file_path = GUI.ask_file(context="Choisissez un fichier", types=[("Fichiers texte", "*.txt"), ("Fichiers csv", "*.csv")])
    with open(file_path, 'r') as file:
        text = file.read()
    text_bloc.delete("1.0", tk.END)
    text_bloc.insert("1.0", text)
    setattr(text_bloc, "path", file_path)

def enregistrer_fichier(text_bloc, to_new_file=None, and_delete=False):
    """Enregistrer un fichier"""
    if to_new_file is True or not text_bloc.path:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file_path:
            return False
        text_bloc.path = file_path
    text = text_bloc.get("1.0", tk.END)
    with open(text_bloc.path, 'w') as file:
        file.write(text)
    if and_delete:
        text_bloc.delete("1.0", tk.END)
    return True

def quitter_application(root, text_var):
    """Quitter l'application"""
    result = True
    if len(text_var.get('1.0', tk.END)) > 5:
        if GUI.ask_yes_no("Suppression", "Voulez-vous enregistrer le fichier avant de quitter?"):
            result = enregistrer_fichier(text_var)
    if result:
        root.quit()


# -- VARIABLES INITIALES --
root = GUI.set_basic_window("Text Editor")
main_text = ttk.Text(root)
setattr(main_text, "path", "")


# -- FONCTIONS MAÎTRES --
def demarrer_application(root, text):
    """Lancement de l'application"""
    text.pack(expand=True, fill="both")

    toolbar = ttk.Menu(root)
    root.config(menu=toolbar)

    menu = ttk.Menu(toolbar)
    toolbar.add_cascade(label="Fichier", menu=menu)
    menu.add_command(label="Ouvrir", command=lambda: ouvrir_fichier(text))
    menu.add_command(label="Enregistrer", command=lambda: enregistrer_fichier(text))
    menu.add_command(label="Quitter", command=lambda:quitter_application(text))
    menu.add_command(label="Enregistrer sous", command=lambda: enregistrer_fichier(text))

    root.bind("<Command-o>", lambda event: ouvrir_fichier(text))
    root.bind("<Command-s>", lambda event: enregistrer_fichier(text))
    root.bind("<Command-q>", lambda event: quitter_application(text))
    root.bind("<Command-S>", lambda event: enregistrer_fichier(text))
    root.bind("<Command-n>", lambda event: enregistrer_fichier(text, and_delete=True))

    root.mainloop()


# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -

    # - Programme -
    demarrer_application(root, main_text)



