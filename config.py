import os
import re
import setup
import menus
import login
import configparser

path = "config"
config_file = "config/config.cfg"

config = configparser.ConfigParser()


def get_value(section, key):
    return(config[section][key])


def set_value(section, key, value):
    config[section][key] = value


def get_folder(folder):
    if folder == "data":
        return(config["folders"]["data-folder"])
    elif folder == "builds":
        return(config["folders"]["builds-folder"])
    else:
        return(f"{folder} is not a valid argument, use 'data' or 'builds'\n")


def write_config():
    with open(config_file, "w") as configfile:
        config.write(configfile)


def write_default_config():
    config["folders"] = {
        "data-folder": "data",
        "builds-folder": "builds"
    }

    config["ftp"] = {
        "enabled": "false",
        "protocol": "ftps",
        "host": "",
        "username": "",
        "password": ""
    }

    config["dropbox"] = {
        "enabled": "false",
        "token": ""
    }

    config["googledrive"] = {
        "enabled": "false"
    }

    write_config()


def check_config():
    # Check if config.cfg exists, if not create default config

    if not os.path.isdir(path):
        print("Missing config folder")
        os.mkdir(path)
        write_default_config()

    if not os.path.isfile(config_file):
        print("Missing config file\n")
        write_default_config()

    # Check if config.cfg is empty, if true create default config
    if os.stat(config_file).st_size == 0:
        print("Config file is empty, default config has been written\n")
        write_default_config()

    config.read_file(open(config_file))


def check_folders():
    # Check if data-folder and builds-folder are set in the config file
    if get_folder('data') == "" or get_folder('builds') == "":
        setup.folders()

    # Check if data-folder and builds-folder exits
    if not os.path.isdir(get_folder('data')) or not os.path.isdir(get_folder('builds')):
        setup.folders()
    else:
        return


def check_services():
    ftp = get_value("ftp", "enabled")
    dropbox = get_value("dropbox", "enabled")
    googledrive = get_value("googledrive", "enabled")

    if ftp == "false" and dropbox == "false" and googledrive == "false":
        print("No services have been enabled, please choose a service:\n")

        service = menus.service_menu("setup")
        if service == "FTP":
            setup.ftp()
        elif service == "Dropbox":
            setup.dropbox()
        elif service == "Google Drive":
            setup.googledrive()
