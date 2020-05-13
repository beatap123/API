import json
import os
from urllib.parse import urljoin

import requests
import hashlib
import zipfile


USERS_API = "https://api.github.com/users/"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(WORK_DIR)

class Checksum(object):

    def __init__(self, username):
        self.username = username


    def get_user_info(self):
        if not self.username:
            return None

        url = urljoin(USERS_API, self.username)
        resp = requests.get(url)
        return resp.json()

    def create_file_and_checksum(self, resp):
        if resp.status_code == requests.codes.ok:
            file = open(os.path.join(file_path, "response.txt"), "wb")
            file.write(resp.content)
            file.close()

    def md5Checksum(self, filepath, url):
        if url is None:
            with open(filepath, 'rb') as fh:
                m = hashlib.md5()
                while True:
                    line = fh.readline(8192)
                    if not line:
                        break
                    m.update(line)
                return m.hexdigest()
        else:
            r = requests.get(url, stream=True)
            m = hashlib.md5()
            for line in r.iter_lines():
                m.update(line)
            return m.hexdigest()

    def create_table(self):
        with open("results.csv", "w") as csv_file: # otwiera csv jako bazę danych
            with open("response.txt") as f:
                for line in f:
                    csv_file.write(line.rstrip())
                    #csv_file.write(md5Checksum("response.txt"))

    def create_zip_folder(self):
        ZIP_DIR = os.path.dirname(os.path.abspath(__file__))
        zip_path = os.path.join(ZIP_DIR, "myfolder.zip")
        zip_file = zipfile.ZipFile(zip_path, "w")
        zip_file.write("response.txt")
        zip_file.write("results.csv")
        zip_file.close()

    def delete(self):
        mytask = os.listdir(WORK_DIR)
        for item in mytask:
            if item.endswith((".txt", ".db", ".csv")):
                if item.startswith("requirements"):
                    pass
                else:
                    os.remove(os.path.join(WORK_DIR, item))

#do dodania
#checksum_local = md5Checksum("response.txt", None)
# checksum_api = md5Checksum(None, url)
# print(checksum_local, checksum_api)
