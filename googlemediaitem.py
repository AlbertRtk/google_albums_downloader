# general imports
import os
import requests
from PIL import Image
from io import BytesIO
import piexif


class GoogleMediaItem:
    def __init__(self, name=None, type=None, url=None, width=None, height=None,
                 creation_time=None, metadata=None):
        self.name = name
        self.type = type
        self.url = url
        self.width = width
        self.height = height
        self.creation_time = creation_time
        self.metadata = metadata

    def __str__(self):
        return 'Media item {}: {}'.format(self.name, self.url)

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
        assert all(key in required_keys for key in list(dictionary.keys())), \
            'Dictionary missing required key. GoogleMediItem.from_dict() ' \
            'requires keys: {}'.format(required_keys)

        self.name = dictionary['filename']
        self.width = dictionary['mediaMetadata']['width']
        self.height = dictionary['mediaMetadata']['height']
        base_url = dictionary['baseUrl']
        self.url = '{}=w{}-h{}'.format(base_url, self.width, self.height)
        self.creation_time = dictionary['mediaMetadata']['creationTime']

        if 'photo' in dictionary['mediaMetadata']:
            self.type = 'photo'
        else:  # 'video' in inner_dict['mediaMetadata']:
            self.type = 'video'

        self.metadata = dictionary['mediaMetadata'][self.type]

    def download_to_dir(self, directory, metadata=True):
        """
        Downloads media item to given directory.

        :param directory: destination directory for downloaded item
        :param metadata: boolean argument defining if media item is saved with
        (True, default) or without (False) metadata
        :return: filename, full path to saved media item
        """

        # Setting filename - full path
        filename = os.path.join(directory, self.name)

        # Setting url, getting and saving media
        response = requests.get(self.url)
        media = Image.open(BytesIO(response.content))
        media.save(filename)

        # Inserting EXIF metadata into media file
        if metadata:
            self.insert_metadata(filename)

        return filename

    def insert_metadata(self, file):
        """
        Method inserts metadata of GoogleMediaItem into given file.
        More about mediaItem metadata at:
        developers.google.com/photos/library/guides/access-media-items#get-media-item

        :param file: path to saved media file - photo or video
        :return: None
        """

        # Creation time
        dt = self.creation_time
        dt = '{}:{}:{} {}'.format(dt[:4], dt[5:7], dt[8:10], dt[11:-1])
        exif_ifd = {piexif.ExifIFD.DateTimeOriginal: dt, }

        # Camera producer and model
        zeroth_ifd = {piexif.ImageIFD.Make: self.metadata['cameraMake'],
                      piexif.ImageIFD.Model:  self.metadata['cameraModel'], }

        # Inserting EXIF
        exif_dict = {'0th': zeroth_ifd, 'Exif': exif_ifd, '1st': zeroth_ifd}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file)
        return None
