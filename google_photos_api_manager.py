"""
AR, 2018-10-25
Google Photos APIs with REST using request
"""

import requests


# Function returns access token to user's account
# def get_bearer_token():
#     store = file.Storage(CREDENTIALS)
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
#         creds = tools.run_flow(flow, store)
#     else:
#         creds.refresh(httplib2.Http())
#     return creds.access_token


# Function returns information about user's albums in JSON format
def get_albums(bearer_token, page_size=20):
    url = 'https://photoslibrary.googleapis.com/v1/albums'
    headers = {'Authorization': 'Bearer %s' % bearer_token}
    payload = {'pageSize': '%s' % page_size}
    response = requests.get(url=url, headers=headers, params=payload)
    return response.json()


# Function returns information about items in given album (in JSON format)
def get_items_from_album(bearer_token, album_id, page_size=25, page_token=None):
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    headers = {'Authorization': 'Bearer %s' % bearer_token,
               'Content - type': 'application / json'}
    payload = {'pageSize': '%s' % page_size, 'albumId': album_id}

    # If album has more than page_size (25) items, next page can be access using
    # page token - returned in previous request with list of item in the album
    if page_token:
        payload['pageToken'] = page_token

    response = requests.post(url=url, headers=headers, params=payload)
    return response.json()
