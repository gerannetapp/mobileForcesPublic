from typing import Set, List, Dict
from pathlib import Path


class FileHandler:
    def __init__(self, google_drive, file_extensions: tuple):
        self.file_extensions = file_extensions
        self.initialize_folder_structure()
        self.google_drive = google_drive

    def get_new_files_from_folder(self, folder_id: str, existing_file_titles: Set[str]) -> dict:
        ocr_file_list = self.google_drive.ListFile({"q": f"'{folder_id}' in parents and trashed=false"}).GetList()
        fetched_file = {file['title']: dict(file) for file in ocr_file_list}

        new_added_titles = self.get_new_added_file_names(existing_file_titles, fetched_file)
        new_added_files = {key: fetched_file[key] for key in new_added_titles}
        return new_added_files

    def get_new_added_file_names(self, existing_file_titles: Set[str], fetched_file: dict):
        fileter_files = self.filter_files_by_extension(fetched_file)
        fetched_titles = set(fileter_files.keys())
        new_added_titles = fetched_titles.difference(existing_file_titles)
        return new_added_titles

    def filter_files_by_extension(self, files: Dict[str, Dict]):
        return {key: files[key] for key, value in files.items() if key.endswith(self.file_extensions)}

    def move_file(self, folder_path, file_name: str, file_id: str, remote_folder_id):
        local_file_path = f"{folder_path}{file_name}"
        file = self.get_file_object(file_id)
        self.download_file(file, local_file_path)
        self.upload_file_into_folder(local_file_path, remote_folder_id)
        self.delete_file(file)
        return local_file_path

    def get_file_object(self, file_id: str):
        file = self.google_drive.CreateFile({'id': file_id})
        return file

    def upload_file_into_folder(self, file_path: str, remote_folder_id: str):
        file_name = Path(file_path).name
        archived_file = self.google_drive.CreateFile({'parents': [{'id': remote_folder_id}],'title': file_name})
        archived_file.SetContentFile(file_path)
        archived_file.Upload()

    @staticmethod
    def download_file(file, file_path: str):
        file.GetContentFile(file_path)  # Download file as 'example.xlsx'.

    @staticmethod
    def delete_file(file):
        file.Delete()

    def initialize_folder_structure(self):
        # TODO: create tmp dir for preprocess dir and categorized dirs
        pass
