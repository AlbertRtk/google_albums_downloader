"""
AR, 2018-10-25

Program "Albums Downloader"  - downloads media items (photos, videos) from an
                               album in Google Photos using Google Photos APIs
                               and google-api-phyton-client

For help with APIs check:
https://developers.google.com/photos/library/guides/overview
"""

# general imports
import os

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


# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo

def main():
    os.system('cls')
    # Loading library info from JSON or setting library (1st run)
    loaded = library.load()
    if loaded is None:
        set_library()
    else:
        print(library)

    while True:
        print('\n[A] add      \t [R] remove   \t [L] list     \t [U] update   '
              '\n[S] settings \t [H] help     \t [Q] quit    ')
        choice = input('What do you want to do:\n>> ').upper()
        os.system('cls')

        if choice == 'A':
            manage_library('add')
            os.system('cls')
            tracked_albums()
        elif choice == 'R':
            manage_library('remove')
            os.system('cls')
            tracked_albums()
        elif choice == 'L':
            tracked_albums()
        elif choice == 'U':
            update_library()
        elif choice == 'S':
            set_library()
        elif choice == 'H':
            show_help()
        elif choice == 'Q':
            break
        else:
            print('Unknown command. Try again or choose H to get help.')

        library.store()


def manage_library(action):
    albums = tracked_albums()

    if action == 'add':
        func = LocalLibrary.add
        prt = action + ' to'
    else:
        func = LocalLibrary.remove
        prt = action + ' from'

    ids = input('\nType ID numbers of albums you want to {} download list\n'
                '(comma separated, leave empty to cancel):\n>> '.format(prt))
    if ids is not '':
        ids = ids.split(',')
        for i in ids:
            try:
                if int(i) > 0:
                    func(library, albums[int(i)-1].id)
            except (ValueError, IndexError):
                pass


def set_library():
    print('Path to local library: {}'.format(library.get_path()))
    path = input('Give new absolute path to local library '
                 '[leave empty to keep current]:\n>> ')
    if os.path.isabs(path):
        print('New library path: {}'.format(library.set_path(path)))
    else:
        print('Path not changed.')
    library.store()


def show_help():
    print('*** Albums Downloader *** AR, 2018 *** \n'
          'Download photos from albums in your Google Photos Library. \n\n'
          'Detailed description of commands: \n'
          '[A] - add albums to track list \n'
          '[R] - remove album from track list \n'
          '[L] - list all albums and mark tracked \n'
          '[U] - update local library \n'
          '[S] - set path of local library \n'
          '[H] - show help \n'
          '[Q] - quite the program')


def tracked_albums():
    print('Your Google Photos Albums ([X] = tracked):')
    albums = get_albums(service)
    for i, a in enumerate(albums):
        check = 'X' if a.id in library.get_ids() else ' '
        print('[{}] {}. {}'.format(check, i+1, a.title))
    return albums


def update_library():
    print('*** Updating local library ***')
    album = GoogleAlbum()
    for i in library.get_ids():
        album.from_id(service, album_id=i)
        print('\n{}'.format(album))
        album.download(service, library.get_path())


if __name__ == '__main__':
    main()
