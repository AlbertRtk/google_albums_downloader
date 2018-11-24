"""
AR, 2018-11
Class GoogleMediaItem - stores information about media item from Google Photos
"""

# general imports
import os
from urllib.request import urlretrieve


class GoogleMediaItem:
    def __init__(self, name=None, item_id=None, base_url=None):
        self.name = name
        self.id = item_id
        self.base_url = base_url

    def __str__(self):
        return 'Media item {}: {}'.format(self.name, self.base_url)

    def from_dict(self, dictionary):
        """
        Sets GoogleMediaItem object attributes to values given in dictionary

        :param dictionary: with info about one of media items from list returned
        by Google APIs request:
        service.mediaItems().search(body).execute()['mediaItems']
        :return: None
        """

        required_keys = ['filename', 'id', 'baseUrl']
        assert all(key in list(dictionary.keys()) for key in required_keys), \
            'Dictionary missing required key. GoogleMediaItem.from_dict() ' \
            'requires keys: {}'.format(required_keys)

        self.name = dictionary['filename']
        self.id = dictionary['id']
        self.base_url = dictionary['baseUrl']

    def download(self, directory):
        """
        Downloads media item to given directory (with metadata, except GPS).
        Info about download URL:
        https://developers.google.com/photos/library/guides/access-media-items#image-base-urls

        :param directory: destination directory for downloaded item
        :return: filename, full path to saved media item
        """

        # Setting filename (full path) and URL of file to download
        filename = os.path.join(directory, self.name)
        download_url = '{}=d'.format(self.base_url)

        # Downloading
        urlretrieve(download_url, filename)

        return filename
