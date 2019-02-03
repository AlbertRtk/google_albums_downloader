"""
Albert Ratajczak, 2018

Program "Albums Downloader"  - downloads media items (photos, videos) from an
                               album in Google Photos using Google Photos APIs
                               and google-api-phyton-client

For help with APIs check:
https://developers.google.com/photos/library/guides/overview
"""

# general imports
import os

# Local imports
from locallibrary import LocalLibrary
from googlealbum import GoogleAlbum, get_albums
from initialize import initialize


# Initialization of local library and Google APIs conection service
library, service = initialize()


def main():
    os.system('cls')

    # Menu options
    options = {
               'A': library_add,
               'R': library_remove,
               'L': tracked_albums,
               'U': update_library,
               'S': set_library,
               'H': show_help,
               'Q': quit,
               }

    # Loading library info from JSON or setting library (1st run)
    loaded = library.load()
    if loaded is None:
        set_library()
    else:
        print(library)

    while True:
        # Printing menu and reading choice of action
        print('\n[A] add      \t [R] remove   \t [L] list     \t [U] update   '
              '\n[S] settings \t [H] help     \t [Q] quit    ')
        choice = input('What do you want to do:\n>> ').upper()
        os.system('cls')

        # Calling chosen action
        try:
            options[choice]()
        except KeyError:
            print('Unknown command. Try again or choose H to get help.')

        # Saving library setting after each action
        library.store()


def manage_library(action):
    """
    Adding or removing Google Album to/from local library settings.
    Removes only ID from LocalLibrary instance, do NOT remove file from local
    library directory
    :param action: str, 'add' or 'remove'
    :return: None
    """
    albums = tracked_albums()

    # Setting function to call and message to print
    if action == 'add':
        func = LocalLibrary.add
        prt = action + ' to'
    elif action == 'remove':
        func = LocalLibrary.remove
        prt = action + ' from'
    else:
        return None

    ids = input('\nType ID numbers of albums you want to {} download list\n'
                '(comma separated, leave empty to cancel):\n>> '.format(prt))
    if ids is not '':
        ids = ids.split(',')
        for i in ids:
            # Handling exception - user gives not int or not a number...
            try:
                if int(i) > 0:  # need to be here! list accepts negative indexes
                    func(library, albums[int(i)-1].id)
            except (ValueError, IndexError):
                pass
    os.system('cls')
    tracked_albums()


def library_add():
    manage_library('add')


def library_remove():
    manage_library('remove')


def set_library():
    """
    Sets new path of local library. Does NOT transfer library content (files)
    to new directory!
    """
    print('Path to local library: {}'.format(library.get_path()))
    path = input('Give new absolute path to local library '
                 '[leave empty to keep current]:\n>> ')
    if os.path.isabs(path):
        print('New library path: {}'.format(library.set_path(path)))
    else:
        print('Path not changed.')
    library.store()


def show_help():
    print('*** Albums Downloader *** AR, 2018 *** \n'
          'Download photos from albums in your Google Photos Library. \n\n'
          'Detailed description of commands: \n'
          '[A] - add albums to track list \n'
          '[R] - remove album from track list \n'
          '[L] - list all albums and mark tracked \n'
          '[U] - update local library \n'
          '[S] - set path of local library \n'
          '[H] - show help \n'
          '[Q] - quite the program')


def tracked_albums():
    """
    Prints list of all albums in Google Photos and marks with [X] those which
    are tracked (to download)
    :return: list of albums
    """
    print('Your Google Photos Albums ([X] = tracked):')
    albums = get_albums(service)
    for i, a in enumerate(albums):
        check = 'X' if a.id in library.get_album_ids() else ' '
        print('[{}] {}. {}'.format(check, i+1, a.title))
    return albums


def update_library():
    """
    Updates local library - downloads ALL tracked albums to local library.
    Downloads even photos which are already downloaded - replaces them
    """
    print('*** Updating local library ***')
    album = GoogleAlbum()
    # Downloading albums by ID (IDs from set stored in LocalLibrary instance)
    for i in library.get_album_ids():
        album.from_id(service, album_id=i)
        print('\n{}'.format(album))
        item_ids = album.download(
                                  service=service,
                                  directory=library.get_path(),
                                  skip=library.get_album_items(i)
                                  )
        library.add_to_album(i, item_ids)

if __name__ == '__main__':
    main()
