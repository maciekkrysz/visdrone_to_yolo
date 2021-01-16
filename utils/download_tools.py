# taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests
import zipfile
import os

# googledrive: https://drive.google.com/file/d/1a2oHjcEcwXP8oUF95qiwrqzACb2YlUhn/view
# ID: 1a2oHjcEcwXP8oUF95qiwrqzACb2YlUhn

# Example:
# file_id = '1a2oHjcEcwXP8oUF95qiwrqzACb2YlUhn'
# destination = './a.zip'
# download_file_from_google_drive(file_id, destination)

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

# ----------------------------------------------------------



def unzip(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall()

