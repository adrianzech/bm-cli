import os
import re
import config


def folders():
    functions.clear()
    print("Please follow the setup wizard\n")

    valid_folder_name = re.compile("[-.a-zA-Z0-9]+$")

    while True:
        data_folder = input("Enter data folder name (default: data): ")

        if data_folder == "":
            config.set_value("folders", "data-folder", "data")
            break
        elif (valid_folder_name.match(data_folder)):
            config.set_value("folders", "data-folder", data_folder)
            break

        functions.clear()
        print("Invalid input. Please use [- . A-Z a-z 0-9]\n")

    while True:
        builds_folder = input("Enter builds folder name(default: builds): ")

        if builds_folder == "":
            config.set_value("folders", "builds-folder", "builds")
            break
        elif (valid_folder_name.match(builds_folder)):
            config.set_value("folders", "builds-folder", builds_folder)
            break

        functions.clear()
        print("Invalid input. Please use [- . A-Z a-z 0-9]\n")

    functions.clear()

    # Check if folder already exists, if not create them
    if not os.path.isdir(config.get_folder('data')):
        os.mkdir(config.get_folder('data'))
    if not os.path.isdir(config.get_folder('builds')):
        os.mkdir(config.get_folder('builds'))

    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def ftp():
    print("ftp settings")


def dropbox():
    print("dropbox settings")


def googledrive():
    print("googledrive settings")
