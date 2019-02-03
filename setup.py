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
        print("Please follow the setup wizard:\n")

        protocol = input("Do you want use ftps instead of ftp? (y, n): ")
        if protocol in ("y", "Y"):
            config.set_value("ftp", "protocol", "ftps")
        elif protocol in ("n", "N"):
            config.set_value("ftp", "protocol", "ftp")
        else:
            functions.clear()
            print("Wrong input, please try again:\n")

        config.set_value("ftp", "host", input("Enter ftp host: "))
        config.set_value("ftp", "username", input("Enter ftp username: "))
        config.set_value("ftp", "password", getpass.getpass("Enter ftp password: "))

        valid_path = re.compile("[-./a-zA-Z0-9]+$")
        while True:
            path = input("Enter ftp path (default: root): ")

            if path == "":
                config.set_value("ftp", "path", "/")
                break
            elif (valid_path.match(path)):
                config.set_value("frp", "path", path)
                break

            functions.clear()
            print("Invalid input. Please use [/ - . A-Z a-z 0-9]\n")

        message = login.ftp_login()

        functions.clear()
        if message == "host_error":
            print("Failed to reach host\n")
        elif message == "login_error":
            print("Failed to login\n")
        elif message == "folder_error":
            print("Path does not exist\n")
        else:
            config.set_value("ftp", "enabled", "true")
            config.write_config()

            print("Successfully logged in\n")
            break


def dropbox():
    while True:
        config.set_value("dropbox", "token", input("Enter Dropbox access token: "))
        config.write_config()
        functions.clear()
        try:
            login.dropbox_login()
            config.set_value("ftp", "enabled", "true")
            config.write_config()
            print("Successfully logged in\n")
            break
        except:
            print("Failed to log in\n")


def googledrive():
    print("googledrive settings")
