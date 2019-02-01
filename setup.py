import os
import re
import login
import config
import getpass
import functions


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

    config.write_config()


def ftp():
    while True:
        config.set_value("ftp", "enabled", "false")
        config.write_config()

        print("Please follow the setup wizard:\n")

        use_ftps = input("Do you want use ftps instead of ftp? (y, n): ")
        if use_ftps in ("y", "Y"):
            config.set_value("ftp", "use_ftps", "true")
        elif use_ftps in ("n", "N"):
            config.set_value("ftp", "use_ftps", "false")
        else:
            functions.clear()
            print("Wrong input, please try again:\n")

        config.set_value("ftp", "host", input("Enter ftp host: "))
        config.set_value("ftp", "username", input("Enter ftp username: "))
        config.set_value("ftp", "password", getpass.getpass("Enter ftp password: "))

        message = login.ftp_login()
        print(message)

        if message == "host_error":
            functions.clear()
            print("Failed to reach host\n")
        elif message == "login_error":
            functions.clear()
            print("Failed to login\n")
        else:
            config.set_value("ftp", "enabled", "true")

            config.write_config()
            functions.clear()
            print("Successfully logged in\n")
            break


def dropbox():
    print("dropbox settings")


def googledrive():
    print("googledrive settings")
