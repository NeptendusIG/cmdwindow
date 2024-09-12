#####################################
#          Titre - Date             #
#####################################
# NOTES :
"""
"""
# -- IMPORTS --
# Modules
import sys, subprocess, os
# import utility.utility as uti
from utility import GUI, Settings, File
from cmdwindow.class_dir.command_window import CommandWindow


# Settings
import cmdwindow.log_config as log_config
logger = Settings.setlog_module(log_config, "debugging")

root_path = "/Users/gaetan/python_workspace/_ongoing/cmdwindow-project/"
root_path += "cmdwindow"

# -- OPÉRATIONS DÉFINIES --
def start_passwords():
    python = sys.executable
    #script_path = "/Users/gaetan/python_workspace/en_cour/PasswordManager/main.py"
    script_path = root_path + "/PasswordManager/main.py"
    os.system("python -m pswmanage")
    # subprocess.Popen([python, script_path])


def start_vocavulaire():
    python = sys.executable
    script_path = root_path + "WeeVocabulary/main.py"
    #sys.path.append("/Users/gaetan/python_workspace/programmes/PasswordManager")
    #sys.path.append("/Users/gaetan/python_workspace/programmes/PasswordManager/utilitaire")
    subprocess.Popen([python, script_path])


def start_finances():
    python = sys.executable
    script_path = root_path + "FinancesTracker/__main__.py"
    subprocess.Popen([python, script_path])


def start_editor():
    python = sys.executable
    script_path = root_path + "TextEditor/main.py"
    subprocess.Popen([python, script_path])

# -- VARIABLES INITIALES -- 
operantions = {
    "Passwords": start_passwords,
    "Vocavulaire": start_vocavulaire,
    "Finances": start_finances,
    "TextEditor": start_editor,
    "AutoBackup": None,
    "YoutubeDown": None, 
}

# -- FONCTIONS MAÎTRES --
def open_command_window():
    """Ouvrir la fenêtre de commande"""
    root = GUI.set_basic_window("Command Window", themename="darkly")
    CommandWindow(root, operantions)
    root.mainloop()


def go_to_cmd():
    os.system("cd /Users/gaetan/python_workspace/en_cours/CommandWindow")
    logger.info("Current directory: REFRESHED")


def main():
    go_to_cmd()
    open_command_window()
    

# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -
    #root = GUI.set_basic_window("Command Window")
    # - Programme -
    main()