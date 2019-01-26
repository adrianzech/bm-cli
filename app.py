import os
import sys
import shutil
import pathlib
import zipfile
import datetime
import getpass
import configparser
from ftplib import FTP
from ftplib import FTP_TLS

config = configparser.ConfigParser()

# region settings
use_ftps = True

data_folder = "data"
builds_folder = "builds"

local_kodi_version = "17.3"
# endregion

# region menu
menu = {}
menu["[1]:"] = "List local builds"
menu["[2]:"] = "List server builds"
menu["[3]:"] = "Backup"
menu["[4]:"] = "Restore"
menu["[5]:"] = "Upload"
menu["[6]:"] = "Download"
menu["[7]:"] = "Delete local file"
menu["[8]:"] = "Delete server file"
menu["[9]:"] = "Change ftp settings"
menu["[0]:"] = "Exit"
# endregion


def clear():
    os.system("clear")


clear()


def main():
    check_config()

    config.read_file(open("config.cfg"))

    if config["ftp"]["host"] == "" or config["ftp"]["username"] == "" or config["ftp"]["password"] == "":
        setup()
    else:
        ftp_login()

    while True:
        start_menu()


def write_default_config():
    config["ftp"] = {"host": "",
                     "username": "",
                     "password": ""}

    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def check_config():
    if not os.path.isfile("config.cfg"):
        print("\nMissing config file, please follow the setup wizard.")
        write_default_config()

    if os.stat("config.cfg").st_size == 0:
        print("\nConfig file is empty, please follow the setup wizard.")
        write_default_config()


def setup():
    config["ftp"]["host"] = input("\nEnter ftp host: ")
    config["ftp"]["username"] = input("Enter ftp username: ")
    config["ftp"]["password"] = getpass.getpass("Enter ftp password: ")

    with open("config.cfg", "w") as configfile:
        config.write(configfile)

    main()


def ftp_login():
    if use_ftps == True:
        try:
            ftp_login.ftp = FTP_TLS(config["ftp"]["host"])
        except:
            print("\nFailed to reach host, please update your ftp settings.\n")
            setup()

        try:
            ftp_login.ftp.login(config["ftp"]["username"],
                                config["ftp"]["password"])

            ftp_login.ftp.prot_p()
            ftp_login.ftp.cwd("/")
        except:
            print("\nFailed to login, please update your ftp settings.\n")
            setup()
    else:
        try:
            ftp_login.ftp = FTP(config["ftp"]["host"])
        except:
            print("\nFailed to reach host, please update your ftp settings.\n")
            setup()

        try:
            ftp_login.ftp.login(config["ftp"]["username"],
                                config["ftp"]["password"])

            ftp_login.ftp.cwd("/")
        except:
            print("\nFailed to login, please update your ftp settings.\n")
            setup()


def start_menu():
    print("Build Manager\n")
    for entry in menu:
        print(entry, menu[entry])

    selection = input("\nPlease Select: ")

    if selection == "1":
        list_local_builds()
    elif selection == "2":
        list_server_builds()
    elif selection == "3":
        backup()
    elif selection == "4":
        restore()
    elif selection == "5":
        upload()
    elif selection == "6":
        download()
    elif selection == "7":
        delete_local_file()
    elif selection == "8":
        delete_server_file()
    elif selection == "9":
        setup()
    elif selection == "0":
        sys.exit()
    else:
        print("\nUnknown Option Selected!\n")


def get_local_builds():
    build_list = []
    build_menu = {}

    for f in os.listdir(builds_folder):
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    for entry in build_menu:
        print(f"{[entry]}: {build_menu[entry]}")
    print("\n")

    return(build_list)


def get_server_builds():
    build_list = []
    build_menu = {}

    builds = []
    ftp_login.ftp.retrlines("NLST ", builds.append)

    for f in builds:
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    for entry in build_menu:
        print(f"{[entry]}: {build_menu[entry]}")
    print("\n")

    return(build_list)


def list_local_builds():
    clear()
    print("Local Builds:\n")
    get_local_builds()


