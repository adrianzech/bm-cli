import os
from ftplib import FTP

host = "159.69.90.146"
username = "kbm"
password = "underwolf99912"

path = "/"
filename = "backup.zip"

option = input("Enter number: ")


def zip():
    # Soon™
    return


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


def delete():
    ftp = FTP(host)
    print(ftp.getwelcome())

    os.remove(filename)

    try:
        ftp.login(username, password)
        print("Logged in.")
    except:
        print("Failed to login.")

    try:
        ftp.cwd(path)
        ftp.delete(filename)
        ftp.quit()
        print("Deleted file.")
    except:
        print("Failed to delete file")


option = {0: zip,
          1: upload,
          2: download,
          3: delete,
          }
