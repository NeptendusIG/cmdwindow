# ----------------------------
#   Gére le lien entre le fichier texte et la liste "new_words" de l'application
#        WeeVocabulary 
# DATE: 2024
# VERSION: 2.0
# ----------------------------
"""  -- Structures des fonctions disponibles --
Vérifier/Poser l'environnement de fichiers / clés
Importer les nouveaux mots (+langue)
"""


# -- IMPORTS --
# Basiques :
import os, logging
from utility import File
# Lang Detecting
from lingua import Language, LanguageDetectorBuilder
languages = [Language.ENGLISH, Language.FRENCH]               #, Language.GERMAN, Language.SPANISH, Language.DUTCH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()


# Paramètres
logger = logging.getLogger("debugging")
count_audio = 0

# - Functions -
# 0 - Set Up
main_settings_json = "WeeVocabulary/main_settings.json"
settings_dict = {
    "global": "data/input/new_words.txt",
    "english": {
        "json_waiting_list": "data/output/en_waitlist.json",
        "text_backup_list": "data/backup/en_backup.txt",
        "deck_id": 1,
        "deck_name": "VocEnglish",
        "output_package": "data/output/en_package.apkg",
        "model_with_reverse": True
    },
    "french": {
        "json_waiting_list": "data/output/fr_waitlist.json",
        "text_backup_list": "data/backup/fr_backup.txt",
        "deck_id": 2,
        "deck_name": "Vocabulaire",
        "output_package": "data/output/fr_package.apkg",
        "model_with_reverse": False
    }
}

language_to_code = {
    Language.ENGLISH: "en",
    Language.FRENCH: "fr",
    Language.SPANISH: "es",
    Language.GERMAN: "de",
    Language.ITALIAN: "it",
    Language.PORTUGUESE: "pt",
    # ...
}

code_to_language = {v: k for k, v in language_to_code.items()}

DEFAULT_CSV = "date,word,language,count,status,front,back"

def establish_files():
    """Vérifier existance des fichiers et dossiers nécessaires. Si non, les créer.
    FICHIERS """
    File.create_file_tree(main_settings_json, settings_dict)  # create settings jsonfile
    source_path = File.JsonFile.get_value_jsondict(main_settings_json, "global")
    File.create_file_tree(source_path, can_make_dirs=False)
    data_path = File.JsonFile.get_value_jsondict(main_settings_json, "data")
    File.create_file_tree(data_path, default_content=DEFAULT_CSV)
    File.create_file_tree("data/backup/en_backup.txt")
    File.create_file_tree("data/backup/fr_backup.txt")
    os.makedirs("data/output/fr_audio", exist_ok=True)


# 1 - New words
def get_new_words(source_path):
    """source_path is a txt file"""
    # 1 - Liste des nouveaux mots
    with open(source_path, "r", encoding='utf-8') as file:
        extraction = file.read().split("\n")
    new_words = [word for word in extraction if word != ""]
    logger.debug("new words: %s", new_words)
    # 2 - Associer la langue à chaque mot
    list_with_language = [
        (word, language_to_code[detect_language(word)]) for word in new_words
        ]
    logger.debug("new words with language: %s", list_with_language)
    return list_with_language


def detect_language(word):
    lang = detector.detect_language_of(word)
    logger.debug(f"Lang Detect: {lang} for {word}")
    return lang


"""def saved_word_to_backup(word, field=None, backup_path=None):
    if not (field or backup_path):
        logger.error(f"File: Backup: NoFile Given (for {word})")
        return
    if backup_path is None and field is not None:
        settings_of_chosen_field = File.JsonFile.get_value_jsondict(main_settings_json, field, handle_keyERROR=True)
        backup_path = settings_of_chosen_field["text_backup_list"]
        if not backup_path:
            logger.error(f"File: Backup: NoPath Assigned (to {field})")
            return
    File.add_line(backup_path, word)"""


# -- SANDBOX --
if __name__ == '__main__':
    # - Variables -
    file_to_backup = "/Users//Docs/Objectifs/4_Apprendre/pythonProject/ProjetsEnCours/AutoBackUp/data/input/test.txt"
    backup_directory = "/Users//Docs/Objectifs/4_Apprendre/pythonProject/ProjetsEnCours/AutoBackUp/data/output"
    # - Programme -
