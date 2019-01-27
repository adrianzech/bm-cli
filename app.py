import os
import sys
import platform
import shutil
import pathlib
import datetime
import getpass
import configparser
from ftplib import FTP
from ftplib import FTP_TLS

config = configparser.ConfigParser()


def clear():
    os.system("clear")


def main():
    check_config()
    config.read_file(open("config.cfg"))
    check_folders()

    # Check if ftp values are empty in config.cfg
    if config["ftp"]["use-ftps"] == "" or config["ftp"]["host"] == "" or config["ftp"]["username"] == "" or config["ftp"]["password"] == "":
        ftp_setup()
    else:
        ftp_login()

    # Set folder variables to config.cfg values
    main.data_folder = config["folders"]["data-folder"]
    main.builds_folder = config["folders"]["builds-folder"]

    while True:
        start_menu()


def write_default_config():
    config["ftp"] = {"use-ftps": "",
                     "host": "",
                     "username": "",
                     "password": ""}

    config["folders"] = {"data-folder": "",
                         "builds-folder": "", }

    with open("config.cfg", "w") as configfile:
        config.write(configfile)


def folders_setup():
    # TODO: Check if name is valid
    clear()
    print("Please follow the setup wizard:\n")
    data_folder = input("Enter data folder name (default: data): ")
    builds_folder = input("Enter builds folder name(default: builds): ")

    # Write default values into config.cfg if users leaves input blank
    # If not blank write users input into config.cfg
    if data_folder == "":
        config["folders"]["data-folder"] = "data"
    else:
        config["folders"]["data-folder"] = data_folder

    if builds_folder == "":
        config["folders"]["builds-folder"] = "builds"
    else:
        config["folders"]["builds-folder"] = builds_folder

    # Check if folder already exists, if not create them
    if not os.path.isdir(config["folders"]["data-folder"]):
        os.mkdir(config["folders"]["data-folder"])
    if not os.path.isdir(config["folders"]["builds-folder"]):
        os.mkdir(config["folders"]["builds-folder"])


def check_folders():
    # Check if data-folder and builds-folder are set in the config file
    if config["folders"]["data-folder"] == "" or config["folders"]["builds-folder"] == "":
        folders_setup()

    # Check if data-folder and builds-folder exits
    if not os.path.isdir(config["folders"]["data-folder"]) or not os.path.isdir(config["folders"]["builds-folder"]):
        folders_setup()
    else:
        return


def check_config():
    # Check if config.cfg exists, if not create default config
    if not os.path.isfile("config.cfg"):
        print("Missing config file, please follow the setup wizard.")
        write_default_config()

    # Check if config.cfg is empty, if true create default config
    if os.stat("config.cfg").st_size == 0:
        print("Config file is empty, please follow the setup wizard.")
        write_default_config()


def ftp_setup():
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

    # Set ftp values in config.cfg to input values
    config["ftp"]["host"] = input("\nEnter ftp host: ")
    config["ftp"]["username"] = input("Enter ftp username: ")
    config["ftp"]["password"] = getpass.getpass("Enter ftp password: ")

    with open("config.cfg", "w") as configfile:
        config.write(configfile)

    clear()
    # FIXME: Don't call main here, call ftp_login() somehow
    main()


def ftp_login():
    # Use ftps
    if config["ftp"]["use-ftps"] == "true":
        try:
            ftp_login.ftp = FTP_TLS(config["ftp"]["host"])
        except:
            print(f"Failed to reach host\n\nPlease enter ftp login information:")
            ftp_setup()

        try:
            ftp_login.ftp.login(config["ftp"]["username"],
                                config["ftp"]["password"])

            ftp_login.ftp.prot_p()
            ftp_login.ftp.cwd("/")
        except:
            print("Failed to login\n\nPlease enter ftp login information:")
            ftp_setup()
    # Use ftp
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
        # Start ftp_setup() because use-ftps is not set to a boolean in config.cfg
        print("Invalid config file\n\nPlease enter ftp login information:")
        ftp_setup()
        return


def start_menu():
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

    print("Build Manager\n")
    for entry in menu:
        print(entry, menu[entry])

    selection = input("\nPlease Select: ")

    clear()

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
        sys.exit()
    else:
        print("Unknown Option Selected\n")