def list_server_builds():
    clear()
    print("Server Builds:\n")
    get_server_builds()


def extract(build):
    clear()
    try:
        if len(os.listdir(data_folder)) != 0:
            for dir in os.listdir(data_folder):
                shutil.rmtree(f"{data_folder}/{dir}")
    except:
        print("Failed to delete files\n")

    try:
        zipf = zipfile.ZipFile(build, "r")
        zipf.extractall(data_folder)
        print(f"Restored [{build}] to [{data_folder}]\n")
    except:
        print(f"Failed to restore [{build}] to [{data_folder}]\n")


def backup():
    clear()
    print("Create Backup:\n")

    build_name = input("\nEnter build name: ")
    build_version = input("Enter build version: ")
    kodi_version = input("Enter kodi version: ")

    timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())

    filename = f"{build_name}_v{build_version}_{timestamp}_v{kodi_version}.zip"

    create_backup = input(f"\nDo you want to create [{filename}]? (y, n):")

    folders = []
    for f in os.listdir(data_folder):
        folders.append(f"{data_folder}/{f}")

    print(folders)

    if create_backup == "y":
        def zipdir(path, ziph):
            for _root, _dirs, _files in os.walk(path):
                for file in _files:
                    ziph.write(os.path.join(_root, file),
                               os.path.relpath(os.path.join(_root, file),
                                               os.path.join(path, "..")))

        def zipit(dir_list, zip_name):
            zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
            for dir in dir_list:
                zipdir(dir, zipf)

        try:
            zipit(folders, filename)
            clear()
            print(f"Created [{filename}] in [{data_folder}]\n")
        except:
            clear()
            print(f"Failed to create [{filename}] in [{data_folder}]\n")
    elif create_backup == "n":
        clear()
        return


def restore():
    clear()
    print("Choose which build to to restore:\n")

    build_list = get_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    parsed_string = pathlib.Path(f"{builds_folder}/{build}").stem.split("_")

    try:
        _kodi_version = parsed_string[4]
    except:
        clear()
        print("File doesn't use valid naming scheme\n")
        return

    if selection == "0":
        clear()
        return
    else:
        if _kodi_version == f"v{local_kodi_version}":
            extract(f"{builds_folder}/{build}")
        else:
            clear()
            print("Wrong Kodi version\n")
            selection = input(
                "Are you sure you want to restore the build? (y, n): ")
            if selection == "y":
                extract(f"{builds_folder}/{build}")
            elif selection == "n":
                clear()
                return


def upload():
    clear()
    print("Choose which build to to upload:\n")

    build_list = get_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    clear()

    if selection == "0":
        return
    else:
        try:
            ftp_login.ftp.storbinary(
                "STOR " + build, open(f"{builds_folder}/{build}", "rb"))
            print(f"Uploaded [{build}] to server\n")
        except:
            print(f"Failed to upload [{build}] to server\n")


def download():
    clear()
    print("Choose which build to to download:\n")

    build_list = get_server_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    clear()

    if selection == "0":
        return
    else:
        try:
            ftp_login.ftp.retrbinary(
                "RETR " + build, open(f"{builds_folder}/{build}", "wb").write)
            print(f"Downloaded [{build}] from server\n")
        except:
            print(f"Failed to download [{build}] from server\n")


def delete_local_file():
    clear()
    print("Choose which build to delete from hard drive:\n")

    build_list = get_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    clear()

    if selection == "0":
        return
    else:
        try:
            os.remove(f"{builds_folder}/{build}")
            print(f"Deleted [{build}] from hard drive\n")
        except:
            print(f"Failed to delete [{build}] from hard drive\n")


def delete_server_file():
    clear()
    print("Choose which build to delete from server:\n")

    build_list = get_server_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    clear()

    if selection == "0":
        return
    else:
        try:
            ftp_login.ftp.delete(build)
            print(f"Deleted [{build}] from server\n")
        except:
            print(f"Failed to delete [{build}] from server\n")


main()
