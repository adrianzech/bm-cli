import os
import sys
import setup
import config
import functions
import login


def start_menu():
    menu = {}

    menu["1"] = "Create Build"
    menu["2"] = "Restore Build"
    menu["3"] = "List Builds"
    menu["4"] = "Download Build"
    menu["5"] = "Upload Build"
    menu["6"] = "Delete Builds"
    menu["7"] = "Settings"
    menu["8"] = "Test Function"
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
            service = service_menu("local")
            if not service == None:
                functions.list_builds(service)
        elif selection == "4":
            service = service_menu("online")
            if not service == None:
                functions.download(service)
        elif selection == "5":
            service = service_menu("online")
            if not service == None:
                functions.upload(service)
        elif selection == "6":
            service = service_menu("local")
            if not service == None:
                functions.delete(service)
        elif selection == "7":
            settings_menu()
        elif selection == "8":
            login.googledrive_login()
        elif selection == "0":
            functions.clear()
            sys.exit()
        else:
            print("Unknown option selected\n")


def service_menu(menu_type):
    menu = {}

    ftp = config.get_value("ftp", "enabled")
    dropbox = config.get_value("dropbox", "enabled")
    googledrive = config.get_value("googledrive", "enabled")

    if menu_type == "local":
        menu["L"] = "Local"
        if ftp == "true":
            menu["F"] = "FTP"
        if dropbox == "true":
            menu["D"] = "Dropbox"
        if googledrive == "true":
            menu["G"] = "Google Drive"
    elif menu_type == "online":
        if ftp == "true":
            menu["F"] = "FTP"
        if dropbox == "true":
            menu["D"] = "Dropbox"
        if googledrive == "true":
            menu["G"] = "Google Drive"
    elif menu_type == "setup":
        menu["F"] = "FTP"
        menu["D"] = "Dropbox"
        menu["G"] = "Google Drive"

    while True:
        print("Service Menu\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        functions.clear()
        if menu_type == "local":
            if selection in ("l", "L"):
                return(menu.get(selection.upper()))
            elif selection in ("f", "F") and ftp == "true":
                return(menu.get(selection.upper()))
            elif selection in ("d", "D") and dropbox == "true":
                return(menu.get(selection.upper()))
            elif selection in ("g", "G") and googledrive == "true":
                return(menu.get(selection.upper()))
            elif selection == "":
                break
            else:
                print("Unknown option selected\n")
        elif menu_type == "online":
            if selection in ("f", "F") and ftp == "true":
                return(menu.get(selection.upper()))
            elif selection in ("d", "D") and dropbox == "true":
                return(menu.get(selection.upper()))
            elif selection in ("g", "G") and googledrive == "true":
                return(menu.get(selection.upper()))
            elif selection == "":
                break
            else:
                print("Unknown option selected\n")
        elif menu_type == "setup":
            if selection.upper() in ("F", "D", "G"):
                return(menu.get(selection.upper()))
            elif selection == "":
                break
            else:
                print("Unknown option selected\n")


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

        print("Unknown option selected\n")


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

        # if selection in ("1", "2", "3", "4"):
        #     return(menu.get(selection))
        # elif selection == "":
        #     break

        print("Unknown option selected\n")

        if selection == "1":
            setup.folders()
        elif selection == "2":
            setup.ftp()
        elif selection == "3":
            print("dropbox settings\n")
        elif selection == "4":
            print("googledrive settings\n")
        elif selection == "":
            break
        else:
            print("Unknown option selected\n")


def create_build_menu(build_list):
    build_menu = {}

    # Loop through builds_list and create and entry in build_menu for every item
    for index, build in enumerate(build_list):
        build_menu[index + 1] = build

    # Create menu with every entry in build_menu
    for entry in build_menu:
        print(f"{[entry]}: {build_menu[entry]}")
    print("\n")
