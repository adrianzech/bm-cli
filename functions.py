import os
import re
import shutil
import menus
import config
import login
import platform
import datetime
import pathlib
import dropbox


def clear():
    os.system("clear")


def create_build():
    print("Create build:\n")

    valid_build_name = re.compile("[-.a-zA-Z0-9]+$")
    while True:
        build_name = input("Enter build name: ")
        if (valid_build_name.match(build_name)):
            break

        clear()
        print("Invalid input, please use [- . A-Z a-z 0-9]\n")

    valid_build_version = re.compile("[.0-9]+$")
    while True:
        build_version = input("Enter build version: ")
        if (valid_build_version.match(build_version)):
            break

        clear()
        print("Invalid input, please use [. 0-9]\n")

    while True:
        system = menus.system_menu()
        if not system == None:
            break

        clear()
        print("Unknown option selected, please try again")

    timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())
    filename = f"{build_name}_v{build_version}_{timestamp}_{system}"

    while True:
        create_backup = input(f"Do you want to create {filename}? (y, n):")
        if create_backup in ("y", "Y"):
            try:
                # Create zip file with all contents from config.get_folder('data')
                shutil.make_archive(
                    f"{config.get_folder('builds')}/{filename}", "zip", config.get_folder('data'))

                clear()
                print(f"Created {filename}\n")
                break
            except:
                clear()
                print(f"Failed to create {filename}\n")
                break
        elif create_backup in ("n", "N"):
            clear()
            return

        clear()
        print("Invalid input, please try again\n")
        create_build()


def extract_build(build):
    clear()
    # Check if config.get_folder('data') has any files or folders in it, if yes delete them
    try:
        if len(os.listdir(config.get_folder('data'))) != 0:
            for file in os.listdir(config.get_folder('data')):
                file_path = os.path.join(config.get_folder('data'), file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
    except:
        print(f"Failed to delete files\n")

    # Extract build into config.get_folder('data')
    try:
        shutil.unpack_archive(
            f"{config.get_folder('builds')}/{build}", config.get_folder('data'), "zip")

        print(f"Restored {build}\n")
    except:
        print(f"Failed to restore {build}\n")


def restore_build():
    print("Choose which build to to restore:\n")

    build_list = list_builds("Local")

    print("Leave blank to go back")
    selection = input("\nPlease Select: ")

    if selection.isdigit():
        if 1 <= int(selection) <= (len(build_list)):
            build = build_list[int(selection) - 1]

            # Parse build name into diffrent variables and store them in a array
            parsed_string = pathlib.Path(
                f"{config.get_folder('builds')}/{build}").stem.split("_")

            # Check if system version matches with build file
            try:
                _system_version = parsed_string[4]
            except:
                clear()
                print(f"File doesn't use valid naming scheme\n")
                return

            # Extratct build
            if _system_version == platform.system():
                extract_build(build)
            else:
                clear()
                print("Wrong system version\n")
                selection = input("Are you sure you want to restore the build? (y, n): ")
                if selection in ("y", "Y"):
                    extract_build(build)
                elif selection in ("n", "N"):
                    clear()
                    return
        else:
            clear()
            print("Invalid input, please try again\n")
            restore_build()
    elif selection == "":
        clear()
        return
    else:
        clear()
        print("Invalid input, please try again\n")
        restore_build()


def list_builds(service):
    if service == "Local":
        build_list = []
        build_menu = {}

        print("Local builds:\n")

        # Loop through config.get_folder('builds') and put all ".zip" files into builds_list
        for f in os.listdir(config.get_folder('builds')):
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

    elif service == "FTP":
        build_list = []
        build_menu = {}

        print("FTP builds:\n")

        builds = []
        # Put all  files on server into builds
        login.ftp_login().retrlines("NLST ", builds.append)

        # Loop through builds and put all ".zip" files into builds_list
        for file in builds:
            _filename, _file_extension = os.path.splitext(file)
            if _file_extension == ".zip":
                build_list.append(file)

        # Loop through builds_list and create and entry in build_menu for every item
        for index, build in enumerate(build_list):
            build_menu[index + 1] = build

        # Create menu with every entry in build_menu
        for entry in build_menu:
            print(f"{[entry]}: {build_menu[entry]}")
        print("\n")

        return(build_list)

    elif service == "Dropbox":
        # TODO: Store dropbox login in variable
        build_list = []
        build_menu = {}

        print("Dropbox builds:\n")

        metadata = login.dropbox_login().files_list_folder(path="")

        for file in metadata.entries:
            _filename, _file_extension = os.path.splitext(file.name)
            if _file_extension == ".zip":
                build_list.append(file.name)

        # Loop through builds_list and create and entry in build_menu for every item
        for index, build in enumerate(build_list):
            build_menu[index + 1] = build

        # Create menu with every entry in build_menu
        for entry in build_menu:
            print(f"{[entry]}: {build_menu[entry]}")
        print("\n")

        return(build_list)

    elif service == "Google Drive":
        build_list = []
        build_menu = {}

        print("Google Drive builds:\n")

        drive = login.googledrive_login()

        upload_folder = "Kodi Build Manager"
        upload_folder_id = None

        # Check if folder exists. If not than create one with the given name
        file_list = drive.ListFile({"q": "'root' in parents and trashed=false"}).GetList()
        for file_folder in file_list:
            if file_folder["title"] == upload_folder:
                upload_folder_id = file_folder["id"]
                break
            else:
                # If there is no mathing folder, create a new one
                file_new_folder = drive.CreateFile({"title": upload_folder,
                                                    "mimeType": "application/vnd.google-apps.folder"})
                file_new_folder.Upload()
                break

        # Auto-iterate through all files in the root folder.
        file_list = drive.ListFile({'q': f"'{upload_folder_id}' in parents and trashed=false"}).GetList()
        for file in file_list:
            _file = file["title"]
            _filename, _file_extension = os.path.splitext(_file)
            if _file_extension == ".zip":
                build_list.append(_file)

        # Loop through builds_list and create and entry in build_menu for every item
        for index, build in enumerate(build_list):
            build_menu[index + 1] = build

        # Create menu with every entry in build_menu
        for entry in build_menu:
            print(f"{[entry]}: {build_menu[entry]}")
        print("\n")

        return(build_list)


def download(service):
    if service == "Local":
        print(f"Download build from {service}\n")
    elif service == "FTP":
        print(f"Download build from {service}\n")
    elif service == "Dropbox":
        print(f"Download build from {service}\n")
    elif service == "Google Drive":
        print(f"Download build from {service}\n")
    else:
        print(f"Something horrible happened")


def upload(service):
    if service == "Local":
        print(f"Upload build to {service}\n")
    elif service == "FTP":
        print(f"Upload build to {service}\n")
    elif service == "Dropbox":
        print(f"Upload build to {service}\n")
    elif service == "Google Drive":
        print(f"Upload build to {service}\n")
    else:
        print(f"Something horrible happened")


def delete(service):
    if service == "Local":
        print(f"Delete build from {service}\n")
    elif service == "FTP":
        print(f"Delete build from {service}\n")
    elif service == "Dropbox":
        print(f"Delete build from {service}\n")
    elif service == "Google Drive":
        print(f"Delete build from {service}\n")
    else:
        print(f"Something horrible happened")
