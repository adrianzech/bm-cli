import os
import sys
from ftplib import FTP
import zipfile
import datetime

host = "159.69.90.146"
username = "kbm"
password = "underwolf99912"

path = "/"
filename = "backup.zip"

folders = [
    "data/addons",
    "data/userdata"]

build_name = "AdrianBuild"
build_version = "1.42"
timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())
kodi_version = "17.6"

filename = f"{build_name}_v{build_version}_{timestamp}_v{kodi_version}.zip"

menu = {}
menu["0"] = "Exit"
menu["1"] = "List local builds"
menu["2"] = "List server builds"
menu["3"] = "Backup"
menu["4"] = "Upload"
menu["5"] = "Download"
menu["6"] = "Delete local file"
menu["7"] = "Delete server file"

build_list = []
build_menu = {}


def start_menu():
    print("\n")
    for entry in menu:
        print(entry, menu[entry])
    print("\n")

    selection = input("Please Select: ")
    print("\n")

    if selection == "0":
        sys.exit()
    elif selection == "1":
        list_local_builds()
    elif selection == "2":
        list_server_builds()
    elif selection == "3":
        zip()
    elif selection == "4":
        upload()
    elif selection == "5":
        download()
    elif selection == "6":
        delete_local_file()
    elif selection == "7":
        delete_server_file()
    else:
        print("Unknown Option Selected!")


def list_local_builds():
    build_list.clear()
    build_menu.clear()

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        build_filename, build_file_extension = os.path.splitext(f)
        if build_file_extension == ".zip":
            build_list.append(f)

    for index, b in enumerate(build_list):
        build_menu[index] = b

    print("\n")
    for entry in build_menu:
        print(entry, build_menu[entry])
    print("\n")


def list_server_builds():
    build_list.clear()
    build_menu.clear()

    ftp = FTP(host)
    print(ftp.getwelcome())

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    ftp.cwd(path)

    lines = []
    ftp.retrlines("NLST ", lines.append)

    for f in lines:
        _filename, _file_extension = os.path.splitext(f)
        if _file_extension == ".zip":
            build_list.append(f)

    for index, b in enumerate(build_list):
        build_menu[index] = b

    print("\n")
    for entry in build_menu:
        print(entry, build_menu[entry])
    print("\n")

    ftp.quit()


def zip():
    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, "..")))

    def zipit(dir_list, zip_name):
        zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
        for dir in dir_list:
            zipdir(dir, zipf)
        zipf.close()

    try:
        zipit(folders, filename)
        print("Created archive")
    except:
        print("Failed to create archive.")


def upload():
    ftp = FTP(host)
    print(ftp.getwelcome())

    list_local_builds()

    selection = input("Please Select: ")
    print("\n")

    build = build_list[int(selection)]

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        ftp.cwd(path)
        ftp.storbinary("STOR " + build, open(build, "rb"))
        ftp.quit()
        print("Uploaded file.")
    except:
        print("Failed to upload file")


def download():
    ftp = FTP(host)
    print(ftp.getwelcome())

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        list_server_builds()

        selection = input("Please Select: ")
        print("\n")

        build = build_list[int(selection)]

        ftp.cwd(path)
        ftp.retrbinary("RETR " + build, open(build, "wb").write)
        ftp.quit()
        print("Downloaded file.")
    except:
        print("Failed to download file")


def delete_local_file():

    list_local_builds()

    selection = input("Please Select: ")
    print("\n")

    build = build_list[int(selection)]

    try:
        os.remove(build)
        print("Deleted local file.")
    except:
        print("Failed to delete local file.")


def delete_server_file():
    ftp = FTP(host)
    print(ftp.getwelcome())

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        list_server_builds()

        selection = input("Please Select: ")
        print("\n")

        build = build_list[int(selection)]

        ftp.cwd(path)
        ftp.delete(build)
        ftp.quit()
        print("Deleted server file.")
    except:
        print("Failed to delete server file.")


while True:
    start_menu()
