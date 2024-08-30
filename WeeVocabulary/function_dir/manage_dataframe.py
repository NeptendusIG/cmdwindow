# ----------------------------
#   Créer les listes de mots
#        WeeVocabulary 
# DATE: 04/8/2024
# VERSION: 1.0
# ----------------------------
"""  -- Structures des fonctions disponibles --
Importer Sauvegarde
 - import_data_csv(path)
Obtenir une donnée spécifique du dataframe
- get_ready_words(df)
Ajouter des données
- add_new_words(new_words, dataframe)
    -> create_fr_audio(word, )
    -> translate_to_french(word, )
"""


# -- IMPORTS --
# Modules basiques
import os, logging, sys, time
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Modules renommés
import pandas as pd
# Imports spécifiques
from translate import Translator  # TRANSLATION
from gtts import gTTS  # VOICE GENERATION
# Imports locaux
from utility import File, Settings, GUI


# Paramètres
logger = Settings.setup_logging("debugging")
HEADERS_DATAFRAME = ['date', 'word', 'language', 'count', 'status', 'front', 'back']
STATUS = ['waiting', 'processed']
COUNT_BEFORE_ANKI = 3
count_audio = 0

# -- LISTES COMPLÈTE --
# 1 - Récupérer les données depuis CSV
def import_data_csv(path_csv):
    """Description de la fonction
    path_csv : le chemin d'un fichier en CSV existant 
    """
    df = pd.read_csv(path_csv, sep=",")
    logger.info(f"Les colonnes {df.columns} correspondents à {HEADERS_DATAFRAME}")
    # Some tests ...
    return df


# 2 - Obtenir des données du dataframe
def get_ready_words(df):
    """Obtenir la liste des mots dont le compte est >= 3 et qui n'ont pas été traités
    df: dataframe suivant HEADERS_DATAFRAME
    """
    mask_count = df["count"] >= COUNT_BEFORE_ANKI
    mask_status = df["status"] == "waiting"
    words = df.loc[mask_count & mask_status, "word"]
    return list(words)

# 3 - Ajouter des mots au dataframe
def add_new_words(new_words, dataframe):
    not_known = []
    for word, lang in new_words:
        word = word.strip().lower()
        if word in dataframe["word"].values:
            logger.debug(f"Word already in dataframe: {word}")
            dataframe.loc[dataframe["word"] == word, "count"] += 1
        else:
            not_known.append((word, lang))
        
    for word, lang in not_known:
        row = {"date": time.strftime("%d/%m/%Y"), "word": word, "language": lang, "count": 1, "status": "waiting"}
        if lang == "fr":
            path = create_fr_audio(word, f"data/output/audio_{lang}_{word}")
            row["front"] = path
            row["back"] = word
        elif lang == "en":
            translation_fr = translate_to_french(word)
            if word.lower() in translation_fr.lower():  # Le mot en français a été confondu
                path = create_fr_audio(word, "data/output/fr_audio")
                row["front"] = path
                row["back"] = word
            else:
                row["front"] = word
                row["back"] = translation_fr
        else:
            logger.error(f"Lang Detect: NotManaged {lang} ({word})")
        # dataframe = dataframe.append(row, ignore_index=True)  
        dataframe.loc[len(dataframe)] = row


def create_fr_audio(word, save_path="data/output/fr_audio"):
    """Créer un fichier audio pour le mot donné,
    pre: text
    post: audio file saved """
    global count_audio
    logger.debug(f"Data Completion: Audio: START ({word})")
    # 1 - Rassembler infos (nom et chemins)
    count_audio += 1
    filename = f"{count_audio:0>3}.mp3"
    filepath = f"{save_path}/{filename}"
    # 2 - Créer le fichier audio
    speech = gTTS(text=word, lang='fr', slow=False)
    speech.save(filepath)
    # 3 - Vérifier la création
    if os.path.exists(filepath):
        logger.debug(f"Data Completion: Audio: SUCCEED ({filename})")
    else:
        logger.error(f"Data Completion: Audio: FAILED {word} ({filepath})")
        return ""
    return filepath


def translate_to_french(word, lang_target="fr"):
    translator = Translator(to_lang=lang_target)
    trad = translator.translate(word)
    logger.debug(f"Data Completion: Traduct: {word} -> {trad}")
    return trad


# -- TESTS ET EXEMPLES --
if __name__ == '__main__':
    # Variables
    variable = None
    objet = None
    dataframe = pd.DataFrame({
        "word": ["Boujour", "Bonsoir", "Aurevoir"],
        "count": [3, 4, 5],
        "status": ["waiting", "waiting", "waiting"]
    })
    # Programme test
    print(dataframe)
    print(get_ready_words(dataframe))
