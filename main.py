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

# imports from google-api-python-client library
from googleapiclient.discovery import build

# local imports
from authorization import Authorization
from googlealbum import GoogleAlbum
from googlemediaitem import GoogleMediaItem


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


def main():
    # Getting albums
    fields = 'nextPageToken,albums(id,title,mediaItemsCount,productUrl)'
    albums = service.albums().list(pageSize=20, fields=fields).execute()
    albums = albums['albums']

    album = GoogleAlbum()
    album.from_dict(albums[1])
    print(album)
    album.download(service, directory=LIBRARY_PATH)


def test():
    fields = 'nextPageToken,albums(id,title,mediaItemsCount,productUrl)'
    albums = service.albums().list(pageSize=2, fields=fields).execute()
    pprint(albums)

    album = GoogleAlbum()
    album.from_dict(albums['albums'][1])

    # Body and fields for service call
    body = {'pageSize': 25, 'albumId': album.id, 'pageToken': None, }
    fields = 'nextPageToken,mediaItems(filename,mediaMetadata,baseUrl)'
    items = service.mediaItems().search(body=body, fields=fields)
    items = items.execute()
    media_items = items['mediaItems']

    media = GoogleMediaItem()
    media.from_dict(media_items[1])
    print(media.name)


if __name__ == '__main__':
    # test()
    main()
