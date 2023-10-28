import logging
import os

import pandas as pd

from file_handler import FileHandler


class OcrPreProcessor:
    VALID_FILE_EXTENSIONS = ('.xlsx',)
    OCR_FOLDER_PATH = "/home/ubuntu/mobileForcesPublic/ocr/"
    ARCHIVE_FOLDER_PATH = "/home/ubuntu/mobileForcesPublic/archive/ocr_archive"
    OCR_FOLDER_ID = None

    def __init__(self, google_drive, ocr_folder_id: str):
        self.google_drive = google_drive
        self.OCR_FOLDER_ID = ocr_folder_id
        self.existing_files = dict()
        self.excel_file_handler = FileHandler(google_drive, self.VALID_FILE_EXTENSIONS)

    def _generate_df_from_ocr_file(self, folder_path, file_name: str, file_id: str, archived_file_id):
        tmp_file_path = f"{folder_path}{file_name}"
        file = self.google_drive.CreateFile({'id': file_id})
        file.GetContentFile(tmp_file_path)  # Download file as 'example.xlsx'.
        file.Delete()
        archived_file = self.google_drive.CreateFile({'parents': [{'id': archived_file_id}]})
        archived_file.SetContentFile(tmp_file_path)
        archived_file.Upload()
        ocr_df = pd.read_excel(tmp_file_path)
        return ocr_df

    def preprocess_file(self, ocr_df):
        return ocr_df

    def preprocess_new_files(self):
        existing_file_titles = set(self.existing_files.keys())
        new_added_files = self.excel_file_handler.get_new_files_from_folder(self.OCR_FOLDER_ID, existing_file_titles)
        if new_added_files:
            for title, new_file in new_added_files.items():
                print(new_file)
                logging.info(f"Execute logic on: {title}, {new_file['id']}")
                ocr_df = self._generate_df_from_ocr_file(self.OCR_FOLDER_PATH, title, new_file['id'], '1MpRnelL2E8Fmxh3Kctp9sfc8p608u2-p')



                preprocess_df = self.preprocess_file(ocr_df)
                # TODO: upload preprocess_df as xls to the relavant folder
                print(preprocess_df)
            if new_added_files:
                self.existing_files.update(new_added_files)
