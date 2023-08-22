import os
import dropbox
from nextcloud import Client
import requests


class FileUploader:

    def __init__(self, dbox=None, nextcloud=None, is_local=False):
        print("FileUploader.__init__")
        self.is_local = is_local,
        if dbox:
            self.dbx = dropbox.Dropbox(dbox['token'])
        if nextcloud:
            session = requests.Session()
            session.verify = False  # for self-signed certificates
            self.nc = Client(url=nextcloud['url'])
            self.nc.login(nextcloud['username'], nextcloud['token'])

    def upload(self, file_name, content):
        print("FileUploader.upload")

        remote_path = '/Apps/Commands/' + file_name
        if self.is_local:
            tmp_file_path = file_name
        else:
            tmp_file_path = os.path.join('/tmp', file_name)

        with open(tmp_file_path, 'w') as f:
            f.write(content)

        if hasattr(self, 'dbx'):
            with open(tmp_file_path, 'rb') as f:
                try:
                    self.dbx.files_upload(f.read(), remote_path, mode=dropbox.files.WriteMode.overwrite)
                    print(f"{file_name} uploaded successfully to Dropbox.")
                except dropbox.exceptions.ApiError as e:
                    error_message = f"Failed to upload {file_name} to Dropbox\nDetails:\n{e}"
                    print(error_message)
                    raise Exception(error_message)
        if hasattr(self, 'nc'):
            try:
                self.nc.put_file(remote_path, tmp_file_path)
                print(f"{file_name} uploaded successfully to Nextcloud.")
            except Exception as e:
                error_message = f"Failed to upload {file_name} to Nextcloud\nDetails:\n{e}"
                print(error_message)
                raise Exception(error_message)
