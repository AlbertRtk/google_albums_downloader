"""
AR, 2018-10-25

Program "Get Photos"  - downloads media items (photos, videos) from an album
                        in Google Photos using Google Photos APIs and
                        google-api-phyton-client

For help with APIs check:
https://developers.google.com/photos/library/guides/overview
"""

# general imports
from pprint import pprint
import re

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
LIBRARY_PATH = 'F:\\'

# Getting authorization
authorization = Authorization(APP_NAME, SCOPES, CLIENT_SECRETS_FILE)
credentials = authorization.get_credentials()
# Building service
service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# TODO: storing album ids with list of downloaded photos
# TODO: refreshing album if its items changed
# TODO: option for refreshing downloaded photo
# TODO: user interface - console

def main():
    # Getting albums
    page_size = 10  # max 20
    fields = 'nextPageToken,albums(id,title,mediaItemsCount,productUrl)'
    albums = service.albums().search(pageSize=10, fields=fields).execute()
    albums = albums['albums']

    g_album = GoogleAlbum()

    # Titles of albums to download start with #
    pattern = re.compile('^#\s*')

    for album in albums:
        g_album.from_dict(album)

        # If title starts with # - changing title and downloading
        if bool(re.match(pattern, g_album.title)):
            print(g_album)
            g_album.set_title(pattern.split(g_album.title)[1])
            g_album.download(service, directory=LIBRARY_PATH)


def get_albums(page_token=None):
    """

    :param page_token:
    :return:
    """
    fields = 'nextPageToken,albums'
    request = service.albums().list(pageToken=page_token, fields=fields)
    response = request.execute()

    try:
        albums = response['albums']
    except KeyError:
        return {}

    if 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        next_page = get_albums(page_token=next_page_token)
        albums.append(next_page)

    return albums


def test():
    albums = get_albums()
    pprint(albums[1])

    for k in ['id', 'title', 'mediaItemsCount', 'productUrl']:
        print(albums[1][k])

    album = GoogleAlbum()
    album.from_dict(albums[1])
    print(album)


if __name__ == '__main__':
    test()
    # main()
