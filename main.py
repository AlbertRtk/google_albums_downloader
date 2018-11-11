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
from auth import Auth
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
authorization = Auth(SCOPES, CLIENT_SECRETS_FILE)
credentials = authorization.get_credentials()
service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# DONE: storing album ids TODO: with list of downloaded photos
# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo

def main():
    # Loading library info from JSON or setting library (1st run)
    loaded = library.load()
    if loaded is None:
        set_library()
    else:
        print(library)

    while True:
        print('\n[A] add - [R] remove - [U] update - [Q] quit')
        choice = input('What do you want to do:\n>> ')

        if choice.upper() == 'A':
            # Adding albums to local library
            manage_library('add')
        elif choice.upper() == 'R':
            # Removing albums from local library
            manage_library('remove')
        elif choice.upper() == 'U':
            # Updating albums in local library
            update_library()
        elif choice.upper() == 'Q':
            break
        else:
            pass

    library.store()


def set_library():
    print('Default path to local library: {}'.format(library.get_path()))
    path = input('Give absolute path to local library '
                 '[leave empty to keep default]:\n>> ')
    if os.path.isabs(path):
        print('Library path: {}'.format(library.set_path(path)))
    else:
        print('Keeping default path.')
    library.store()


def manage_library(action):
    print('\nYour Google Photos Albums:')
    albums = get_albums(service)
    for i, a in enumerate(albums):
        check = 'X' if a.id in library.get_ids() else ' '
        print('[{}] {}. {}'.format(check, i+1, a.title))

    if action == 'add':
        func = LocalLibrary.add
        action += ' to'
    else:
        func = LocalLibrary.remove
        action += ' from'

    ids = input('\nType ID numbers of albums you want to {} download list\n'
                '(comma separated, leave empty to cancel):\n>> '.format(action))
    if ids is not '':
        ids = ids.split(',')
        for i in ids:
            if int(i) > 0:
                func(library, albums[int(i)-1].id)


def update_library():
    print('\n*** Updating local library ***')
    album = GoogleAlbum()
    for i in library.get_ids():
        album.from_id(service, album_id=i)
        print(album)
        album.download(service, library.get_path())
    print('\nUpdated {}'.format(library))


if __name__ == '__main__':
    main()
