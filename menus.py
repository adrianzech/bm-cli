import os
import sys
import settings
import functions


def start_menu():
    menu = {}

    menu["1"] = "Create Build"
    menu["2"] = "Restore Build"
    menu["3"] = "List Builds"
    menu["4"] = "Download Build"
    menu["5"] = "Upload Build"
    menu["6"] = "Delete Builds"
    menu["7"] = "Settings"
    menu["0"] = "Exit"

    while True:
        print("Build Manager\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        selection = input("\nPlease Select: ")

        functions.clear()

        if selection == "1":
            functions.create_build()
        if selection == "2":
            functions.restore_build()
        elif selection == "3":
            service = service_menu()
            if not service == None:
                functions.list_builds(service)
        elif selection == "4":
            service = service_menu()
            if not service == None:
                functions.download(service)
        elif selection == "5":
            service = service_menu()
            if not service == None:
                functions.upload(service)
        elif selection == "6":
            service = service_menu()
            if not service == None:
                functions.delete(service)
        elif selection == "7":
            settings_menu()
        elif selection == "0":
            functions.clear()
            sys.exit()
        else:
            print("Unknown Option Selected\n")


def service_menu():
    menu = {}

    menu["1"] = "Local"
    menu["2"] = "FTP"
    menu["3"] = "Dropbox"
    menu["4"] = "Google Drive"

    while True:
        print("Service Menu\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        functions.clear()

        if selection in ("1", "2", "3", "4"):
            return(menu.get(selection))
        elif selection == "":
            break
        else:
            print("Unknown Option Selected\n")


def system_menu():
    menu = {}

    menu["1"] = "Linux"
    menu["2"] = "Windows"
    menu["3"] = "MacOS"

    while True:
        print("Service Menu\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        if selection in ("1", "2", "3"):
            return(menu.get(selection))
        elif selection == "":
            break

        print("Unknown Option Selected\n")


def settings_menu():
    menu = {}

    menu["1"] = "Folder Settings"
    menu["2"] = "FTP Settings"
    menu["3"] = "Dropbox Settings"
    menu["4"] = "Google Drive Settings"

    while True:
        print("Settings Menu\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        functions.clear()

        if selection in ("1", "2", "3", "4"):
            return(menu.get(selection))
        elif selection == "":
            break
        else:
            print("Unknown Option Selected\n")

        # if selection == "1":
        #     print("folder settings\n")
        # elif selection == "2":
        #     print("ftp settings\n")
        # elif selection == "3":
        #     print("dropbox settings\n")
        # elif selection == "4":
        #     print("googledrive settings\n")
        # elif selection == "":
        #     break
        # else:
        #     print("Unknown Option Selected\n")
