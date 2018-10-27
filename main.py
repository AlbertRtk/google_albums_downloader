"""
AR, 2018-10-25

Program "Get Photos"  - downloads media items (photos, videos) from an album
                        in Google Photos using Google Photos APIs and
                        google-api-phyton-client

For help with APIs check:
https://developers.google.com/photos/library/guides/overview
"""

# general imports
import os
from pprint import pprint
import re
import json

# imports from google-api-python-client library
from googleapiclient.discovery import build

# local imports
from authorization import Authorization
from googlealbum import GoogleAlbum


# Name of a file that contains the OAuth 2.0 information for this application:
CLIENT_SECRETS_FILE = "client_secret.json"

# This access scope grants read-only access:
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'

APP_NAME = 'Get Photos'
LIBRARY_PATH = os.path.join(os.path.expanduser('~'), APP_NAME)

# Getting authorization
authorization = Authorization(APP_NAME, SCOPES, CLIENT_SECRETS_FILE)
credentials = authorization.get_credentials()
# Building service
service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# DONE: storing album ids TODO: with list of downloaded photos
# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo
# TODO: user interface - console

def main():
    # Getting albums
    albums = get_albums(album_fields='(id,title,mediaItemsCount,productUrl)')

    # Titles of albums to download start with #
    pattern = re.compile('^#\s*')

    google_album = GoogleAlbum()
    downloaded_albums = []

    for album in albums:
        google_album.from_dict(album)

        # If title starts with # - changing title and downloading
        if bool(re.match(pattern, google_album.title)):
            print(google_album)
            downloaded_albums.append(google_album.to_dict())
            google_album.set_title(pattern.split(google_album.title)[1])
            google_album.download(service, directory=LIBRARY_PATH,
                                  media_fields='(filename,baseUrl)')

    with open(os.path.join(LIBRARY_PATH, 'downloaded_albums.json'), 'w') as f:
        json.dump(downloaded_albums, f)


def get_albums(page_token=None, album_fields=''):
    """
    Function gets list of all albums (dict) from user photo library.
    Recursion as long as in response is next page token.

    :param album_fields: string - listing keys in dict describing albums,
    starts and ends with brackets (), comma-separated, no whitespace characters,
    eg. '(id,title,mediaItemsCount,productUrl)', default empty string gets all
    possible fields
    :param page_token: string - next page token, for 1st call None
    :return:
    """

    # Setting fields and request
    fields = 'nextPageToken,albums{}'.format(album_fields)
    request = service.albums().list(pageToken=page_token, fields=fields)
    response = request.execute()

    # Getting albums list from response - if exists, else albums is empty list
    albums = response['albums'] if 'albums' in response else []

    # If in response is 'nextPageToken' - recursion and merging return to albums
    if 'nextPageToken' in response:
        albums += get_albums(response['nextPageToken'], album_fields)

    return albums


def test():
    albums = get_albums(album_fields='(id,title,mediaItemsCount,productUrl)')
    pprint(albums[1])

    album = GoogleAlbum()
    album.from_dict(albums[1])


if __name__ == '__main__':
    # test()
    main()
