#############################
#     WeeVocabulary      #
#      Class name       #
#        Date//         #
#############################
# NOTES :
"""

"""
# IMPORTS
import os, sys
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from utility import GUI, File, Settings
import tkinter as tk
import ttkbootstrap as ttk

# SETTINGS
logger = Settings.setup_logging("debugging")


# APPLICATIONS
class NewWordsListApp:

    def __init__(self, master, words_lang):
        self.master = master
        self.entries = []
        logger.info("New words list: %s" % words_lang)

        for idx, (word, lang) in enumerate(words_lang):
            style = ttk.Style()
            style.configure("Small.TButton", padding=(5, 1), font=('Arial', 14))
            style = ttk.Style()
            style.configure("Small.TEntry", padding=(5, 1), font=('Arial', 14))

            mot = ttk.Entry(self.master, width=10, style="Small.TEntry")
            mot.grid(row=idx, column=1)
            mot.insert(0, word)

            info = ttk.Entry(self.master, width=4, style="Small.TEntry")
            info.grid(row=idx, column=2)
            info.insert(0, lang)

            delete_button = ttk.Button(self.master, text="Delete", command=lambda idx=idx: self.delete_line(idx), style="Small.TButton")
            delete_button.grid(row=idx, column=0)

            self.entries.append((mot, info, delete_button))

    def delete_line(self, idx):
        if 0 <= idx < len(self.entries):
            mot, info, delete_button = self.entries[idx]
            mot.grid_forget()  # Supprimer le widget de la grille
            info.grid_forget()  # Supprimer le widget de la grille
            delete_button.grid_forget()
            self.entries.pop(idx)  # Supprimer les références des widgets de la liste

            # Réorganiser les widgets restants
            for i in range(idx, len(self.entries)):
                self.entries[i][0].grid(row=i, column=1)
                self.entries[i][1].grid(row=i, column=2)
                self.entries[i][2].config(command=lambda idx=i: self.delete_line(idx))  # Mettre à jour l'index du bouton de suppression
                self.entries[i][2].grid(row=i, column=0)

    def get_words(self):
        return [(mot.get(), info.get()) for mot, info, _ in self.entries]
        

class ReadyWordsApp():
    def __init__(self, master, words) -> None:
        self.master = master

        for word in words:
            label = ttk.Label(self.master, text=word, font=("Arial", 15), anchor="w")
            label.pack(expand=True, fill="both")


HEADERS_DATAFRAME = ['date', 'word', 'language', 'count', 'status', 'front', 'back']
class ShowDataFrame():
    def __init__(self, master, df) -> None:
        self.master = master
        ttk.Style().configure("Black.TLabel", foreground="black", padding=(1, 1))

        ttk.Label(self.master, text="word", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=0, row=0)
        ttk.Label(self.master, text="lang", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=1, row=0)
        ttk.Label(self.master, text="count", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=2, row=0)
        ttk.Label(self.master, text="status", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=3, row=0)
        ttk.Separator(self.master, orient="vertical").grid(column=4, row=0, sticky="ns")
        ttk.Label(self.master, text="front", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=5, row=0)
        ttk.Label(self.master, text="back", font=("Arial", 12, "bold"), style="Black.TLabel").grid(column=6, row=0)
        for idx, row in df.iterrows():
            idx += 1
            ttk.Label(self.master, text=row["word"], font=("Arial", 12), style="Black.TLabel").grid(column=0, row=idx)
            ttk.Label(self.master, text=row["language"], font=("Arial", 12), style="Black.TLabel").grid(column=1, row=idx)
            ttk.Label(self.master, text=row["count"], font=("Arial", 12), style="Black.TLabel").grid(column=2, row=idx)
            ttk.Label(self.master, text=row["status"], font=("Arial", 12), style="Black.TLabel").grid(column=3, row=idx)
            ttk.Separator(self.master, orient="vertical").grid(column=4, row=idx, sticky="ns")
            ttk.Label(self.master, text=row["front"], font=("Arial", 9), style="Black.TLabel").grid(column=5, row=idx)
            ttk.Label(self.master, text=row["back"], font=("Arial", 9), style="Black.TLabel").grid(column=6, row=idx)




if __name__ == '__main__':
    objet = [("Bonjour", "en"), ("Aurevoir", "fr"), ("Hello", "en"), ("Hi", "en")]
    df = pd.DataFrame({
        "word": ["Boujour", "Bonsoir", "Aurevoir"],
        "count": [3, 4, 5],
        "status": ["waiting", "waiting", "waiting"],
        "language": ["fr", "fr", "fr"],
        "front": ["Hello", "Hello", "Hello"],
        "back": ["Bonjour", "Bonjour", "Bonjour"]
    })

    wind = GUI.set_basic_window()
    if 0:
        frame = ttk.Frame(wind)
        frame2 = ttk.Frame(wind)
        # tests
        App = NewWordsListApp(frame, objet)
        ReadyWordsApp(frame2, ["Bonjour", "Aurevoir", "Hello"])
        frame.pack(pady=0)
        frame2.pack(pady=10, padx=20)
    if True:
        # df = File.JsonLine.made_dataframe_from_jsonline("data/words.json")
        ShowDataFrame(wind, df)
    wind.mainloop()

