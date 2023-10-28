import re

from google.cloud import vision
from google.oauth2 import service_account
import pandas as pd


def image_to_df(path) -> pd.DataFrame:
    client = _get_vision_client()
    image = _load_image(path)

    raw_detection = client.text_detection(image=image)

    if raw_detection.error.message:
        raise Exception(f"{raw_detection.error.message}\nCheck: https://cloud.google.com/apis/design/errors")

    parsed_text = _parse_annotations(raw_detection.text_annotations)
    return pd.DataFrame.from_dict(parsed_text)


def _get_vision_client():
    credentials = service_account.Credentials.from_service_account_file("credentials.json")
    return vision.ImageAnnotatorClient(credentials=credentials)


def _load_image(path):
    with open(path, "rb") as image_file:
        content = image_file.read()

    return vision.Image(content=content)


def _parse_annotations(annotations):
    items_to_filter = ['מספר אישי', 'תעודת זהות', 'דרגה מחושבת', 'שם משפחה', 'שם פרטי']
    table_data = annotations[0].description.split("\n")
    table_data = list(filter(lambda x: x not in items_to_filter, table_data))

    num_rows = _get_num_rows(table_data)
    army_ids = table_data[:num_rows]
    national_ids = table_data[num_rows:2 * num_rows]

    return {
        "army_id": army_ids,
        "national_id": national_ids,
    }


def _get_num_rows(table_data) -> int:
    army_id_regex = r"^\d{7}$"
    count = 0
    for item in table_data:
        if re.match(army_id_regex, item):
            count += 1
        else:
            return count

    raise ValueError("Got unexpected data after performing OCR")
