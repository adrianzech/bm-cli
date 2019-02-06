import os
import sys
import setup
import config
import functions
import login


def start_menu():
    menu = {}
    menu_items = [
        "Exit",
        "Create Build",
        "Restore Build",
        "List Builds",
        "Download Build",
        "Upload Build",
        "Delete Builds",
        "Settings"
    ]

    for i in range(len(menu_items)):
        menu[f"{i}"] = menu_items[i]

    # while True:
    print("Build Manager\n")
    for entry in menu:
        print(f"[{entry}]:", menu[entry])

    selection = input("\nPlease Select: ")

    functions.clear()
    if selection.isdigit():
        if 1 <= int(selection) <= 7:
            switcher = {
                1: lambda: functions.create_build(),
                2: lambda: functions.restore_build(),
                3: lambda: functions.list_builds(service_menu("local")),
                4: lambda: functions.download(service_menu("online")),
                5: lambda: functions.upload(service_menu("online")),
                6: lambda: functions.delete(service_menu("local")),
                7: lambda: settings_menu()
            }
            func = switcher.get(int(selection), lambda: "Unknown option selected\n")
            return func()
        elif selection == "0":
            functions.clear()
            sys.exit()

    print("Unknown option selected\n")


def service_menu(menu_type):
    menu = {}
    online = []
    local = ["Local"]
    setup = [
        "Local",
        "FTP",
        "Dropbox",
        "Google Drive"
    ]

    if config.get_value("ftp", "enabled") == "true":
        local.append("FTP")
        online.append("FTP")
    if config.get_value("dropbox", "enabled") == "true":
        local.append("Dropbox")
        online.append("Dropbox")
    if config.get_value("googledrive", "enabled") == "true":
        local.append("Google Drive")
        online.append("Google Drive")

    if menu_type == "local":
        for i in range(len(local)):
            menu[f"{i + 1}"] = local[i]
    elif menu_type == "online":
        for i in range(len(online)):
            menu[f"{i + 1}"] = online[i]
    elif menu_type == "setup":
        for i in range(len(setup)):
            menu[f"{i + 1}"] = setup[i]

    while True:
        print("Service Menu\n")
        for entry in menu:
            print(f"[{int(entry)}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        functions.clear()

        if selection.isdigit():
            if 1 <= int(selection) <= (len(menu)):
                return(menu.get(selection))
        elif selection == "":
            break

        print("Unknown option selected\n")


def system_menu():
    menu = {}
    menu_items = [
        "Linux",
        "Windows",
        "MacOS"
    ]

    for i in range(len(menu_items)):
        menu[f"{i + 1}"] = menu_items[i]

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
    menu_items = [
        "Folder Settings",
        "FTP Settings",
        "Dropbox Settings",
        "Google Drive Settings"
    ]

    for i in range(len(menu_items)):
        menu[f"{i + 1}"] = menu_items[i]

    while True:
        print("Settings Menu\n")
        for entry in menu:
            print(f"[{entry}]:", menu[entry])

        print("\nPress Enter to go back")
        selection = input("Please Select: ")

        functions.clear()
        if selection.isdigit():
            if 1 <= int(selection) <= 4:
                switcher = {
                    1: lambda: setup.folders(),
                    2: lambda: setup.ftp(),
                    3: lambda: setup.dropbox(),
                    4: lambda: setup.googledrive()
                }
                func = switcher.get(int(selection), lambda: "Unknown option selected\n")
                return func()
        elif selection == "":
            break

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
