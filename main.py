import os
import sys
import menus
import config
import functions

functions.clear()

config.check_config()
config.check_folders()

menus.start_menu()
