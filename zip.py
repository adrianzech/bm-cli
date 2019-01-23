import os
import zipfile

filename = "backup.zip"
folders = [
    "data/addons",
    "data/userdata"]

"""
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
"""


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()


""""
try:
    zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    zipdir("data/", zipf)
    zipf.close()
    zipit(folders, filename)
    print("Created archive")
except:
    print("Failed to create archive.")
"""

zipit(folders, filename)
print("Created archive")

# https://stackoverflow.com/questions/46229764/python-zip-multiple-directories-into-one-zip-file/46267469
