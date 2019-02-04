"""
Albert Ratajczak, 2019
GUI for Google Albums Downloader
"""
import tkinter as tk

# Local imports
from locallibrary import LocalLibrary
from googlealbum import GoogleAlbum, get_albums
from initialize import initialize


# Initialization of local library and Google APIs conection service
library, service = initialize()


""" >>>>>>>>>>>>>>>>>>>>  MAIN WINDOW WIDGETS <<<<<<<<<<<<<<<<<<<< """

class MyButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['width'] = 12
        self['height'] = 2


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Google Albums Downloader by Albert Ratajczak')
        self.pack()
        self.create_widgets()
        library.load()

    def create_widgets(self):
        # Creating widgets
        self.report_text = tk.Text(self, width=80, height=12)
        self.albums_button = MyButton(
                                      self,
                                      text='Albums',
                                      command=TrackedWindow
                                      )
        self.update_button = MyButton(
                                      self,
                                      text='Update',
                                      command=self.update_library
                                      )
        self.quit_button = MyButton(
                                    self,
                                    text='Quit',
                                    command=self.master.destroy
                                    )
        # Placing widgets in the window
        self.report_text.pack(side='top')
        self.albums_button.pack(side='left')
        self.update_button.pack(side='left')
        self.quit_button.pack(side='left')

    def update_library(self):
        """
        Updates local library - downloads ALL tracked albums to local library.
        """
        self.print_report('Checking Googel Albums for updates:\n')
        album = GoogleAlbum()
        # Downloading albums by ID (IDs from set stored in LocalLibrary)
        for i in library.get_album_ids():
            album.from_id(service, album_id=i)
            self.print_report('--> {}... '.format(album.title))
            item_ids = album.download(
                                      service=service,
                                      directory=library.get_path(),
                                      skip=library.get_album_items(i)
                                      )
            library.add_to_album(i, item_ids)
            self.print_report('DONE! {} item(s) downloaded\n' \
                              .format(len(item_ids)))
        library.store()

    def print_report(self, report_text):
        self.report_text.insert(tk.INSERT, report_text)
        self.report_text.update()


""" >>>>>>>>>>>>>>>>>>>>  TRACKED WINDOW WIDGETS <<<<<<<<<<<<<<<<<<<< """

class MyCheckbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['onvalue'] = True
        self['offvalue'] = False
        self['width'] = 40
        self['height'] = 1
        self['anchor'] = 'w'  # text aligned to left 


class TrackedWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        """
        :selected: dict, keys - Google Album IDs, values - tk.BooleanVar
        (True -> download, False -> ignore)
        :checkbuttons: list with checkbuttons, linked to values of selected dict
        """
        super().__init__(*args, **kwargs)
        self.title = 'Tracked Google Albums'
        self.selected = dict()
        self.checkbuttons = list()
        # Widgets
        self.create_list()
        self.save_button = MyButton(
                                    self,
                                    text='Save',
                                    command=self.save_selected
                                    )
        self.save_button.pack()

    def create_list(self):
        # Gettingt albums from Google Photos
        albums = get_albums(service)
        for i, a in enumerate(albums):
            # Checking if album is saved in local library
            tracked = True if a.id in library.get_album_ids() else False
            # Setting checkbutton for each album, tracked albums selected
            self.selected.update({a.id: tk.BooleanVar(value=tracked)})
            self.checkbuttons.append(
                                     MyCheckbutton(
                                                   self,
                                                   text=a.title,
                                                   variable=self.selected[a.id]
                                                   )
                                     )
            self.checkbuttons[i].pack()

    def save_selected(self):
        """
        Saves selected albums to local library and closes selection window
        """
        for i in self.selected:
            if self.selected[i].get() == 1:
                library.add(i)
            else:
                library.remove(i)
        library.store()
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()
