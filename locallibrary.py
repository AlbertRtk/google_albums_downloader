import os.path
import json


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

    # TODO
    def load(self):
        pass

    def store(self):
        cwd = os.getcwd()
        user_dir = os.path.join(cwd, 'user')
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        ids = [i for i in self.album_ids]
        library = {'path': self.path, 'album_ids': ids}

        with open(os.path.join(user_dir, 'local_library.json'), 'w') as f:
            json.dump(library, f)

    def set_path(self, path):
        assert os.path.isabs(path), 'Argument path has to be absolute path'
        if path != self.path:
            if not os.path.exists(path):
                os.makedirs(path)
            self.path = path
        return self.path
