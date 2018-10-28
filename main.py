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

# imports from google-api-python-client library
from googleapiclient.discovery import build

# local imports
from locallibrary import LocalLibrary
from authorization import Authorization
from googlealbum import get_albums


APP_NAME = 'Albums downloader'

# Name of a file that contains the OAuth 2.0 information for this application:
CLIENT_SECRETS_FILE = "client_secret.json"

# This access scope grants read-only access:
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'


LIBRARY_PATH = os.path.join(os.path.expanduser('~'), APP_NAME)
DOWNLOADED_ALBUMS = 'downloaded_albums.json'

# Settings
library = LocalLibrary(APP_NAME)

# Getting authorization
authorization = Authorization(APP_NAME, SCOPES, CLIENT_SECRETS_FILE)
credentials = authorization.get_credentials()
print(credentials)
# Building service
service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# DONE: storing album ids TODO: with list of downloaded photos
# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo
# TODO: user interface - console

def main():
    library.load()
    print('\nStarting {}'.format(library))

    # Getting albums
    fields = '(id,title,mediaItemsCount,productUrl)'
    albums = get_albums(service, album_fields=fields)

    # Titles of albums to download start with #
    pattern = re.compile('^#\s*')

    for album in albums:
        # If title starts with # - changing title and downloading
        if bool(re.match(pattern, album.title)):
            print(album, end='\n'*2)
            library.add(album.id)
            album.set_title(re.sub(pattern, '', album.title))
            # album.download(service, directory=LIBRARY_PATH)

    library.store()
    print('\nUpdated {}'.format(library))


def test():
    library.load()
    print('\nStarting {}'.format(library))
    print(library.get_path())
    print(library.get_ids())

    # library.store()
    print('\nUpdated {}'.format(library))

    # print(library)
    # album = GoogleAlbum()
    # library.add(album)
    # library.add(album)
    # library.set_path('C:\\Users\\Albert\\Albums downloader')
    #
    # print(library.get_ids())
    #
    # print(library)


if __name__ == '__main__':
    # test()
    main()

# end of file

"""
    # Titles of albums to download start with #
    pattern = re.compile('^#\s*')

    for album in albums:
        # If title starts with # - changing title and downloading
        if bool(re.match(pattern, album.title)):
            print(album, end='\n'*2)
            library.add(album.id)
            album.set_title(re.sub(pattern, '', album.title))
            album.download(service, directory=LIBRARY_PATH,
                           media_fields='(id,filename,baseUrl)')
"""