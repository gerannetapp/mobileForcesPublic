from typing import Set, List, Dict

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

    def initialize_folder_structure(self):
        # TODO: create tmp dir for preprocess dir and categorized dirs
        pass

    def filter_files_by_extension(self, files: Dict[str, Dict]):
        return {key: files[key] for key, value in files.items() if key.endswith(self.file_extensions)}
