import os
import sys
import menus
import config


def main():
    clear()

    config.check_config()
    config.check_folders()

    menus.start_menu()


def clear():
    os.system("clear")


main()
