import os
import sys
import menus
import config
import functions

functions.clear()

config.check_config()
config.check_folders()
config.check_services()

while True:
    menus.start_menu()
