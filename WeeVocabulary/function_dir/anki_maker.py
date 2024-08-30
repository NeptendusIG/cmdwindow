#####################################
#     Utilisation Template Anki     #
#####################################
# NOTES :
"""
-- Gestion TEMPLATE --
-- Creation de CARTE --
-- Creation de DECK --
Le nom détermine l'appartenance, plus que son id
-- Creation de PACKAGE --
"""
import sys

# -- IMPORTS --
# Modules
from utility import *
import function_dir.ankicard_template as tmp
import genanki

# Classes
# -- FONCTIONS DÉFINIES --
def card_to_test(info, model, deck_id=20000):
    note = genanki.Note(
        model=model,
        fields=list(info.values())
    )
    deck = genanki.Deck(deck_id, "DeckTEST")
    deck.add_note(note)

    pack = genanki.Package(deck)
    pack.media_files = []  # enter full paths
    pack.write_to_file('output_deck.apkg')
    File.open_file('output_deck.apkg')


def create_note_2fields_anytype(model, note_front, note_back):
    """Return note du modèle donné avec les 2 champs donnés.
    pre: model est un modèle basic/ pour texte (la fct ajoute l'html),
         note_front est un texte ou un chemin d'image/son
    post: note de class genanki.Note"""
    note_front = add_appropriate_html(note_front)
    note_back = add_appropriate_html(note_back)
    note = genanki.Note(
        model=model,
        fields=[note_front, note_back]
    )
    return note


def add_appropriate_html(string_data):
    """Ajoute les balises html appropriées."""
    if not os.path.isfile(string_data):
        return string_data
    if os.path.splitext(string_data)[1] in [".jpg", ".png", ".jpeg", ".heic"]:
        image_fulname = (os.path.split(string_data)[1])
        return '<img src="{}">'.format(image_fulname)
    if os.path.splitext(string_data)[1] in [".mp3"]:
        sound_fulname = (os.path.split(string_data)[1])
        return '[sound:{0}]'.format(sound_fulname)


def find_media_files(note_data):
    """Trouve les fichiers médias dans les données de la note."""
    medias = []
    for field_data in note_data:
        if os.path.isfile(field_data):
            medias.append(os.path.abspath(field_data))
    return medias


def add_card_and_media_from_bituples(list_data_for_notes, model_2fields, card_deck, media_list=[], return_result=False):
    """Ajoute notes et media (abs path) à deck à partir d'une liste de bi-tuples."""
    for note_data in list_data_for_notes:
        # retrieve stored data
        media_list.extend(find_media_files(note_data))
        note = create_note_2fields_anytype(model_2fields, note_data[0], note_data[1])
        logger.debug(f"NOTE: {note_data[0]}, {note_data[1]}\n{note}")
        # add note and delete from waitlist
        card_deck.add_note(note)
    else:
        logger.debug(f"Anki: process: deck MADE")
    if return_result:
        return card_deck, media_list


def save_anki_package(deck, media_list, output_package):
    """Construit et créé un package Anki à partir d'un deck et une liste de médias."""
    package = genanki.Package(deck)
    package.media_files = media_list
    package.write_to_file(output_package)
    logger.debug(f"Anki: process: package CREATED")
    return package

# -- VARIABLES INITIALES --


# -- FONCTIONS MAÎTRES --
def make_ankipackage_from_bituples(list_data_for_notes, deck_name="DeckTEST", deck_id=10000, output_package="output_deck.apkg", model_with_reverse=False, **kwargs):
    """Créer un storing_deck de notes à partir d'un fichier jsonline."""
    if not list_data_for_notes:
        logger.error(f"AnkiProcess: CANCELED (No data)")
        return
    logger.info(f"AnkiProcess: START")
    # Add cards and media
    deck = genanki.Deck(deck_id, deck_name)
    media = []
    model = tmp.basic_and_reversed if model_with_reverse else tmp.basic_qa
    add_card_and_media_from_bituples(list_data_for_notes, model_2fields=model, card_deck=deck, media_list=media)
    # New Package
    save_anki_package(deck, media, output_package)
    # Open the created package.apkg
    File.open_file(output_package)
    logger.info(f"OP:AnkiProcess: package FINISHED (cards:{len(deck.notes)})")


# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -

    # - Programme -
    #card_to_test({1: "output15.mp3, [sound:output15.mp3]", 2: "IMG_8419.jpg"}, tmp.sound_to_word)
    pass
