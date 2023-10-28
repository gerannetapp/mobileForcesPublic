from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time
import json
import logging

from ocr_preprocessor import OcrPreProcessor

logging.basicConfig(level=logging.INFO)

CONFIGURATION_FILE = "config.json"
OCR_FOLDER_ID = "ocr_folder_id"


def import_configuration_data():
    with open(CONFIGURATION_FILE, "r") as config_file:
        config_data = json.load(config_file)
    return config_data


def main():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    config_data = import_configuration_data()
    if OCR_FOLDER_ID not in config_data or config_data[OCR_FOLDER_ID] is None:
        print("no ocr folder id found, please add to configuration file")
        
    ocr_pre_process = OcrPreProcessor(drive, config_data[OCR_FOLDER_ID])
    while True:
        ocr_pre_process.preprocess_new_file()
        time.sleep(1)


if __name__ == '__main__':
    main()
