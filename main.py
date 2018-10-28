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

# imports from google-api-python-client library
from googleapiclient.discovery import build

# local imports
from locallibrary import LocalLibrary
from authorization import Authorization
from googlealbum import GoogleAlbum, get_albums


# Settings
APP_NAME = 'Albums downloader'
library = LocalLibrary(APP_NAME)
# File with the OAuth 2.0 information:
CLIENT_SECRETS_FILE = "client_secret.json"
# This access scope grants read-only access:
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'

# Getting authorization and building service
authorization = Authorization(APP_NAME, SCOPES, CLIENT_SECRETS_FILE)
credentials = authorization.get_credentials()
service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# DONE: storing album ids TODO: with list of downloaded photos
# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo
# TODO: user interface - console

def main():
    # Loading library info from JSON or setting library (1st run)
    loaded = library.load()
    if loaded is False:
        print('Default path to local library: {}'.format(library.get_path()))
        path = input('Give absolute path to local library '
                     '[leave empty to keep default]:\n')
        if os.path.isabs(path):
            print('Library path: {}'.format(library.set_path(path)))
        else:
            print('Keeping default path.')
        library.store()
    else:
        print(library)

    # Updating albums in local library
    print('\n*** Updating local library ***')
    album = GoogleAlbum()
    for i in library.get_ids():
        album.from_id(service, album_id=i)
        print(album)
        album.download(service, library.get_path())

    library.store()
    print('\nUpdated {}'.format(library))


if __name__ == '__main__':
    main()
