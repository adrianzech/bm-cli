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
local_system_version = "17.3"

# region menu
menu = {}
menu["[1]:"] = "List local builds"
menu["[2]:"] = "List server builds"
menu["[3]:"] = "Create build"
menu["[4]:"] = "Restore build"
menu["[5]:"] = "Upload build"
menu["[6]:"] = "Download build"
menu["[7]:"] = "Delete local build"
menu["[8]:"] = "Delete server build"
menu["[9]:"] = "Change ftp settings"
menu["[0]:"] = "Exit"
# endregion


def clear():
    os.system("clear")


def main():
    check_config()

    config.read_file(open("config.cfg"))

    if config["folders"]["data-folder"] == "" or config["folders"]["data-folder"] == "":
        folders_setup()

    check_folders()

    if config["ftp"]["use-ftps"] == "" or config["ftp"]["host"] == "" or config["ftp"]["username"] == "" or config["ftp"]["password"] == "":
        ftp_setup()
    else:
        ftp_login()

    while True:
        start_menu()


def write_default_config():
    config["ftp"] = {"use-ftps": "",
                     "host": "",
                     "username": "",
                     "password": ""}

    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def check_folders():
    if not os.path.isdir(config["folders"]["data-folder"]):
        os.mkdir(config["folders"]["data-folder"])
    elif not os.path.isdir(config["folders"]["data-folder"]):
        os.mkdir(config["folders"]["data-folder"])
    else:
        return


def check_config():
    if not os.path.isfile("config.cfg"):
        print("Missing config file, please follow the setup wizard.")
        write_default_config()

    if os.stat("config.cfg").st_size == 0:
        print("Config file is empty, please follow the setup wizard.")
        write_default_config()


def folders_setup():
    # TODO: Press enter for default value
    # TODO: Check if name is valid
    clear()
    print("Please follow the setup wizard:\n")
    config["folders"]["data-folder"] = input("Enter data folder name: ")
    config["folders"]["data-folder"] = input("Enter builds folder name: ")
    return
    # TODO: Message


def ftp_setup():
    clear()
    print("Please follow the setup wizard:\n")
    use_ftps = input("Do you want use ftps instead of ftp? (y, n):  ")
    if use_ftps == "y":
        config["ftp"]["use-ftps"] = "true"
    elif use_ftps == "n":
        config["ftp"]["use-ftps"] = "false"
    else:
        clear()
        print("Wrong input, please try again:\n")
        ftp_setup()

    config["ftp"]["host"] = input("\nEnter ftp host: ")
    config["ftp"]["username"] = input("Enter ftp username: ")
    config["ftp"]["password"] = getpass.getpass("Enter ftp password: ")

    with open("config.cfg", "w") as configfile:
        config.write(configfile)

    clear()
    main()


def ftp_login():
    if config["ftp"]["use-ftps"] == "true":
        try:
            ftp_login.ftp = FTP_TLS(config["ftp"]["host"])
        except:
            print("Failed to reach host\n\nPlease enter ftp login information:")
            ftp_setup()

        try:
            ftp_login.ftp.login(config["ftp"]["username"],
                                config["ftp"]["password"])

            ftp_login.ftp.prot_p()
            ftp_login.ftp.cwd("/")
        except:
            print("Failed to login\n\nPlease enter ftp login information:")
            ftp_setup()
    elif config["ftp"]["use-ftps"] == "false":
        try:
            ftp_login.ftp = FTP(config["ftp"]["host"])
        except:
            print("Failed to reach host\n\nPlease enter ftp login information:")
            ftp_setup()

        try:
            ftp_login.ftp.login(config["ftp"]["username"],
                                config["ftp"]["password"])

            ftp_login.ftp.cwd("/")
        except:
            print("Failed to login\n\nPlease enter ftp login information:")
            ftp_setup()
    else:
        # TODO: do something
        return


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
        create_build()
    elif selection == "4":
        restore_build()
    elif selection == "5":
        upload_build()
    elif selection == "6":
        download_build()
    elif selection == "7":
        delete_local_build()
    elif selection == "8":
        delete_server_build()
    elif selection == "9":
        ftp_setup()
    elif selection == "0":
        clear()
        sys.exit()
    else:
        clear()
        print("Unknown Option Selected!\n")


def get_local_builds():
    build_list = []
    build_menu = {}

    for f in os.listdir(config["folders"]["data-folder"]):
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
        if len(os.listdir(config["folders"]["data-folder"])) != 0:
            for dir in os.listdir(config["folders"]["data-folder"]):
                # shutil.rmtree(f"{config["folders"]["data-folder"]}/{dir}")
                # shutil.rmtree("{}/{}".format(config["folders"]["data-folder"], dir)
                shutil.rmtree("%s/%s" % config["folders"]["data-folder"], dir)
    except:
        print("Failed to delete files\n")

    try:
        zipf = zipfile.ZipFile(build, "r")
        zipf.extractall(config["folders"]["data-folder"])
        print(f"Restored [{build}] to [{config["folders"]["data-folder"]}]\n")
    except:
        print(f"Failed to restore [{build}] to [{config["folders"]["data-folder"]}]\n")


def create_build():
    clear()
    print("Create build:\n")

    build_name = input("\nEnter build name: ")
    build_version = input("Enter build version: ")
    system_version = input("Enter system version: ")

    timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())

    filename = f"{build_name}_v{build_version}_{timestamp}_v{system_version}.zip"

    create_backup = input(f"\nDo you want to create [{filename}]? (y, n):")

    folders = []
    for f in os.listdir(config["folders"]["data-folder"]):
        folders.append(config["folders"]["data-folder"])

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
            print(f"Created [{filename}] in [{config["folders"]["data-folder"]}]\n")
        except:
            clear()
            print(f"Failed to create [{filename}] in [{config["folders"]["data-folder"]}]\n")
    elif create_backup == "n":
        clear()
        return


def restore_build():
    clear()
    print("Choose which build to to restore:\n")

    build_list = get_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    parsed_string = pathlib.Path(f"{config["folders"]["data-folder"]}/{build}").stem.split("_")

    try:
        _system_version = parsed_string[4]
    except:
        clear()
        print("File doesn't use valid naming scheme\n")
        return

    if selection == "0":
        clear()
        return
    else:
        if _system_version == f"v{local_system_version}":
            extract(f"{config["folders"]["data-folder"]}/{build}")
        else:
            clear()
            print("Wrong system version\n")
            selection = input(
                "Are you sure you want to restore the build? (y, n): ")
            if selection == "y":
                extract(f"{config["folders"]["data-folder"]}/{build}")
            elif selection == "n":
                clear()
                return


def upload_build():
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
                "STOR " + build, open(f"{config["folders"]["data-folder"]}/{build}", "rb"))
            print(f"Uploaded [{build}] to server\n")
        except:
            print(f"Failed to upload [{build}] to server\n")


def download_build():
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
                "RETR " + build, open(f"{config["folders"]["data-folder"]}/{build}", "wb").write)
            print(f"Downloaded [{build}] from server\n")
        except:
            print(f"Failed to download [{build}] from server\n")


def delete_local_build():
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
            os.remove(f"{config["folders"]["data-folder"]}/{build}")
            print(f"Deleted [{build}] from hard drive\n")
        except:
            print(f"Failed to delete [{build}] from hard drive\n")


def delete_server_build():
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


clear()
main()
