import config
import setup
import functions
import dropbox
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from ftplib import FTP
from ftplib import FTP_TLS


def ftp_login():
    # TODO: Add custom ftp path
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
            ftps.cwd("/")

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

            ftp.cwd("/")

            return(ftp)
        except:
            return("login_error")


def dropbox_login():
    db = dropbox.Dropbox(config.get_value("dropbox", "token"))
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
