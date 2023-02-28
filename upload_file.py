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




uploader = FileUploader(
    dropbox_access_token="YOUR_DROPBOX_ACCESS_TOKEN",
    onedrive_access_token="YOUR_ONEDRIVE_ACCESS_TOKEN",
    onedrive_root_folder_id="YOUR_ONEDRIVE_ROOT_FOLDER_ID",
    nextcloud_url="YOUR_NEXTCLOUD_URL",
    nextcloud_username="YOUR_NEXTCLOUD_USERNAME",
    nextcloud_password="YOUR_NEXTCLOUD_PASSWORD"
)

# Upload a file to Dropbox
uploader.dropbox("file.txt", "Hello, Dropbox!")

# Upload a file to OneDrive
uploader.onedrive("file.txt", "Hello, OneDrive!")

# Upload a file to Nextcloud
uploader.nextcloud("file.txt", "Hello, Nextcloud!")
