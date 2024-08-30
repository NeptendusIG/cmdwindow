# BASICS :
import os, shutil, time, logging, json
# LANG DETECTING
# from langdetect import detect
from lingua import Language, LanguageDetectorBuilder
languages = [Language.ENGLISH, Language.FRENCH]               #, Language.GERMAN, Language.SPANISH, Language.DUTCH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()
# TRANSLATION
from translate import Translator
# VOICE GENERATION
from gtts import gTTS
# PERSONAL MODULES
import function_dir.anki_maker as anki_maker
from utility import File, OutNetwork


logger = logging.getLogger("debugging")
count_audio = 0

# -- Step 0 : Set Up --
main_settings_json = "main_settings.json"
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


def establish_files():
    """Vérifier existance des fichiers et dossiers nécessaires. Si non, les créer.
    FICHIERS """
    File.create_file_tree(main_settings_json, settings_dict)  # create settings jsonfile
    source_path = File.JsonFile.get_value_jsondict(main_settings_json, "global")
    File.create_file_tree(source_path, can_make_dirs=False)
    File.create_file_tree("data/output/main_list.csv")
    File.create_file_tree("data/backup/en_backup.txt")
    File.create_file_tree("data/backup/fr_backup.txt")
    os.makedirs("data/output/fr_audio", exist_ok=True)


# -- Step 1 : New words --
def there_is_new_words(filetxt_path="data/input/new_words.txt"):
    """Vérifier s'il y a des nouveaux mots dans le fichier new_words.txt"""
    return open(filetxt_path, "r").read() != ""


def add_new_words(filetxt_path):
    with open(filetxt_path, "r", encoding="utf-8") as file:
        new_words = file.readlines()

    for word in new_words:
        word = word.strip()
        if word == "":
            continue

        lang = detector.detect_language_of(word)
        logger.debug(f"Lang Detect: {lang} for {word}")

        if lang == Language.FRENCH :
            path = create_fr_audio(word, "data/output/fr_audio")
            logger.debug(f"File: AddLine: ({[path, word]})\n")
            File.JsonLine.add_a_jsonline([path, word], "data/output/fr_waitlist.json")
            saved_word_to_backup(word, field="french")

        elif lang == Language.ENGLISH:
            translation_fr = translate_to_french(word)
            if word.lower() in translation_fr.lower():  # Le mot en français a été confondu
                path = create_fr_audio(word, "data/output/fr_audio")
                logger.debug(f"File: AddLine: ({[path, word]})\n")
                File.JsonLine.add_a_jsonline((path, word), "data/output/fr_waitlist.json")
            else:
                logger.debug(f"File: AddLine: ({(word, translation_fr)})\n")
                File.JsonLine.add_a_jsonline((word, translation_fr), "data/output/en_waitlist.json")
                saved_word_to_backup(word, field="english")

        else:
            logger.error(f"Lang Detect: NotManage {lang} ({word})")


def saved_word_to_backup(word, field=None, backup_path=None):
    """Sauvegarder les nouveaux mots dans un fichier texte"""
    if not (field or backup_path):
        logger.error(f"File: Backup: NoFile Given (for {word})")
        return
    if backup_path is None and field is not None:
        settings_of_chosen_field = File.JsonFile.get_value_jsondict(main_settings_json, field, handle_keyERROR=True)
        backup_path = settings_of_chosen_field["text_backup_list"]
        if not backup_path:
            logger.error(f"File: Backup: NoPath Assigned (to {field})")
            return
    File.add_line(backup_path, word)


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


# -- Step 2 : Ajouter les données en attentes --
def create_cards_from_waitlist(choce_of_field, clear_source=True):
    logger.info(f"OP:AnkiProcess: START ({choce_of_field})")
    # 1 Get path of the wait list with the given name
    settings_of_chosen_field = File.JsonFile.get_value_jsondict(main_settings_json, choce_of_field)  # Dict of wait lists
    file_path = settings_of_chosen_field["json_waiting_list"]  # path of the wait list
    logger.debug(f"AnkiProcess: source: file path ({file_path})")
    # 2 Retrieve list of the cards (each line is a tuple of its fields)
    datalist_from_waiting_words = File.JsonLine.made_list_of_jsonline(file_path)
    logger.debug(f"AnkiProcess: source: data lines\n\t{datalist_from_waiting_words}")
    # 3 Make package and Open it
    logger.debug(f"AnkiProcess: settings load")
    anki_maker.make_ankipackage_from_bituples(datalist_from_waiting_words, **settings_of_chosen_field)
    # 4 <Make backup> and Clear the wait list
    if clear_source:
        open(file_path, 'w').close()
        logger.debug(f"AnkiProcess: source: CLEARED")



# -- SANDBOX --
if __name__ == '__main__':
    # - Variables -
    file_to_backup = "/Users/gaetan/Docs/Objectifs/4_Apprendre/pythonProject/ProjetsEnCours/AutoBackUp/data/input/test.txt"
    backup_directory = "/Users/gaetan/Docs/Objectifs/4_Apprendre/pythonProject/ProjetsEnCours/AutoBackUp/data/output"
    backup_interval_minutes = 0.05  # Une fois par jour
    # - Programme -
