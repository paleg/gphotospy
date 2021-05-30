import os
import requests
import mimetypes
import tenacity


from .authorize import get_credentials


upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
mimetypes.init()


def upload(secrets, media_file):
    """
    Uploads files of media to Google Server, to put in Photos

    Parameters
    ----------
    secrets: str
        JSON file containing the secrets for OAuth,
        as created in the Google Cloud Consolle
    media_file: Path
        Path to the file to upload

    Returns
    -------
    Upload Token if successfull, otherwise None
    """
    credentials = get_credentials(secrets)

    header = {
        'Authorization': "Bearer " + credentials.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }

    header['X-Goog-Upload-Content-Type'] = mimetypes.guess_type(media_file)[0]

    f = open(media_file, 'rb').read()

    response = requests.post(upload_url, data=f, headers=header)
    if response.ok:
        return response.content.decode('utf-8')
    return None


@tenacity.retry(wait=tenacity.wait_exponential(multiplier=3, min=10, max=60))
def change_description(secrets, media_id, description):
    credentials = get_credentials(secrets)

    header = {
        'Authorization': "Bearer " + credentials.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }

    response = requests.patch(
            f"https://photoslibrary.googleapis.com/v1/mediaItems/{media_id}?updateMask=description",
            json={'description': description},
            headers=header
    )
    response.raise_for_status()
    return response.content.decode('utf-8')


@tenacity.retry(wait=tenacity.wait_exponential(multiplier=3, min=10, max=60))
def change_album_cover(secrets, album_id, cover_id):
    credentials = get_credentials(secrets)

    header = {
        'Authorization': "Bearer " + credentials.token,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-Protocol': 'raw'
    }

    response = requests.patch(
            f"https://photoslibrary.googleapis.com/v1/albums/{album_id}?updateMask=coverPhotoMediaItemId",
            json={'coverPhotoMediaItemId': cover_id},
            headers=header
    )
    response.raise_for_status()
    return response.content.decode('utf-8')
