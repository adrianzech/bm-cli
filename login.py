import config
import setup
import functions
from ftplib import FTP
from ftplib import FTP_TLS


def ftp():
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

            return("success")
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

            return("success")
        except:
            return("login_error")
