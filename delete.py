import os
from ftplib import FTP

host = "159.69.90.146"
username = "kbm"
password = "underwolf99912"

path = "/"
filename = "backup.zip"

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
