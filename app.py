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

build_name = "DanielBuild"
build_version = "1.42"
timestamp = "{0:%Y%m%d_%H%M}".format(datetime.datetime.now())
kodi_version = "17.6"

filename = f"{build_name}_v{build_version}_{timestamp}_v{kodi_version}.zip"

menu = {}
menu["0"] = "Exit"
menu["1"] = "Backup"
menu["2"] = "Upload"
menu["3"] = "Download"
menu["4"] = "Delete Server file"
menu["5"] = "Delete locale file"


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

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        ftp.cwd(path)
        ftp.storbinary("STOR " + filename, open(filename, "rb"))
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
        ftp.cwd(path)
        ftp.retrbinary("RETR " + filename, open(filename, "wb").write)
        ftp.quit()
        print("Downloaded file.")
    except:
        print("Failed to download file")


def delete_server_file():
    ftp = FTP(host)
    print(ftp.getwelcome())

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        ftp.cwd(path)
        ftp.delete(filename)
        ftp.quit()
        print("Deleted server file.")
    except:
        print("Failed to delete server file.")


def delete_local_file():
    try:
        os.remove(filename)
        print("Deleted local file.")
    except:
        print("Failed to delete local file.")


while True:
    print("\n")
    for entry in menu:
        print(entry, menu[entry])
    print("\n")

    selection = input("Please Select: ")
    print("\n")

    if selection == "0":
        sys.exit()
    elif selection == "1":
        zip()
    elif selection == "2":
        upload()
    elif selection == "3":
        download()
    elif selection == "4":
        delete_server_file()
    elif selection == "5":
        delete_local_file()
    else:
        print("Unknown Option Selected!")
