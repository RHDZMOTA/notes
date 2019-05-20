import settings
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime


GoogleAuth.DEFAULT_SETTINGS["client_config_file"] = settings.GDRIVE_CLIENT_CONFIG


def auto_reload(function):
    def wrapper(self, *args, **kwargs):
        delta = (datetime.now() - self.created_at).seconds
        if self.auto_reload_flag and delta > int(settings.GDRIVE_AUTO_RELOAD):
            self.reload()
        return function(self, *args, **kwargs)

    return wrapper


class GoogleDriveWrapper(object):
    def __init__(self, auto_reload_flag=True):
        self.auto_reload_flag = auto_reload_flag
        self.created_at = datetime.now()
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

    def reload(self):
        del self.drive, self.gauth
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        return self

    @auto_reload
    def ls(self, folder_id="root", filter=lambda elem: elem):
        elements = self.drive.ListFile({"q": f"'{folder_id}' in parents and trashed=false"}).GetList()
        return [elem for elem in elements if filter(elem)]

    @auto_reload
    def get_file_by_title(self, title, folder_id="root", filter=lambda elem: elem, raise_error=False):
        elements = self.ls(folder_id, filter)
        for elem in elements:
            if elem["title"] == title:
                return elem
        if raise_error:
            raise Exception(f"Not found elem with title={title}")

    @auto_reload
    def get_file_by_id(self, drive_file_id):
        return self.drive.auth.service.files().get(fileId=drive_file_id).execute()

    @auto_reload
    def upload_file(self, file_path, parent_id, rename=None):
        drive_file = self.drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": parent_id}]})
        drive_file.SetContentFile(file_path)
        drive_file["title"] = rename if rename else file_path.split("/")[-1]
        drive_file.Upload()

    @auto_reload
    def create_file(self, title, content, parent_id):
        drive_file = self.drive.CreateFile({"title": title, "parents": [{"kind": "drive#fileLink", "id": parent_id}]})
        drive_file.SetContentString(content)
        drive_file.Upload()
        return drive_file

    @auto_reload
    def update_file(self, title, content, parent_id, filter=lambda elem: elem, raise_error=True):
        drive_file = self.get_file_by_title(title, parent_id, filter)
        if drive_file:
            drive_file.SetContentString(content)
            drive_file.Upload()
            return drive_file
        elif raise_error:
            raise Exception(f"Not found elem for update with title={title}")

    @auto_reload
    def update_or_create(self, title, content, parent_id, filter=lambda elem: elem):
        drive_file = self.update_file(title, content, parent_id, filter, raise_error=False)
        if not drive_file:
            drive_file = self.create_file(title, content, parent_id)
        return drive_file

    @auto_reload
    def update_or_create_content_file(self, file_path, parent_id, filter=lambda elem: elem):
        title = os.path.basename(file_path)
        drive_file = self.get_file_by_title(title, parent_id, filter)
        if not drive_file:
            drive_file = self.drive.CreateFile(
                {"title": title, "parents": [{"kind": "drive#fileLink", "id": parent_id}]}
            )
        drive_file.SetContentFile(file_path)
        drive_file.Upload()

    @auto_reload
    def set_content_string(self, drive_file_id, content):
        drive_file = self.drive.auth.service.files().get(fileId=drive_file_id).execute()
        drive_file.SetContentString(content)
        drive_file.Upload()

    @auto_reload
    def get_content_string_by_id(self, drive_file_id):
        drive_file = self.get_file_by_id(drive_file_id)
        return drive_file.GetContentFile(drive_file["title"])

    @auto_reload
    def get_content_string(self, title, folder_id="root", filter=lambda elem: elem, raise_error=False):
        drive_file = self.get_file_by_title(title, folder_id, filter, raise_error)
        if not drive_file:
            return ""
        return drive_file.GetContentString()

    @auto_reload
    def get_last_modified(self, title, folder_id="root", filter=lambda elem: elem, raise_error=False):
        drive_file = self.get_file_by_title(title, folder_id, filter, raise_error)
        if drive_file:
            return datetime.strptime(drive_file["modifiedDate"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        elif raise_error:
            raise Exception(f"Not found elem with title={title} in folder={folder_id}")
        return -1


gdrive_wrapper = GoogleDriveWrapper()
