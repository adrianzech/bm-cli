import os
import sys
import shutil
import pathlib
import zipfile
import datetime
from ftplib import FTP

host = "159.69.90.146"
username = "kbm"
password = "underwolf99912"

# region ftp login
ftp = FTP(host)

try:
    ftp.login(username, password)
except:
    print("Failed to login.\n")

ftp.cwd("/")
# endregion

# region settings
data_folder = "data"
folders = [
    "data/addons",
    "data/userdata"]

build_name = "AdrianBuild"
build_version = "1.42"
timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())
kodi_version = "17.62"
# endregion

# region menu
menu = {}

menu["0"] = "Exit"
menu["1"] = "List local builds"
menu["2"] = "List server builds"
menu["3"] = "Backup"
menu["4"] = "Restore"
menu["5"] = "Upload"
menu["6"] = "Download"
menu["7"] = "Delete local file"
menu["8"] = "Delete server file"
# endregion


def start_menu():
    for entry in menu:
        print(entry, menu[entry])

    selection = input("\nPlease Select: ")

    if selection == "0":
        ftp.quit()
        sys.exit()
    elif selection == "1":
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
    else:
        print("\nUnknown Option Selected!\n")


def list_local_builds():
    build_list = []
    build_menu = {}

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    print("\n")
    for entry in build_menu:
        print(entry, build_menu[entry])
    print("\n")

    return(build_list)


def list_server_builds():
    build_list = []
    build_menu = {}

    builds = []
    ftp.retrlines("NLST ", builds.append)

    for f in builds:
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    print("\n")
    for entry in build_menu:
        print(entry, build_menu[entry])
    print("\n")

    return(build_list)


def extract(build):
    try:
        if len(os.listdir(data_folder)) != 0:
            for dir in os.listdir(data_folder):
                shutil.rmtree(f"{data_folder}/{dir}")
                print("\nDeleted files")
    except:
        print("\nFailed to delete files")

    try:
        zipf = zipfile.ZipFile(build, "r")
        zipf.extractall(data_folder)
        zipf.close()
        print("Restored files\n")
    except:
        print("Failed to restore files\n")


def backup():
    filename = f"{build_name}_v{build_version}_{timestamp}_v{kodi_version}.zip"

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
        zipf.close()

    try:
        zipit(folders, filename)
        print("\nCreated archive\n")
    except:
        print("\nFailed to create archive\n")


def restore():
    build_list = list_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    parsed_string = pathlib.Path(build).stem.split("_")

    try:
        _kodi_version = parsed_string[4]
    except:
        print("\nFile doesn't use valid naming scheme\n")
        return

    if selection == "0":
        return
    else:
        if _kodi_version == f"v{kodi_version}":
            extract(build)
        else:
            print("\nWrong Kodi version\n")
            selection = input(
                "Are you sure you want to restore the build? (y, n): ")
            if selection == "y":
                extract(build)
            elif selection == "n":
                return


def upload():
    build_list = list_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    if selection == "0":
        return
    else:
        try:
            ftp.storbinary("STOR " + build, open(build, "rb"))
            print("\nUploaded file\n")
        except:
            print("\nFailed to upload file\n")


def download():
    build_list = list_server_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    if selection == "0":
        return
    else:
        try:
            ftp.retrbinary("RETR " + build, open(build, "wb").write)
            print("\nDownloaded file\n")
        except:
            print("\nFailed to download file\n")


def delete_local_file():
    build_list = list_local_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    if selection == "0":
        return
    else:
        try:
            os.remove(build)
            print("\nDeleted local file\n")
        except:
            print("\nFailed to delete local file\n")


def delete_server_file():
    build_list = list_server_builds()

    print("Press \"0\" to go back.")
    selection = input("\nPlease Select: ")

    build = build_list[int(selection) - 1]

    if selection == "0":
        return
    else:
        try:
            ftp.delete(build)
            print("\nDeleted server file\n")
        except:
            print("\nFailed to delete server file\n")


while True:
    start_menu()
