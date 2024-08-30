#####################################
#   Learn Vocabulary - 15/2/24      #
#####################################
# NOTES :
"""
"""
# -- IMPORTS --
import sys, os, subprocess
# Modules
from utility import File, GUI, Settings
from function_dir.manage_text import get_new_words, establish_files # add_new_words, create_cards_from_waitlist, 
from function_dir.manage_dataframe import import_data_csv, get_ready_words, add_new_words
from function_dir.launch_interfaces import add_three_board
from function_dir.anki_maker import make_ankipackage_from_bituples
# typing
from pandas import DataFrame


# Logging
logger = Settings.setup_logging("main")
logger.info("Start")



# -- FONCTIONS DÉFINIES --
def choose_location_for_input_words():
    new_dir_location = File.ask_dir()
    if new_dir_location is None or not os.path.exists(new_dir_location):
        logger.error(f"OP:Change Location: CANCELED (DirNotFound: {new_dir_location})")
        return
    new_file_path = os.path.join(new_dir_location, "new_words.txt")
    File.JsonFile.set_value_jsondict("WeeVocabulary/main_settings.json", "global", new_file_path,
                                     can_modify_key=True, can_add_key=False)
    logger.info(f"OP:Change Location: CHANGED ({new_file_path})")
    File.create_file_tree(new_file_path, can_make_dirs=False)


def get_data():
    """Charge the data for the application
    -> New words, managed words, words ready to be processed (to Anki)
    param: settings_path, source_path, data_path"""
    # 1 - New words
    source_path = File.JsonFile.get_value_jsondict("WeeVocabulary/main_settings.json", "global", handle_keyERROR=False)
    new_words = get_new_words(source_path)
    # 2 - Dataframe of managed words
    data_path = File.JsonFile.get_value_jsondict("WeeVocabulary/main_settings.json", "data", handle_keyERROR=False)
    words_df = import_data_csv(data_path)
    # 3 - List of words ready to be processed
    ready_list = get_ready_words(words_df)
    return new_words, words_df, ready_list


def actualiser_nouveaux_mots(mots: list[tuple[str, str]], dataframe: DataFrame):
    """Bouton ADD, ajoute les nouveaux mots au DataFrame
    :param: source_path (chemin du fichier data)
            Accés au dataframe pour le modifier
            La liste des mots comme ils sont sur l'application (delete+modifs)
    :return: None, mets à jour le dataframe et le fichier CSV (data)
    """
    logger.info("Actualisation des mots")
    # 1 - Ajouter les nouveaux mots
    add_new_words(mots, dataframe)
    # 2 - Sauvegarder les nouveaux mots
    data_path = File.JsonFile.get_value_jsondict("WeeVocabulary/main_settings.json", "data", handle_keyERROR=False)
    dataframe.to_csv(data_path, index=False)
    # 3 - Clear file
    source_path = File.JsonFile.get_value_jsondict("WeeVocabulary/main_settings.json", "global", handle_keyERROR=False)
    with open(source_path, "w") as file:
        file.write("")
        logger.info("Get Data: list DELETED")
    # 4 - Update GUI (quit and restart)
    logger.info("Actualisation terminée")
    Settings.relaunch_program()


def create_anki_cards(dataframe: DataFrame):
    logger.info("Création de cartes")
    # 1 - Sélectionner les mots prêts
    count_ok = dataframe["count"] >= 3
    anki_not_done = dataframe["status"] == "waiting"
    words = dataframe[count_ok & anki_not_done]
    # 2 - Séprarer selon le model de carte
    english_list = words.loc[words["language"] == "en", ["front", "back"]].values.tolist()
    print("\nLISTE EEEE: ", english_list, "\n")
    make_ankipackage_from_bituples(english_list, deck_name="vocabulary_en", deck_id=10, output_package="data/output/package_en.apkg", model_with_reverse=True)
    french_list = words.loc[words["language"] == "fr", ["front", "back"]].values.tolist()
    make_ankipackage_from_bituples(french_list, deck_name="vocabulary_fr", deck_id=20, output_package="data/output/package_fr.apkg", model_with_reverse=False)
    # 3 - Update Dataframe and Save
    dataframe.loc[count_ok & anki_not_done, "status"] = "created"
    data_path = File.JsonFile.get_value_jsondict("WeeVocabulary/main_settings.json", "data", handle_keyERROR=False)
    dataframe.to_csv(data_path, index=False)
    # 4 - Quit
    logger.info("Création de cartes terminée")
    Settings.relaunch_program()


# -- PROGRAMME --
if __name__ == '__main__':
    # -- Variables --
    buttons = {
        "ADD": actualiser_nouveaux_mots,
        "CREATE": create_anki_cards
    }
    
    # -- Environnement --
    establish_files()

    # -- Programme --
    # Récupération des données
    new_words, total_dataframe, ready_list = get_data()
    # Fenêtre / Dashboard
    wind = GUI.set_basic_window()
    add_three_board(wind, new_words, total_dataframe, ready_list, buttons)
    wind.mainloop()
