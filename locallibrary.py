import os.path

from googlealbum import GoogleAlbum


class LocalLibrary:
    def __init__(self, app_name):
        self.path = os.path.join(os.path.expanduser('~'), app_name)
        self.downloaded_albums = set()

    def __str__(self):
        return 'App settings:\n- library path: {}\n- downloaded albums: {}'\
            .format(self.path, len(self.downloaded_albums))

    def add(self, google_album):
        if not isinstance(google_album, GoogleAlbum):
            raise TypeError('append() takes GoogleAlbum instance as argument')
        self.downloaded_albums.add(google_album)

    def get_ids(self):
        ids = set()
        for album in self.downloaded_albums:
            ids.add(album.id)
        return ids

    def get_path(self):
        return self.path

    def load(self, file):
        pass

    def store(self, file):
        pass

    def set_path(self, path):
        assert os.path.isabs(path), 'Argument path has to be absolute path'
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
