import os
import dropbox
from io import BytesIO
from PIL import Image  # Make sure you have Pillow installed
import nc_py_api


class FileUploader:

    def __init__(self, dbox=None, nextcloud=None):
        print("FileUploader.__init__")
        self.is_local = False
        if dbox:
            self.dbx = dropbox.Dropbox(dbox['token'])
        if nextcloud:
            self.nc = nc_py_api.Nextcloud(
                nextcloud_url=nextcloud['url'],
                nc_auth_user=nextcloud['username'],
                nc_auth_pass=nextcloud['token']
            )

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
                with open(tmp_file_path, 'rb') as f:  # Open the file in binary mode
                    buf = BytesIO(f.read())  # Create a BytesIO stream from the file content
                    self.nc.files.upload_stream(remote_path, buf)  # Use the upload_stream method
                print(f"{file_name} uploaded successfully to Nextcloud.")
            except Exception as e:
                error_message = f"Failed to upload {file_name} to Nextcloud\nDetails:\n{e}"
                print(error_message)
                raise Exception(error_message)
            finally:
                if self.is_local:
                    os.remove(tmp_file_path)
