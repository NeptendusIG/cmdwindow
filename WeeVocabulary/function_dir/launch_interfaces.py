# ----------------------------
#   Créer les listes de mots
#        WeeVocabulary 
# DATE: 04/8/2024
# VERSION: 1.0
# ----------------------------
"""  -- Structures des fonctions disponibles --
Classement 1
 - function_name(arg1)
Classement 2
- f2(arg1)
"""


# -- IMPORTS --
import os, logging
# Modules renommés
import tkinter as tk
import ttkbootstrap as ttk
# Imports locaux
from utility import File, Settings, GUI
from class_dir.interfaces import NewWordsListApp, ReadyWordsApp, ShowDataFrame


# Paramètres
logger = Settings.setup_logging("debugging")


# -- LISTES COMPLÈTE --
# 1 - La Frame des trois tableaux (NewWords, Ready, DataFrame)
def add_three_board(master, new_words, total_dataframe, ready_list, button_dict):
    """Ajoute les trois tableau à une fenêtre"""
    # 1 - Créer les styles
    set_styles()
    # Default for all : space=5; pad=2; style for Frame="Black.TFrame"
    # 2 -Créer les cadres des tableaux
    add_func = lambda words, df=total_dataframe: button_dict["ADD"](words, dataframe=df)
    create_func = lambda df=total_dataframe: button_dict["CREATE"](df)
    board_for_new_words(master, new_words, add_func)
    board_for_ready_words(master, ready_list, create_func)
    board_for_data_frame(master, total_dataframe)


# 2 - Les trois listes/tableaux (séparement)
def board_for_new_words(master, new_words, function, style="Black.TFrame", pad=2, space=5):
    """Crée un cadre pour les nouveaux mots"""
    frame = ttk.Frame(master, style=style, padding=pad)
    # Dans le cadre
    table = ttk.Frame(frame)
    App = NewWordsListApp(table, new_words)
    table.pack(side="bottom")
    ttk.Label(frame, text="New Words", font=("Arial", 17), style="Blue.TLabel", anchor="center").pack(side="left", fill="both",  expand=True)
    ttk.Button(frame, text="Add", command=lambda :add_words(App, function)).pack()
    # Affichage du cadre
    frame.grid(row=0, column=0, sticky="n", padx=space, pady=space)


def board_for_ready_words(master, ready_list, fonction, style="Black.TFrame", pad=2, space=5):
    """Crée un cadre pour les mots prêts"""
    frame = ttk.Frame(master, style=style, padding=pad)
    # Dans le cadre
    table = ttk.Frame(frame)
    ReadyWordsApp(table, ready_list)
    table.pack(side="bottom", expand=True, fill="both")
    ttk.Label(frame, text="Ready", font=("Arial", 17), style="Blue.TLabel", anchor="center").pack(side="left", fill="both",  expand=True)
    ttk.Button(frame, text="Create", command=fonction).pack()
    # Affichage du cadre
    frame.grid(row=1, column=0, sticky="we", pady=space, padx=space)


def board_for_data_frame(master, total_dataframe, style="Black.TFrame", pad=2, space=5):
    """Crée un cadre pour le dataframe"""
    frame = ttk.Frame(master, style=style, padding=pad)
    # Dans le cadre
    table = ttk.Frame(frame)  # Tableau
    ShowDataFrame(table, total_dataframe)
    table.pack()
    # Affichage du cadre
    frame.grid(row=0, rowspan=2, column=1, sticky="ns", padx=space, pady=space)


# 3 - ~Wrapper pour les fonctions des boutons
def add_words(App, function):
        """Ajoute les nouveaux mots au dataframe, avec les Audio/Traduction"""
        words = App.get_words()
        function(words=words)


def set_styles():
    """Cadres noirs, titres bleus"""
    style = ttk.Style()  # Style des cadre (Frame)
    style.configure("Black.TFrame", borderwidth=0, relief="solid")
    style.map("Black.TFrame", background=[('!active', 'black')])
    style = ttk.Style()  # Style des titres (Label)
    style.configure("Blue.TLabel", foreground="blue")