from ftplib import FTP

host = "159.69.90.146"
username = "kbm"
password = "underwolf99912"

path = "/"
filename = "backup.zip"

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
