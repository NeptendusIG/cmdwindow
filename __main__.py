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
logger = Settings.setup_logging("debugging")

root_path = "/Users/gaetan/python_workspace/_ongoing/cmdwindow-project/"
root_path += "cmdwindow"

# -- OPÉRATIONS DÉFINIES --
def start_package(package_name):
    logger.info(f'CMD Window : LAUNCH app "{package_name}"')
    Settings.launch_package(package_name)


# -- VARIABLES INITIALES -- 
operantions = {
    "Passwords": lambda: start_package("pswmanage"),
    "Vocavulaire": lambda: start_package("weevocabulary"),
    "Finances": lambda: start_package("financetrack"),
    "TextEditor": lambda: start_package("txteditor"),
    "AutoBackup": lambda: start_package("autobackup"),
    "YoutubeDown": lambda: start_package("youtubedown"), 
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