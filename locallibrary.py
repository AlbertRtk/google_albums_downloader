"""

"""

# general imports
import os
import json

# local imports
from userdir import user_dir


# TODO: commenting
class LocalLibrary:
    def __init__(self, app_name):
        self.path = os.path.join(os.path.expanduser('~'), app_name)
        self.album_ids = set()

    def __str__(self):
        return 'Local library:\n' \
               '- library directory: {}\n' \
               '- downloaded albums: {}'\
               .format(self.path, len(self.album_ids))

    def add(self, album_id):
        if not isinstance(album_id, str):
            raise TypeError('add() takes \str\' object as argument')
        self.album_ids.add(album_id)

    def get_ids(self):
        return self.album_ids

    def get_path(self):
        return self.path

    @user_dir
    def load(self, **kwargs):
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        try:
            with open(json_file) as f:
                storage = json.load(f)
            self.path = storage['path']
            [self.album_ids.add(i) for i in storage['album_ids']]
            return True
        except FileNotFoundError:
            return False

    @user_dir
    def store(self, **kwargs):
        ids = [i for i in self.album_ids]
        library = {'path': self.path, 'album_ids': ids}
        json_file = os.path.join(kwargs['user_dir'], 'local_library.json')
        with open(json_file, 'w') as f:
            json.dump(library, f)

    def set_path(self, path):
        assert os.path.isabs(path), 'Argument path has to be absolute path'
        if path != self.path:
            if not os.path.exists(path):
                os.makedirs(path)
            self.path = path
        return self.path
