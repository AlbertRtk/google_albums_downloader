"""
AR1 2018-11-14
Class LocalLibrary - stores information about path to local library directory
and IDs of tracked albums
"""

# general imports
import os
import json

# local imports
from userdir import user_dir


class LocalLibrary:
    def __init__(self, app_name):
        self.path = os.path.join(os.path.expanduser('~'), app_name)
        self.albums = set()

    def __str__(self):
        return 'Local library:\n' \
               '- library directory: {}\n' \
               '- tracked albums: {}'\
               .format(self.path, len(self.albums))

    def add(self, album_id):
        """
        Adds album ID to set of tracked albums ISs (albums to download)

        :param album_id: ID of an album in Google Photos
        :return: None
        """
        if not isinstance(album_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        self.albums.add(LocalAlbum(album_id))

    def remove(self, album_id):
        """
        Removes album ID from set of tracked albums IDs

        :param album_id: ID of an album in Google Photos
        :return: None
        """
        if not isinstance(album_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        try:
            for album in self.albums:
                if album_id is album.get_id():
                    self.albums.remove(album)
                    break
        except KeyError:
            pass

    def get_ids(self):
        return [album.get_id() for album in self.albums]

    def get_path(self):
        return self.path

    @user_dir
    def load(self, **kwargs):
        """
        Loads local library setups from JSON file: path and IDs of tracked
        albums

        :param kwargs: to send user directory between method and decorator
        :return: self
        """
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        if os.path.exists(json_file):
            with open(json_file) as f:
                storage = json.load(f)
            self.path = storage['path']
            [self.albums.add(LocalAlbum(i)) for i in storage['albums']]
            return self

    @user_dir
    def store(self, **kwargs):
        """
        Stores (saves) local library setups to JSON file: path and IDs of
        tracked albums

        :param kwargs: to send user directory between method and decorator
        :return: None
        """
        library = {'path': self.path, 'albums': self.get_ids()}
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        with open(json_file, 'w') as f:
            json.dump(library, f)

    def set_path(self, path):
        """
        Sets path to directory of local library

        :param path: absolute path to local library
        :return: self.path
        """
        assert os.path.isabs(path), 'Argument path has to be absolute path'
        if path != self.path:
            if not os.path.exists(path):
                os.makedirs(path)
            self.path = path
        return self.path


# TODO: saving item ids to LocalAlbum
class LocalAlbum:
    def __init__(self, album_id):
        self.id = album_id
        self.item_ids = set()

    def add(self, item_id):
        """
        """
        if not isinstance(item_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        self.item_ids.add(item_id)

    def remove(self, item_id):
        """
        """
        if not isinstance(item_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        try:
            self.item_ids.remove(item_id)
        except KeyError:
            pass

    def get_id(self):
        return self.id

    def get_item_ids(self):
        return self.item_ids
