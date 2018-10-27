# general imports
import os

# local imports
from googlemediaitem import GoogleMediaItem


class GoogleAlbum:
    def __init__(self, album_id=None, title=None, items_count=None, url=None):
        self.id = album_id
        self.title = title
        self.items_count = items_count
        self.url = url

    def __str__(self):
        return 'Album "{}": {}'.format(self.title, self.url)

    def set_title(self, title):
        self.title = title

    def from_dict(self, dictionary):
        """
        Sets GoogleAlbum object attributes to values given in dictionary

        :param dictionary: with info about one of albums from list returned by
        Google APIs request: service.albums().list().execute()['albums']
        :return: None
        """
        required_keys = ['id', 'title', 'mediaItemsCount', 'productUrl']
        assert all(key in list(dictionary.keys()) for key in required_keys), \
            'Dictionary missing required key. GoogleAlbum.from_dict() ' \
            'requires keys: {}'.format(required_keys)

        self.id = dictionary['id']
        self.title = dictionary['title']
        self.items_count = int(dictionary['mediaItemsCount'])
        self.url = dictionary['productUrl']

    def download(self, service, page_token=None, media_fields='',
                  directory=os.path.expanduser('~'), counter=0):
        """
        Method downloads whole album from Google Photos to directory.
        Calls method GoogleMediaItem.download_to_dir() to download each media
        item in the album. Recursion as long as in response is next page token.

        :param service: googleapiclient flow object
        :param page_token: string - next page token, for 1st call None
        :param media_fields: string - listing keys in dict describing
        mediaItems, starts and ends with brackets (), comma-separated, no
        whitespace characters, eg. '(filename,mediaMetadata,baseUrl)', default
        empty string gets all possible fields
        :param directory: destination directory for downloaded album, by default
        user home directory (on Windows C:\\Users\\User)
        :param counter: int - just a simple counter to count downloaded media
        :return: None
        """

        # Setting destination directory for media files - named as album
        album_dir = os.path.join(directory, self.title)
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)

        # Setting body, fields and request
        body = {'albumId': self.id, 'pageToken': page_token, }
        fields = 'nextPageToken,mediaItems{}'.format(media_fields)
        request = service.mediaItems().search(body=body, fields=fields)
        response = request.execute()

        # Getting media items list from response
        items = response['mediaItems'] if 'mediaItems' in response else []

        media = GoogleMediaItem()
        # Downloading all media from the page
        for item in items:
            counter += 1
            media.from_dict(item)
            name = media.download(album_dir)
            print('({}/{}) Downloaded: {}'.
                  format(counter, self.items_count, name))

        if 'nextPageToken' in response:
            self.download(service, response['nextPageToken'], media_fields,
                          directory, counter)
