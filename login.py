import config
import setup
import functions
import dropbox
import ftplib
from ftplib import FTP
from ftplib import FTP_TLS
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def ftp_login():
    # Use ftps
    if config.get_value("ftp", "protocol") == "ftps":
        try:
            ftps = FTP_TLS(config.get_value("ftp", "host"))
        except:
            return("host_error")

        try:
            ftps.login(
                config.get_value("ftp", "username"),
                config.get_value("ftp", "password")
            )

            ftps.prot_p()

            try:
                ftps.cwd(config.get_value("ftp", "path"))
            except:
                ftps.mkd(config.get_value("ftp", "path"))
                ftps.cwd(config.get_value("ftp", "path"))

            return(ftps)
        except:
            return("login_error")

    # Use ftp
    if config.get_value("ftp", "protocol") == "ftp":
        try:
            ftp = FTP(config.get_value("ftp", "host"))
        except:
            return("host_error")

        try:
            ftp.login(
                config.get_value("ftp", "username"),
                config.get_value("ftp", "password")
            )

            try:
                ftp.cwd(config.get_value("ftp", "path"))
            except:
                ftp.mkd(config.get_value("ftp", "path"))
                ftp.cwd(config.get_value("ftp", "path"))

            return(ftp)
        except:
            return("login_error")


def dropbox_login():
    db = dropbox.Dropbox(config.get_value("dropbox", "token"))
    db.users_get_current_account()
    return(db)


def googledrive_login():
    gauth = GoogleAuth()

    gauth.DEFAULT_SETTINGS['client_config_file'] = "config/client_secrets.json"

    gauth.LoadCredentialsFile("config/credentials")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("config/credentials")

    drive = GoogleDrive(gauth)
    return(drive)


def get_folder_id():
    drive = googledrive_login()
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

    return(upload_folder_id)
