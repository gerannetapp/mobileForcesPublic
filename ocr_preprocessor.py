import logging
import pandas as pd

from file_handler import FileHandler


class OcrPreProcessor:
    VALID_FILE_EXTENSIONS = ('.xlsx',)
    OCR_FOLDER_ID = None
    OCR_FOLDER_PATH = "/home/ubuntu/mobileForcesPublic/ocr"

    def __init__(self, google_drive, ocr_folder_id: str):
        self.google_drive = google_drive
        self.existing_files = dict()
        self.excel_file_handler = FileHandler(google_drive, self.VALID_FILE_EXTENSIONS)

    def _generate_df_from_ocr_file(self, folder_path, file_name: str, file_id: str):
        tmp_file_path = f"{folder_path}{file_name}"
        file = self.google_drive.CreateFile({'id': file_id})
        file.GetContentFile(tmp_file_path)  # Download file as 'example.xlsx'.
        ocr_df = pd.read_excel(tmp_file_path)
        return ocr_df

    def preprocess_new_file(self):
        existing_file_titles = set(self.existing_files.keys())
        new_added_files = self.excel_file_handler.get_new_files_from_folder(self.OCR_FOLDER_ID, existing_file_titles)
        if new_added_files:
            for title, new_file in new_added_files.items():
                logging.info(f"Execute logic on: {title}, {new_file['id']}")
                ocr_df = self._generate_df_from_ocr_file(self.OCR_FOLDER_PATH, title, new_file['id'])
                print(ocr_df)
            if new_added_files:
                self.existing_files.update(new_added_files)
