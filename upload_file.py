import requests


class FileUploader:
    def __init__(self, dropbox_access_token, onedrive_access_token, onedrive_root_folder_id, nextcloud_url, nextcloud_username, nextcloud_password):
        self.dropbox_url = "https://content.dropboxapi.com/2/files/upload"
        self.dropbox_access_token = dropbox_access_token
        self.onedrive_url = "https://graph.microsoft.com/v1.0/drive/root:/"
        self.onedrive_access_token = onedrive_access_token
        self.onedrive_root_folder_id = onedrive_root_folder_id
        self.nextcloud_url = nextcloud_url
        self.nextcloud_username = nextcloud_username
        self.nextcloud_password = nextcloud_password

    def dropbox(self, file_name, content):
        headers = {
            "Authorization": f"Bearer {self.dropbox_access_token}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": f'{{"path": "/{file_name}","mode": "add","autorename": true,"mute": false}}'
        }
        response = requests.post(self.dropbox_url, headers=headers, data=content)
        response.raise_for_status()
        return response.json()

    def onedrive(self, file_name, content):
        url = f"{self.onedrive_url}{self.onedrive_root_folder_id}/{file_name}:/content"
        headers = {
            "Authorization": f"Bearer {self.onedrive_access_token}",
            "Content-Type": "text/plain"
        }
        response = requests.put(url, headers=headers, data=content)
        response.raise_for_status()
        return response.json()

    def nextcloud(self, file_name, content):
        url = f"{self.nextcloud_url}/remote.php/dav/files/{self.nextcloud_username}/{file_name}"
        headers = {
            "Content-Type": "text/plain"
        }
        response = requests.put(url, headers=headers, data=content, auth=(self.nextcloud_username, self.nextcloud_password))
        response.raise_for_status()
        return response.text


""" #this is the class i used with AWS Lambda to upload a file to dropbox
import os
import dropbox


class FileUploader:
    def __init__(self, dropbox_access_token):
        self.dbx = dropbox.Dropbox(dropbox_access_token)

    def dropbox(self, file_name, content):
        tmp_file_path = os.path.join('/tmp', file_name)
        with open(tmp_file_path, 'w') as f:
            f.write(content)
        with open(tmp_file_path, 'rb') as f:
            self.dbx.files_upload(f.read(), '/Apps/Commands/' + file_name
"""