def get_local_builds():
    build_list = []
    build_menu = {}

    # Loop through builds_folder and put all ".zip" files into builds_list
    for f in os.listdir(main.builds_folder):
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    # Loop through builds_list and create and entry in build_menu for every item
    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    # Create menu with every entry in build_menu
    for entry in build_menu:
        print(f"{[entry]}: {build_menu[entry]}")
    print("\n")

    return(build_list)


def get_server_builds():
    build_list = []
    build_menu = {}

    builds = []
    # Put all  files on server into builds
    ftp_login.ftp.retrlines("NLST ", builds.append)

    # Loop through builds and put all ".zip" files into builds_list
    for f in builds:
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    # Loop through builds_list and create and entry in build_menu for every item
    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    # Create menu with every entry in build_menu
    for entry in build_menu:
        print(f"{[entry]}: {build_menu[entry]}")
    print("\n")

    return(build_list)


def list_local_builds():
    print("Local Builds:\n")
    get_local_builds()


def list_server_builds():
    print("Server Builds:\n")
    get_server_builds()


def extract_build(build):
    clear()
    # Check if data_folder has any files or folders in it, if yes delete them
    try:
        if len(os.listdir(main.data_folder)) != 0:
            for f in os.listdir(main.data_folder):
                file_path = os.path.join(main.data_folder, f)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
    except Exception as e:
        print(f"Failed to delete files:\n{e}\n")

    # Extract build into data_folder
    try:
        shutil.unpack_archive(
            f"{main.builds_folder}/{build}", main.data_folder, "zip")

        print(f"Restored [{build}] to [{main.data_folder}]\n")
    except Exception as e:
        print(f"Failed to restore [{build}] to [{main.data_folder}]:\n{e}\n")


def create_build():
    print("Create build:\n")

    build_name = input("\nEnter build name: ")
    build_version = input("Enter build version: ")
    system_input = input(
        f"Enter system version (default: {platform.system()}): ")

    if system_input == "":
        system = platform.system()
    else:
        system = system_input

    timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())
    filename = f"{build_name}_v{build_version}_{timestamp}_{system}.zip"

    create_backup = input(f"\nDo you want to create [{filename}]? (y, n):")

    if create_backup == "y":
        try:
            # Create zip file with all contents from data_folder
            shutil.make_archive(
                f"{main.builds_folder}/{filename}", "zip", main.data_folder)

            clear()
            print(f"Created [{filename}] in [{main.builds_folder}]\n")
        except Exception as e:
            clear()
            print(
                f"Failed to create [{filename}] in [{main.builds_folder}]:\n{e}\n")
    elif create_backup == "n":
        clear()
        return
    else:
        clear()
        print("Invalid input, please try again:\n")
        create_build()


def restore_build():
    print("Choose which build to to restore:\n")

    build_list = get_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    # Parse build name into diffrent variables and store them in a array
    parsed_string = pathlib.Path(
        f"{main.builds_folder}/{build}").stem.split("_")

    try:
        # Check if system version matches with build file
        _system_version = parsed_string[4]
    except Exception as e:
        clear()
        print(f"File doesn't use valid naming scheme:\n{e}\n")
        return

    if selection == "0":
        clear()
        return
    else:
        # Extratct build
        if _system_version == f"v{system_version}":
            extract_build(build)
        else:
            clear()
            print("Wrong system version\n")
            selection = input(
                "Are you sure you want to restore the build? (y, n): ")
            if selection == "y":
                extract_build(build)
            elif selection == "n":
                clear()
                return


def upload_build():
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
                "STOR " + build, open(f"{main.builds_folder}/{build}", "rb"))
            print(f"Uploaded [{build}] to server\n")
        except Exception as e:
            print(f"Failed to upload [{build}] to server:\n{e}\n")


def download_build():
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
                "RETR " + build, open(f"{main.builds_folder}/{build}", "wb").write)
            print(f"Downloaded [{build}] from server\n")
        except Exception as e:
            print(f"Failed to download [{build}] from server:\n{e}\n")


def delete_local_build():
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
            os.remove(f"{main.builds_folder}/{build}")
            print(f"Deleted [{build}] from hard drive\n")
        except Exception as e:
            print(f"Failed to delete [{build}] from hard drive:\n{e}\n")


def delete_server_build():
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
        except Exception as e:
            print(f"Failed to delete [{build}] from server:\n{e}\n")


clear()
main()
