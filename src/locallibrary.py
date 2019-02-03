"""
Albert Ratajczak, 2018
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
        """
        self.path: path to local library dir
        self.albums: dict with album IDs as keys and sets of item IDs as values
        """
        self.path = os.path.join(os.path.expanduser('~'), app_name)
        self.albums = dict()

    def __str__(self):
        return 'Local library:\n- library directory: {}\n- tracked albums: {}'\
               .format(self.path, len(self.albums))

    def add(self, album_id):
        """
        Adds album ID as a key to dict of tracked albums (albums to download)
        :param album_id: ID of an album in Google Photos
        :return: None
        """
        if not isinstance(album_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        self.albums.update({album_id: set()})

    def remove(self, album_id):
        """
        Removes album ID from dict of tracked albums IDs
        :param album_id: ID of an album in Google Photos
        :return: None
        """
        if not isinstance(album_id, str):
            raise TypeError('add() takes \'str\' object as argument')
        try:
            self.albums.pop(album_id)
        except KeyError:
            pass

    def get_album_ids(self):
        return list(self.albums.keys())

    def add_to_album(self, album_id, item_ids=set()):
        """
        Adds item IDs as values to dict self.albums for key album_id
        """
        self.albums[album_id].update(item_ids)

    def get_album_items(self, album_id):
        """
        :returns: IDs of items in given album
        """
        return self.albums[album_id]

    def get_path(self):
        return self.path

    @user_dir
    def load(self, **kwargs):
        """
        Loads local library setups from JSON file: path and albums
        :param kwargs: to send user directory between method and decorator
        :return: self
        """
        # Reading JSON file
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        if os.path.exists(json_file):
            with open(json_file) as f:
                storage = json.load(f)
            self.path = storage['path']
            self.albums = storage['albums']
            # Converting lists form JSON file to sets
            for key in self.albums:
                self.albums[key] = set(self.albums[key])
            return self

    @user_dir
    def store(self, **kwargs):
        """
        Stores (saves) local library setups to JSON file: path and albums
        :param kwargs: to send user directory between method and decorator
        :return: None
        """
        albums = dict()
        # Converting sets in albums dict to lists - JSON dosn't accept set
        for key in self.albums:
            albums[key] = list(self.albums[key])
        # Saving to JSON file
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        with open(json_file, 'w') as f:
            json.dump({'path': self.path, 'albums': albums}, f)

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
