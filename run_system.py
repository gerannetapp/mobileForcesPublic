from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google import CreateService
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


def generate_google_drive_connection():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)
    return drive

def generate_google_drive_service():
    scope = ['https://www.googleapis.com/auth/drive']
    service_account_json_key = '/home/ubuntu/mobileForcesPublic/client_secrets.json'
    API_Version = 'v3'
    API_NAMR = 'drive'

    service = CreateService(service_account_json_key, API_NAMR, API_Version, scope)
    return service



def main():
    drive = generate_google_drive_connection()
    service = generate_google_drive_service()
    config_data = import_configuration_data()

    if OCR_FOLDER_ID not in config_data or config_data[OCR_FOLDER_ID] is None:
        print("no OCR folder ID found, please add to configuration file")
    else:
        ocr_pre_process = OcrPreProcessor(service, drive, config_data[OCR_FOLDER_ID])

        while True:
            ocr_pre_process.preprocess_new_files()
            time.sleep(1)


if __name__ == '__main__':
    main()
