import os
import zipfile

filename = "backup.zip"


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


try:
    zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    zipdir("data/", zipf)
    zipf.close()
    print("Created archive")
except:
    print("Failed to create archive.")
