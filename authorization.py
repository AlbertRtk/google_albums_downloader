"""
AR, 2018-10-25
Authorization class and get_credentials method for Google APIs
"""

from oauth2client import file, client, tools
import httplib2
import os


# Class with data for authorization of connection between client and service
class Authorization:
    def __init__(self, app_name, scopes, client_secret_file):
        self.app_name = app_name
        self.scopes = scopes
        self.client_secret_file = client_secret_file

    def __str__(self):
        return 'Authorization class for {}'.format(self.app_name)

    # Method gets user credential from storage - JSON file
    # If credential are not in storage or are invalid, gets new credentials
    # If stored credential are expired, refreshes them
    # Return credentials
    def get_credentials(self):
        # Setting directory and JSON file with user's credentials
        cwd_dir = os.getcwd()
        creds_dir = os.path.join(cwd_dir, 'credentials')
        if not os.path.exists(creds_dir):
            os.makedirs(creds_dir)
        creds_file = os.path.join(creds_dir, 'user_credentials.json')

        # Getting credentials from Storage
        store = file.Storage(creds_file)
        creds = store.get()
        # print(store == creds.store)  # just a test

        # Validating or refreshing credentials, if necessary
        if creds is None or creds.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file,
                                                  self.scopes)
            creds = tools.run_flow(flow, store)
        elif creds.access_token_expired:
            creds.refresh(httplib2.Http())
        else:
            pass

        return creds


"""
HELP:

About tools.run_flow:
'The new credentials are also stored in the storage argument, 
which updates the file associated with the Storage object.'
https://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html

About OAuth2Credentials and refresh():
'Forces a refresh of the access_token' - and updates Storage object by storage 
argument of credentials (see tools.run_flow above). 
Storage argument is set by file.Storage.get(), when credentials are loaded
https://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html#oauth2client.client.OAuth2Credentials

"""
