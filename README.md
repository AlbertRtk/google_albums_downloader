# Albums Downloader
Downloads photos from albums in your Google Photos Library.

## Verion 1.0
### What you can do?
* List your albums from Google Photos
* Select album(s) to be tracked
* Download/update tracked album(s) to local library on your hard drive
* ALL photos from the album(s) are always downloaded (photos, which has been downloaded earlier, will be overwritten)

### How to run it?
* In project directory (v1p0), you need to place client_secret.json file from [Google API Console](https://console.developers.google.com/apis/)
* You also need virtual environment for the project (venv directory)
* If you have client_secret.json and virtual environment, run run.bat file

### About client secret
* Create new project in [Google API Console](https://console.developers.google.com/apis/)
* Enable Photos Library API
* Create and download credentials (OAuth client ID). Save them as client_secret.json
