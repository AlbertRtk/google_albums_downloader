# general imports
import os
from urllib.request import urlretrieve


class GoogleMediaItem:
    def __init__(self, name=None, type=None, base_url=None,
                 width=None, height=None, creation_time=None, metadata=None):
        self.name = name
        self.type = type
        self.base_url = base_url
        self.width = width
        self.height = height
        self.creation_time = creation_time
        self.metadata = metadata

    def __str__(self):
        return 'Media item {}: {}=w{}-h{}'.\
            format(self.name, self.base_url, self.width, self.height)

    #
    def from_dict(self, dictionary):
        """
        Sets GoogleMediaItem object attributes to values given in dictionary

        :param dictionary: with info about one of media items from list returned
        by Google APIs request:
        service.mediaItems().search(body).execute()['mediaItems']
        :return: None
        """

        required_keys = ['filename', 'mediaMetadata', 'baseUrl']
        assert all(key in list(dictionary.keys()) for key in required_keys), \
            'Dictionary missing required key. GoogleMediItem.from_dict() ' \
            'requires keys: {}'.format(required_keys)

        self.name = dictionary['filename']
        self.width = dictionary['mediaMetadata']['width']
        self.height = dictionary['mediaMetadata']['height']
        base_url = dictionary['baseUrl']
        self.base_url = base_url
        self.creation_time = dictionary['mediaMetadata']['creationTime']

        if 'photo' in dictionary['mediaMetadata']:
            self.type = 'photo'
        else:  # 'video' in inner_dict['mediaMetadata']:
            self.type = 'video'

        self.metadata = dictionary['mediaMetadata'][self.type]

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
