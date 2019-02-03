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
        self['width'] = 8
        self['height'] = 2


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Google Albums Downloader by Albert Ratajczak')
        self.pack()
        self.create_widgets()
        library.load()

    def __del__(self):
        library.store()  # TODO: there is some bug!?

    def create_widgets(self):
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
            self.print_report('DONE!\n')

    def print_report(self, report_text):
        self.report_text.insert(tk.INSERT, report_text)
        self.report_text.update()


""" >>>>>>>>>>>>>>>>>>>>  TRACKED WINDOW WIDGETS <<<<<<<<<<<<<<<<<<<< """

class MyCheck(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['onvalue'] = True
        self['offvalue'] = False
        self['width'] = 40
        self['height'] = 1


class TrackedWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Tracked Google Albums'
        self.check_vars = []
        self.checks = []
        self.create_list()
        # TODO: BUTTON - save (add/remove)

    def create_list(self):
        albums = get_albums(service)
        for i, a in enumerate(albums):
            self.check_vars.append(tk.BooleanVar())
            if a.id in library.get_album_ids():
                self.check_vars[i].set(True)
            self.checks.append(
                               MyCheck(
                                       self,
                                       text=a.title,
                                       var=self.check_vars[i]
                                       )
                               )
            self.checks[i].pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()
