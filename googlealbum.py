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
        return 'Google Photos Album "{}".\nURL: {}'.format(self.title, self.url)

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

    def from_id(self, service, album_id):
        request = service.albums().get(albumId=album_id)
        response = request.execute()
        self.from_dict(response)

    def to_dict(self):
        return {'id': self.id, 'title': self.title,
                'mediaItemsCount': self.items_count, 'productUrl': self.url}

    def download(self, service, directory, page_token=None,
                 media_fields='(id,filename,baseUrl)', counter=0):
        """
        Method downloads whole album from Google Photos to directory.
        Calls method GoogleMediaItem.download_to_dir() to download each media
        item in the album. Recursion as long as in response is next page token.

        :param service: googleapiclient flow object
        :param directory: destination directory for downloaded album
        :param page_token: string - next page token, for 1st call None
        :param media_fields: string - listing keys in dict describing
        mediaItems, starts and ends with brackets (), comma-separated, no
        whitespace characters, eg. '(filename,mediaMetadata,baseUrl)', default
        empty string gets all possible fields
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
            self.download(service, directory, response['nextPageToken'],
                          media_fields, counter)


def get_albums(service, page_token=None,
               album_fields='(id,title,mediaItemsCount,productUrl)'):
    """
    Function gets list of all GoogleAlbums from user photo library.
    Recursion as long as in response is next page token.

    :param service: service
    :param page_token: string - next page token, for 1st call None
    :param album_fields: string - listing keys in dict describing albums,
    starts and ends with brackets (), comma-separated, no whitespace characters,
    eg. '(id,title,mediaItemsCount,productUrl)', default empty string gets all
    possible fields
    :return:
    """

    # Setting fields and request
    fields = 'nextPageToken,albums{}'.format(album_fields)
    request = service.albums().list(pageToken=page_token, fields=fields)
    response = request.execute()

    # Getting albums list from response - if exists, else albums is empty list
    albums_list = response['albums'] if 'albums' in response else []
    albums = []
    for album in albums_list:
        albums.append(GoogleAlbum())
        albums[-1].from_dict(album)

    # If in response is 'nextPageToken' - recursion and merging return to albums
    if 'nextPageToken' in response:
        albums += get_albums(service, response['nextPageToken'], album_fields)

    return albums
