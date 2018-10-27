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

    def download(self, service, directory='.'):
        """
        Method downloads whole album from Google Photos to directory.
        Calls method GoogleMediaItem.download_to_dir() to download each media
        item in the album.

        :param service: googleapiclient flow object
        :param directory: destination directory for downloaded album
        :return: None
        """

        # Setting page size (items/page) and counter of downloads
        page_size = 25
        counter = 0

        # Setting and creating destination directory
        album_dir = os.path.join(directory, self.title)
        if not os.path.exists(album_dir):
            os.makedirs(album_dir)

        # Body and fields for service call
        body = {'pageSize': page_size, 'albumId': self.id, 'pageToken': None, }
        fields = 'nextPageToken,mediaItems(filename,mediaMetadata,baseUrl)'

        # Repeat until counts of downloads lower than items in the album
        while counter < self.items_count:
            # Getting next page with list of media in album
            items = service.mediaItems().search(body=body, fields=fields)
            items = items.execute()
            media_items = items['mediaItems']

            media = GoogleMediaItem()
            # Downloading all media from the page
            for item in media_items:
                counter += 1
                media.from_dict(item)
                name = media.download(album_dir)
                print('({}/{}) downloaded: {}'.
                      format(counter, self.items_count, name))

            # Setting new page token in body, for next execution
            # Handling exception - if key 'nextPageToken' doesn't exist, return
            # Last page doesn't have nextPagToken
            try:
                body['pageToken'] = items['nextPageToken']
            except KeyError:
                return None
