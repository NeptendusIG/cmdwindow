#####################################
#          Titre - Date             #
#####################################
# NOTES :
"""
"""
# -- IMPORTS --
# Modules
import sys, subprocess, os
import importlib
# import utility.utility as uti
from utility import GUI, Settings, File
from cmdwindow.class_dir.command_window import CommandWindow
from cmdwindow import __help__

# Settings
logger = Settings.setup_logging("debugging")

root_path = "/Users/gaetan/python_workspace/_ongoing/cmdwindow-project/"
root_path += "cmdwindow"

# -- OPÉRATIONS DÉFINIES --
def start_package(package_name, *args):
    """CURRENTLY NOT USED"""
    Settings.launch_package(package_name, *args)

def launch_from_arg(string_arg, *args):
    if string_arg in associate_longargs.keys():
        package_name = operations[associate_longargs[string_arg]]
        logger.info(f'CMD Window : LAUNCH app "{package_name}"')
        Settings.launch_package(package_name, *args)
    elif string_arg in associate_shortargs.keys():
        package_name = operations[associate_shortargs[string_arg]]
        logger.info(f'CMD Window : LAUNCH app "{package_name}"')
        Settings.launch_package(package_name, *args)
    else:
        logger.error(f'CMD Window : ERROR - Package "{string_arg}" not found')
        # raise ValueError(f'CMD Window : ERROR - Package "{long_arg}" not found')
        show_help()


# -- VARIABLES INITIALES -- 
operations = {
    "Passwords": "pswmanage",
    "Vocabulaire": "weevocabulary",
    "Finances": "financetrack",
    "TextEditor": "txteditor",
    "AutoBackup": "autobackup",
    "YoutubeDown": "youtubedown", 
}

associate_longargs = {
    "--passwords": "Passwords",
    "--vocabulary": "Vocabulaire",
    "--finances": "Finances",
    "--texteditor": "TextEditor",
    "--autobackup": "AutoBackup",
    "--youtubedown": "YoutubeDown",
}
associate_longargs_reversed = {value: key for key, value in associate_longargs.items()}

associate_shortargs = {
    "-p": "Passwords",
    "-v": "Vocabulaire",
    "-f": "Finances",
    "-t": "TextEditor",
    "-a": "AutoBackup",
    "-y": "YoutubeDown",
}
associate_shortargs_reversed = {value: key for key, value in associate_shortargs.items()}

# -- FONCTIONS MAÎTRES --
def open_command_window():
    """Ouvrir la fenêtre de commande"""
    root = GUI.set_basic_window("Command Window", themename="darkly")
    CommandWindow(root, operations)
    logger.info("CMD Window : GUI mode - LAUNCH app")
    root.mainloop()


def go_to_env():
    os.system("cd /Users/gaetan/python_workspace/en_cours/CommandWindow")
    logger.info("Current directory: REFRESHED")

def show_help():
    print(__help__)
    for module_name in operations.keys():
        try:
            module = importlib.import_module(operations[module_name])
            if hasattr(module, '__help__'):
                module_help = getattr(module, '__help__')
                print(f"{module_name}, \t {associate_shortargs_reversed[module_name]}, {associate_longargs_reversed[module_name]}\n\t{module_help}")
            else:
                print(f"{module_name}, \t {associate_shortargs_reversed[module_name]}, {associate_longargs_reversed[module_name]}")
        except ModuleNotFoundError:
            print(f"{module_name}, \t {associate_shortargs_reversed[module_name]}, {associate_longargs_reversed[module_name]}")

def manage_by_args() -> str:
    """Fonction sui interprète les arguments de la ligne de commande
    pour trouver le package qui correspond.
    """
    if len(sys.argv) == 1:
        # Pas d'argument -> Ouvrir la fenêtre de commande (GUI)
        sys.argv.append("DEFAULT_WINDOW_GUI")
    
    logger.info(f'CMD Window : CALL program "{sys.argv[1]}"')
    first_arg = sys.argv[1]
    if first_arg == "help" or first_arg == "--help" or first_arg == "-h":
        show_help()
    elif first_arg == "DEFAULT_WINDOW_GUI":
        logger.info("CMD Window : GUI mode - START")
        open_command_window()
        logger.info("CMD Window : GUI mode - CLOSED")
    elif first_arg.startswith("-"):
        # Si le premier argument est une option -> Lancer le package correspondant
        logger.info(f'CMD Window : Terminal mode "{first_arg}"')
        launch_from_arg(first_arg, *sys.argv[2:]) 

def main():
    manage_by_args()
    

# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -
    #root = GUI.set_basic_window("Command Window")
    # - Programme -
    main()