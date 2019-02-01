import config
import setup
import functions
from ftplib import FTP
from ftplib import FTP_TLS


def ftp():
    # Use ftps
    if config.get_value("ftp", "protocol") == "ftps":
        try:
            ftps = FTP_TLS(config.get_value("ftp", "host"))
        except:
            functions.clear()
            config.set_value("ftp", "enabled", "false")
            config.write_config()
            print(f"Failed to reach host\n")
            setup.ftp()

        try:
            ftps.login(
                config.get_value("ftp", "username"),
                config.get_value("ftp", "password")
            )

            ftps.prot_p()
            ftps.cwd("/")

            config.set_value("ftp", "enabled", "true")
            config.write_config()
        except:
            functions.clear()
            config.set_value("ftp", "enabled", "false")
            config.write_config()
            print("Failed to login\n")
            setup.ftp()

    # Use ftp
    if config.get_value("ftp", "protocol") == "ftp":
        try:
            ftp = FTP(config.get_value("ftp", "host"))
        except:
            functions.clear()
            print(f"Failed to reach host\n")
            setup.ftp()

        try:
            ftp.login(
                config.get_value("ftp", "username"),
                config.get_value("ftp", "password")
            )

            ftp.cwd("/")
        except:
            functions.clear()
            print("Failed to login\n")
            setup.ftp()
