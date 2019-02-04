import os
import sys
import menus
import config
import login
import functions

functions.clear()

config.check_config()
config.check_folders()
config.check_services()

if config.get_value("ftp", "enabled") == "true":
    print("Logging into FTP")
    login.ftp_login()

if config.get_value("dropbox", "enabled") == "true":
    print("Logging into Dropbox")
    login.dropbox_login()

if config.get_value("googledrive", "enabled") == "true":
    print("Logging into Google Drive")
    login.googledrive_login()

print("\n")

while True:
    menus.start_menu()
