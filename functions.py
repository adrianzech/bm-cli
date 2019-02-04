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
            clear()
            try:
                # Create zip file with all contents from config.get_folder('data')
                shutil.make_archive(f"{config.get_folder('builds')}/{filename}", "zip", config.get_folder('data'))
                print(f"Created {filename}\n")
                break
            except:
                print(f"Failed to create {filename}\n")
                break
        elif create_backup in ("n", "N"):
            clear()
            return

        clear()
        print("Invalid input, please try again\n")


def list_builds(service):
    print(f"{service} builds:\n")
    # region [Local]
    if service == "Local":
        build_list = []

        for file in os.listdir(config.get_folder('builds')):
            _filename, _file_extension = os.path.splitext(file)
            if _file_extension == ".zip":
                build_list.append(file)

        menus.create_build_menu(build_list)
        return(build_list)
    # endregion
    # region [FTP]
    elif service == "FTP":
        build_list = []
        file_list = []

        login.ftp_login().retrlines("NLST ", file_list.append)

        for file in file_list:
            _filename, _file_extension = os.path.splitext(file)
            if _file_extension == ".zip":
                build_list.append(file)

        menus.create_build_menu(build_list)
        return(build_list)
    # endregion
    # region [Dropbox]
    elif service == "Dropbox":
        build_list = []

        metadata = login.dropbox_login().files_list_folder(path="")

        for file in metadata.entries:
            _filename, _file_extension = os.path.splitext(file.name)
            if _file_extension == ".zip":
                build_list.append(file.name)

        menus.create_build_menu(build_list)
        return(build_list)
    # endregion
    # region [Google Drive]
    elif service == "Google Drive":
        build_list = []
        build_id_list = []

        drive = login.googledrive_login()
        upload_folder_id = login.get_folder_id()

        file_list = drive.ListFile({'q': f"'{upload_folder_id}' in parents and trashed=false"}).GetList()

        for file in file_list:
            file_title = file["title"]
            file_id = file["id"]
            _filename, _file_extension = os.path.splitext(file_title)
            if _file_extension == ".zip":
                build_list.append(file_title)
                build_id_list.append(file_id)

        menus.create_build_menu(build_list)
        return(build_list, build_id_list)
    # endregion


def download(service):
    print(f"Download build from {service}\n")
    # region [FTP]
    if service == "FTP":
        ftp = login.ftp_login()
        while True:
            build_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        ftp.retrbinary("STOR " + build, open(f"{config.get_folder('builds')}/{build}", "wb").write)
                        print(f"Downloaded {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to download {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Dropbox]
    elif service == "Dropbox":
        db = login.dropbox_login()
        while True:
            build_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        db.files_download_to_file(f"{config.get_folder('builds')}/{build}", "/" + build)
                        print(f"Downloaded {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to download {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Google Drive]
    elif service == "Google Drive":
        drive = login.googledrive_login()
        while True:
            build_list, build_id_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    build_id = build_id_list[int(selection) - 1]
                    clear()
                    try:
                        file = drive.CreateFile({'id': build_id})
                        file.GetContentFile(f"{config.get_folder('builds')}/{build}")
                        print(f"Downloaded {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to download {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion


def upload(service):
    print(f"Upload build to {service}\n")
    # region [FTP]
    if service == "FTP":
        ftp = login.ftp_login()
        while True:
            build_list = list_builds("Local")
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        ftp.storbinary("STOR " + build, open(f"{config.get_folder('builds')}/{build}", "rb"))
                        print(f"Uploaded {build} to {service}\n")
                        break
                    except:
                        print(f"Failed to upload {build} to {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Dropbox]
    elif service == "Dropbox":
        db = login.dropbox_login()
        while True:
            build_list = list_builds("Local")
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        file = open(f"{config.get_folder('builds')}/{build}", "rb")
                        db.files_upload(file.read(), f"/{build}")
                        file.close()
                        print(f"Uploaded {build} to {service}\n")
                        break
                    except:
                        print(f"Failed to upload {build} to {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Google Drive]
    elif service == "Google Drive":
        drive = login.googledrive_login()
        upload_folder_id = login.get_folder_id()
        while True:
            build_list = list_builds("Local")
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        file = drive.CreateFile(metadata={"title": build, "parents": [{"kind": "drive#fileLink", "id": upload_folder_id}]})
                        file.SetContentFile(f"{config.get_folder('builds')}/{build}")
                        file.Upload()
                        print(f"Uploaded {build} to {service}\n")
                        break
                    except:
                        print(f"Failed to upload {build} to {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion


def delete(service):
    print(f"Delete build from {service}\n")
    # region [Local]
    if service == "Local":
        while True:
            build_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        os.remove(f"{config.get_folder('builds')}/{build}")
                        print(f"Deleted {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to delete {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [FTP]
    elif service == "FTP":
        ftp = login.ftp_login()
        while True:
            build_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        ftp.delete(build)
                        print(f"Deleted {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to delete {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Dropbox]
    elif service == "Dropbox":
        db = login.dropbox_login()
        while True:
            build_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    clear()
                    try:
                        db.files_delete("/" + build)
                        print(f"Deleted {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to delete {build} from {service}\n")
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion
    # region [Google Drive]
    elif service == "Google Drive":
        drive = login.googledrive_login()
        while True:
            build_list, build_id_list = list_builds(service)
            print("Press Enter to go back")
            selection = input("Please Select: ")

            if selection.isdigit():
                if 1 <= int(selection) <= (len(build_list)):
                    build = build_list[int(selection) - 1]
                    build_id = build_id_list[int(selection) - 1]
                    clear()
                    try:
                        file = drive.CreateFile({'id': build_id})
                        file.Trash()
                        print(f"Deleted {build} from {service}\n")
                        break
                    except:
                        print(f"Failed to delete {build} from {service}\n")
                        break
            elif selection == "":
                clear()
                return
            clear()
            print("Invalid Input, please try again\n")
    # endregion


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
        shutil.unpack_archive(f"{config.get_folder('builds')}/{build}", config.get_folder('data'), "zip")
        print(f"Restored {build}\n")
    except:
        print(f"Failed to restore {build}\n")


def restore_build():
    print("Choose which build to to restore:\n")
    build_list = list_builds("Local")

    while True:
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
                        break
                    elif selection in ("n", "N"):
                        clear()
                        return
        elif selection == "":
            clear()
            return
        clear()
        print("Invalid Input, please try again\n")
